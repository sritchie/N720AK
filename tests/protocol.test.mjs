import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Radio, RadioImage, WRITE_REGIONS, diffChunks, chunkRegions, MODEL_CODE } from '../sections/tools/fta850/fta850.js';
import { FakeRadio } from './fake-radio.mjs';

const fast = { timeout: 60, retries: 3, retryInterval: 1 };

function patternImage() {
  const img = RadioImage.default();
  for (let i = 0x3000; i < 0x3000 + 4800; i++) img.bytes[i] = (i * 7) & 0xff;
  return img;
}

test('connect wakes the radio, syncs twice and reads the firmware version', async () => {
  const fake = new FakeRadio();
  const radio = new Radio(fake, fast);
  const { version } = await radio.connect();
  assert.equal(version, 3.52);
  assert.equal(fake.received[0], 'P0ACMD:002');
  assert.deepEqual(fake.received.filter((l) => l === '#CMDSY').length, 2);
  await radio.close();
});

test('connect rejects a radio with firmware below 2.01', async () => {
  const fake = new FakeRadio({ firmware: '1.90' });
  const radio = new Radio(fake, fast);
  await assert.rejects(radio.connect(), /firmware/i);
  await radio.close();
});

test('connect retries the sync when the first reply is lost', async () => {
  const fake = new FakeRadio({ faults: { dropSync: 1 } });
  const radio = new Radio(fake, fast);
  await radio.connect();
  assert.equal(fake.received.filter((l) => l === '#CMDSY').length, 3);
  await radio.close();
});

test('readImage returns the radio image byte for byte and acks every block', async () => {
  const fake = new FakeRadio({ image: patternImage().bytes });
  const radio = new Radio(fake, fast);
  await radio.connect();
  const progress = [];
  const bytes = await radio.readImage((done, total) => progress.push([done, total]));
  assert.deepEqual(bytes, fake.image);
  assert.equal(fake.received.filter((l) => l.startsWith('#CEPRD')).length, 512);
  assert.equal(fake.received.filter((l) => l === '#CMDOK').length, 1024);
  assert.deepEqual(progress.at(-1), [32768, 32768]);
  await radio.close();
});

test('readImage re-requests a block whose reply had a bad checksum', async () => {
  const fake = new FakeRadio({ image: patternImage().bytes, faults: { corruptRead: 1 } });
  const radio = new Radio(fake, fast);
  await radio.connect();
  const bytes = await radio.readImage();
  assert.deepEqual(bytes, fake.image);
  assert.equal(fake.received.filter((l) => l.startsWith('#CEPRD\t0000')).length, 2);
  await radio.close();
});

test('readImage gives up after the retry budget when the radio goes silent', async () => {
  const fake = new FakeRadio({ faults: { silentAfter: 0x80 } });
  const radio = new Radio(fake, fast);
  await radio.connect();
  await assert.rejects(radio.readImage(), /timeout.*0080/i);
  assert.equal(fake.received.filter((l) => l.startsWith('#CEPRD\t0080')).length, 3);
  await radio.close();
});

test('writeChunks programs only the given chunks and waits out a busy status', async () => {
  const fake = new FakeRadio({ image: RadioImage.default().bytes, faults: { busyStatus: 2 } });
  const radio = new Radio(fake, fast);
  await radio.connect();
  const before = RadioImage.default();
  const after = before.clone();
  after.applyChannels([{ group: 1, freq: '118000', tag: 'BJC TWR' }, { group: 2, freq: '121500', tag: 'GUARD' }]);
  after.setGroupName(1, 'DENVER');
  const chunks = diffChunks(before.bytes, after.bytes, WRITE_REGIONS);
  await radio.writeChunks(after.bytes, chunks);
  assert.deepEqual(fake.image, after.bytes);
  assert.equal(fake.received.filter((l) => l.startsWith('#CEPWR')).length, chunks.length);
  assert.ok(fake.received.some((l) => l.startsWith('#CEPRD\t0100\t02')), 'reads the model code first');
  assert.ok(fake.received.some((l) => l.startsWith('#CEPRD\t7FFE\t02')), 'reads the footer model code first');
  await radio.close();
});

test('writeChunks refuses when the radio reports a different model code', async () => {
  const other = RadioImage.default().bytes; other[0x101] = 0x53;
  const fake = new FakeRadio({ image: other });
  const radio = new Radio(fake, fast);
  await radio.connect();
  await assert.rejects(radio.writeChunks(RadioImage.default().bytes, chunkRegions(WRITE_REGIONS).slice(0, 1)), /model/i);
  assert.equal(fake.received.filter((l) => l.startsWith('#CEPWR')).length, 0);
  await radio.close();
});

test('verifyChunks reads back and reports chunks that differ', async () => {
  const img = RadioImage.default();
  const fake = new FakeRadio({ image: new Uint8Array(img.bytes) });
  const radio = new Radio(fake, fast);
  await radio.connect();
  fake.image[0x3000 + 70] ^= 0xff;
  const chunks = chunkRegions(WRITE_REGIONS).filter((c) => c.addr >= 0x3000 && c.addr < 0x3100);
  const bad = await radio.verifyChunks(img.bytes, chunks);
  assert.deepEqual(bad.map((c) => c.addr), [0x3040]);
  await radio.close();
});
