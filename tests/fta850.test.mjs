import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  checksum, frame, verifyChecksum, parseReply,
  RadioImage, IMAGE_SIZE, MODEL_CODE, compareTag,
  validateFrequency, validateTag, channelsToCsv, csvToChannels,
  WRITE_REGIONS, chunkRegions, diffChunks,
} from '../sections/tools/fta850/fta850.js';

// ---------- framing ----------
test('checksum XORs every byte of the body (oracle from YCE46 frames)', () => {
  assert.equal(checksum('#CEPSR\t00\t'), '74');
  assert.equal(checksum('#CVRRQ\t'), '6E');
  assert.equal(checksum('#CEPRD\t0000\t40\t'), '6E');
  assert.equal(checksum('#CEPRD\t3000\t40\t'), '6D');
  assert.equal(checksum('#CEPWR\t0300\t04\tDEADBEEF\t'), '77');
});

test('frame appends checksum and CRLF', () => {
  assert.equal(frame('#CEPSR\t00\t'), '#CEPSR\t00\t74\r\n');
});

test('verifyChecksum checks the two hex chars after the last tab', () => {
  assert.equal(verifyChecksum('#CEPSD\t00\t62'), true);
  assert.equal(verifyChecksum('#CEPSD\t00\t63'), false);
  assert.equal(verifyChecksum('#CEPSD\t00\t'), false);
});

test('parseReply decodes a CEPDT data line', () => {
  const body = '#CEPDT\t3000\t04\tDEADBEEF\t';
  const r = parseReply(body + checksum(body));
  assert.equal(r.type, 'CEPDT');
  assert.equal(r.addr, 0x3000);
  assert.equal(r.len, 4);
  assert.deepEqual(Array.from(r.data), [0xde, 0xad, 0xbe, 0xef]);
});

test('parseReply flags a CEPDT line with a bad checksum', () => {
  const r = parseReply('#CEPDT\t3000\t04\tDEADBEEF\t00');
  assert.equal(r.type, 'BADSUM');
});

test('parseReply decodes simple replies and the version line', () => {
  assert.equal(parseReply('#CMDOK').type, 'CMDOK');
  assert.equal(parseReply('#CMDSM').type, 'CMDSM');
  assert.deepEqual(parseReply('#CEPSD\t00\t62'), { type: 'CEPSD', status: '00' });
  assert.deepEqual(parseReply('#CVRDQ\t3.52\t1A'), { type: 'CVRDQ', version: 3.52 });
  assert.deepEqual(parseReply('#CVRDQ\t--.--\t1A'), { type: 'CVRDQ', version: null });
  assert.equal(parseReply('$PMTK001,622,3*36').type, 'PMTK');
  assert.equal(parseReply('garbage').type, 'UNKNOWN');
});

// ---------- default image ----------
test('default image matches the YCE46 factory file (model code, names, size)', () => {
  const img = RadioImage.default();
  assert.equal(img.bytes.length, IMAGE_SIZE);
  assert.equal(img.modelCode(), MODEL_CODE);
  assert.equal(img.footerModelCode(), MODEL_CODE);
  assert.deepEqual(img.groupNames(), ['GROUP1','GROUP2','GROUP3','GROUP4','GROUP5','GROUP6','GROUP7','GROUP8','GROUP9']);
  assert.deepEqual(img.weatherTags(), ['WX01','WX02','WX03','WX04','WX05','WX06','WX07','WX08','WX09','WX10']);
  let nonFF = 0; for (const b of img.bytes) if (b !== 0xff) nonFF++;
  assert.equal(nonFF, 1477);
  assert.deepEqual(img.channels(), []);
});

