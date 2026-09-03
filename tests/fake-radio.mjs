// A fake FTA-850 in CP mode: implements the transport interface used by Radio
// and answers the same wire protocol YCE46 speaks. Test utility only.
import { checksum, frame, hexToBytes, bytesToHex, IMAGE_SIZE } from '../sections/tools/fta850/fta850.js';

export class FakeRadio {
  constructor({ image, firmware = '3.52', pieceSize = 5, faults = {} } = {}) {
    this.image = image ?? new Uint8Array(IMAGE_SIZE).fill(0xff);
    this.firmware = firmware;
    this.pieceSize = pieceSize;
    this.faults = { dropSync: 0, corruptRead: 0, silentAfter: Infinity, busyStatus: 0, ...faults };
    this.received = [];
    this.outQueue = [];
    this.waiters = [];
    this.inbuf = '';
    this.closed = false;
  }

  // transport interface
  async write(bytes) {
    this.inbuf += String.fromCharCode(...bytes);
    let i;
    while ((i = this.inbuf.indexOf('\r\n')) >= 0) {
      const line = this.inbuf.slice(0, i);
      this.inbuf = this.inbuf.slice(i + 2);
      this.received.push(line);
      this.handle(line);
    }
  }

  async read() {
    if (this.outQueue.length) return this.outQueue.shift();
    if (this.closed) return null;
    return new Promise((resolve) => this.waiters.push(resolve));
  }

  async close() {
    this.closed = true;
    for (const w of this.waiters.splice(0)) w(null);
  }

  reply(text) {
    const bytes = new Uint8Array([...text].map((c) => c.charCodeAt(0)));
    for (let i = 0; i < bytes.length; i += this.pieceSize) {
      const piece = bytes.subarray(i, i + this.pieceSize);
      const w = this.waiters.shift();
      if (w) w(piece); else this.outQueue.push(piece);
    }
  }

  handle(line) {
    if (line.endsWith('ACMD:002')) return this.reply('OK\r\n');
    if (line === '#CMDSY') {
      if (this.faults.dropSync > 0) { this.faults.dropSync--; return; }
      return this.reply('#CMDOK\r\n');
    }
    if (line === '#CMDOK') return; // host ack
    if (line.startsWith('#CVRRQ')) return this.reply(frame(`#CVRDQ\t${this.firmware}\t`));
    if (line.startsWith('#CEPSR')) {
      if (this.faults.busyStatus > 0) { this.faults.busyStatus--; return this.reply(frame('#CEPSD\t01\t')); }
      return this.reply(frame('#CEPSD\t00\t'));
    }
    if (line.startsWith('#CEPRD')) {
      const [, a, l, ck] = line.split('\t');
      if (checksum(line.slice(0, line.lastIndexOf('\t') + 1)) !== ck) return this.reply('#CMDSM\r\n');
      const addr = parseInt(a, 16), len = parseInt(l, 16);
      if (addr >= this.faults.silentAfter) return;
      let hex = bytesToHex(this.image.subarray(addr, addr + len));
      let body = `#CEPDT\t${a}\t${l}\t${hex}\t`;
      let out = frame(body);
      if (this.faults.corruptRead > 0) { this.faults.corruptRead--; out = body + '00\r\n'; }
      return this.reply(out);
    }
    if (line.startsWith('#CEPWR')) {
      const [, a, l, hex, ck] = line.split('\t');
      if (checksum(line.slice(0, line.lastIndexOf('\t') + 1)) !== ck) return this.reply('#CMDSM\r\n');
      const addr = parseInt(a, 16), len = parseInt(l, 16);
      const data = hexToBytes(hex);
      if (data.length !== len || addr + len > IMAGE_SIZE) return this.reply('#CMDER\r\n');
      this.image.set(data, addr);
      return this.reply('#CMDOK\r\n');
    }
    this.reply('#CMDUN\r\n');
  }
}