// ---------- BCD / entry layout ----------
test('setChannelSlot writes the YCE46 entry layout and bitmaps', () => {
  const img = RadioImage.default();
  img.setChannelSlot(0, { address: 1, group: 3, freq: '118000', tag: 'KBDU TWR', enable: true, freqEnable: true, posEnable: false, scan: false, shift: 0 });
  const e = img.bytes.subarray(0x3000, 0x3030);
  assert.deepEqual(Array.from(e.subarray(16, 22)), [0x00, 0x01, 0x03, 0x11, 0x80, 0x00]);
  assert.equal(Buffer.from(e.subarray(32, 46)).toString('latin1'), 'KBDU TWR\xff\xff\xff\xff\xff\xff');
  assert.equal(e[31], 0xff);            // no position -> NS/EW undefined
  assert.equal(e[47], 0);               // shift off
  assert.equal(img.bytes[5632] & 0x80, 0x80);       // enable bit, slot 0
  assert.equal(img.bytes[5632 + 64 * 3] & 0x80, 0x80); // group-3 bitmap
  assert.equal(img.bytes[5632 + 64 * 1] & 0x80, 0);    // not in group 1
  assert.equal(img.bytes[5376] & 0x80, 0x80);       // freqEnable
  assert.equal(img.bytes[5440] & 0x80, 0);          // posEnable
  assert.equal(img.bytes[368] & 0x80, 0);           // scan off
});

test('channel round-trips through the image', () => {
  const img = RadioImage.default();
  const ch = { address: 7, group: 2, freq: '122800', tag: 'KLMO CTAF', enable: true, freqEnable: true, posEnable: false, scan: true, shift: 0 };
  img.setChannelSlot(5, ch);
  const back = img.getChannelSlot(5);
  assert.equal(back.slot, 5);
  for (const k of Object.keys(ch)) assert.equal(back[k], ch[k], k);
  assert.equal(back.lat, '');
  assert.equal(back.trueCourse, '');
});

test('a slot with a non-digit nibble in the frequency is rejected', () => {
  const img = RadioImage.default();
  img.bytes[0x3000 + 19] = 0x1a;
  assert.throws(() => img.getChannelSlot(0), /Frequency/);
});

// ---------- sort order ----------
test('compareTag follows YCE46: space < digits < letters < marks, prefix first', () => {
  const sorted = ['B', 'A1', '2', 'A', ' Z', 'A-', 'A*', 'AB'].sort(compareTag);
  assert.deepEqual(sorted, [' Z', '2', 'A', 'A1', 'AB', 'A*', 'A-', 'B']);
});

test('compareTag is case-insensitive', () => {
  assert.equal(compareTag('kbdu', 'KBDU'), 0);
});

// ---------- apply ----------
test('applyChannels sorts by tag, assigns addresses, and compacts', () => {
  const img = RadioImage.default();
  img.applyChannels([
    { group: 1, freq: '121500', tag: 'GUARD' },
    { group: 1, freq: '118000', tag: 'BJC TWR' },
  ]);
  const chs = img.channels();
  assert.deepEqual(chs.map(c => [c.slot, c.address, c.tag]), [[0, 1, 'BJC TWR'], [1, 2, 'GUARD']]);
  // delete GUARD, add a new one: existing keeps address 1, new gets lowest free (2)
  img.applyChannels([chs[0], { group: 4, freq: '122200', tag: 'FSS' }]);
  const after = img.channels();
  assert.deepEqual(after.map(c => [c.slot, c.address, c.tag]), [[0, 1, 'BJC TWR'], [1, 2, 'FSS']]);
  // slot 2 is cleared back to the factory pattern: enable bit off, all 48 bytes FF
  // (YCE46 leaves a 0x00 group byte behind after a delete; the radio accepts either,
  // and FF keeps untouched slots out of the write diff)
  assert.equal(img.bytes[5632] & 0x20, 0);
  assert.ok(img.bytes.subarray(0x3000 + 96, 0x3000 + 144).every((b) => b === 0xff));
});

test('applyChannels refuses more than 400 channels', () => {
  const img = RadioImage.default();
  const many = Array.from({ length: 401 }, (_, i) => ({ group: 1, freq: '118000', tag: 'CH' + i }));
  assert.throws(() => img.applyChannels(many), /400/);
});

test('applyChannels rewrites flip-flop copies by address and drops deleted ones', () => {
  const img = RadioImage.default();
  img.applyChannels([{ group: 1, freq: '118000', tag: 'A' }, { group: 1, freq: '119000', tag: 'B' }]);
  const [a, b] = img.channels();
  // simulate the radio having recalled B then A (flip-flop 1 = B, 2 = A) and last memory = A
  img.bytes.set(img.bytes.subarray(0x3000 + 48 * b.slot, 0x3000 + 48 * b.slot + 48), 2624);
  img.bytes.set(img.bytes.subarray(0x3000 + 48 * a.slot, 0x3000 + 48 * a.slot + 48), 2624 + 64);
  img.bytes.set(img.bytes.subarray(0x3000 + 48 * a.slot, 0x3000 + 48 * a.slot + 48), 2560);
  // rename A and delete B
  img.applyChannels([{ ...a, tag: 'ALPHA' }]);
  const ff1 = img.readEntry(2624), ff2 = img.readEntry(2624 + 64), last = img.readEntry(2560);
  assert.equal(ff1.tag, 'ALPHA'); assert.equal(ff1.address, a.address);
  assert.equal(ff2.address, 0xffff);
  assert.equal(last.tag, 'ALPHA');
});

// ---------- validation ----------
test('validateFrequency enforces band edges and 25 kHz / 8.33 kHz steps', () => {
  assert.equal(validateFrequency('118000'), null);
  assert.equal(validateFrequency('136975'), null);
  assert.equal(validateFrequency('108000'), null);            // NAV band OK
  assert.match(validateFrequency('137000'), /range/);
  assert.match(validateFrequency('118010'), /step/);
  assert.equal(validateFrequency('118010', { allow833: true }), null);
  assert.match(validateFrequency('118.0'), /6 digits/);
  assert.match(validateFrequency(''), /6 digits/);
});

test('validateTag allows letters, digits and the YCE46 mark set up to 14 chars', () => {
  assert.equal(validateTag('KBDU TWR'), null);
  assert.equal(validateTag('A/B-C.D[1]*+,&'), null);
  assert.match(validateTag(''), /empty/);
  assert.match(validateTag('123456789012345'), /14/);
  assert.match(validateTag('BAD#'), /character/);
});

// ---------- CSV ----------
test('CSV round-trips group, frequency (MHz) and tag', () => {
  const list = [{ group: 1, freq: '118000', tag: 'BJC TWR' }, { group: 9, freq: '121500', tag: 'GUARD, X' }];
  const csv = channelsToCsv(list);
  assert.equal(csv.split('\n')[0], 'group,frequency,tag');
  assert.deepEqual(csvToChannels(csv), list);
});

test('csvToChannels reports the line of a bad row', () => {
  assert.throws(() => csvToChannels('group,frequency,tag\n1,118.000,OK\n7,999.000,BAD'), /line 3/);
});

// ---------- write regions ----------
test('write regions stay inside the memory-book areas and chunk to 64 bytes', () => {
  const total = WRITE_REGIONS.reduce((n, r) => n + r.len, 0);
  assert.equal(total, 20774);
  for (const r of WRITE_REGIONS) assert.ok(r.addr >= 0x0102 && r.addr + r.len <= 0x7B00);
  const chunks = chunkRegions(WRITE_REGIONS);
  assert.equal(chunks.length, 326);
  assert.ok(chunks.every(c => c.len > 0 && c.len <= 64));
  assert.deepEqual(chunks[0], { addr: 0x0170, len: 50 });
});

test('diffChunks keeps only chunks whose bytes changed', () => {
  const a = RadioImage.default(), b = RadioImage.default();
  b.bytes[0x3000 + 40] = 0x41;
  b.bytes[0x0300] = 0x5a;
  const d = diffChunks(a.bytes, b.bytes, WRITE_REGIONS);
  assert.deepEqual(d.map(c => c.addr), [0x0300, 0x3000]);
});

test('mhzToFreq accepts MHz text, whole MHz, or raw kHz digits', async () => {
  const { mhzToFreq } = await import('../sections/tools/fta850/fta850.js');
  assert.equal(mhzToFreq('118.000'), '118000');
  assert.equal(mhzToFreq('121.5'), '121500');
  assert.equal(mhzToFreq('118'), '118000');
  assert.equal(mhzToFreq('118000'), '118000');
  assert.equal(mhzToFreq('11.8'), '11.8');
});
