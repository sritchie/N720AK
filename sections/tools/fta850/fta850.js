// Yaesu FTA-850 memory-book codec and CP-mode serial protocol.
// Pure module: no DOM, no WebSerial. Everything here was derived from the
// behaviour of Yaesu's YCE46 programmer; see the notes in sys-23.

export const IMAGE_SIZE = 32768;
export const MODEL_CODE = 0x0352;
export const MAX_CHANNELS = 400;
export const TAG_LEN = 14;
export const GROUP_NAME_LEN = 10;
export const GROUP_COUNT = 9;
export const USB_VENDOR_ID = 0x26aa;
export const USB_PRODUCT_ID = 0x0024;
export const MIN_FIRMWARE = 2.01;

// Byte offsets inside the 32 KiB image (decimal, as in YCE46's memory map).
export const OFF = Object.freeze({
  model: 0x0100, footerModel: 0x7ffe,
  enable833: 299,
  scanBits: 368,
  groupNames: 768,           // 9 x 16 bytes, 10-char names
  weather: 1280,             // 10 x 16 bytes, 14-char tags
  lastMemory: 2560,          // one 48-byte entry copy
  flipFlop: 2624,            // 9 x 64-byte banks, each a 48-byte entry copy
  freqEnableBits: 5376,
  posEnableBits: 5440,
  enableBits: 5632,          // + 64*g for the per-group bitmaps, g = 1..9
  memoryBook: 12288,         // 400 x 48 bytes
  entrySize: 48,
});

// Regions the programmer writes: exactly the bytes the memory-book editor can
// change. All of them lie inside YCE46's own "Program to Radio" write table.
export const WRITE_REGIONS = Object.freeze([
  { addr: 0x0170, len: 50 },    // scan bits
  { addr: 0x0300, len: 144 },   // group names
  { addr: 0x0a00, len: 640 },   // last memory + flip-flop banks
  { addr: 0x1500, len: 50 },    // frequency-enable bits
  { addr: 0x1540, len: 50 },    // position-enable bits
  { addr: 0x1600, len: 640 },   // enable bits + per-group bitmaps
  { addr: 0x3000, len: 19200 }, // memory book
]);

// ---------------------------------------------------------------- framing

export function checksum(str) {
  let c = 0;
  for (let i = 0; i < str.length; i++) c ^= str.charCodeAt(i);
  return (c & 0xff).toString(16).toUpperCase().padStart(2, '0');
}

export function frame(body) {
  return body + checksum(body) + '\r\n';
}

export function verifyChecksum(line) {
  const t = line.lastIndexOf('\t');
  if (t < 0 || line.length !== t + 3) return false;
  return checksum(line.slice(0, t + 1)) === line.slice(t + 1).toUpperCase();
}

export function hexToBytes(hex) {
  if (hex.length % 2) throw new Error('odd hex length');
  const out = new Uint8Array(hex.length / 2);
  for (let i = 0; i < out.length; i++) {
    const v = parseInt(hex.substr(i * 2, 2), 16);
    if (Number.isNaN(v)) throw new Error('bad hex');
    out[i] = v;
  }
  return out;
}

export function bytesToHex(bytes) {
  let s = '';
  for (const b of bytes) s += b.toString(16).toUpperCase().padStart(2, '0');
  return s;
}

export function parseReply(line) {
  if (line.startsWith('#CMDOK')) return { type: 'CMDOK' };
  if (line.startsWith('#CMDER')) return { type: 'CMDER' };
  if (line.startsWith('#CMDUN')) return { type: 'CMDUN' };
  if (line.startsWith('#CMDSM')) return { type: 'CMDSM' };
  if (line.startsWith('#CEPSD')) {
    const f = line.split('\t');
    if (f.length !== 3 || !verifyChecksum(line)) return { type: 'BADSUM', line };
    return { type: 'CEPSD', status: f[1] };
  }
  if (line.startsWith('#CEPDT')) {
    const f = line.split('\t');
    if (f.length !== 5 || !verifyChecksum(line)) return { type: 'BADSUM', line };
    let data;
    try { data = hexToBytes(f[3]); } catch { return { type: 'BADSUM', line }; }
    return { type: 'CEPDT', addr: parseInt(f[1], 16), len: parseInt(f[2], 16), data };
  }
  if (line.startsWith('#CVRDQ')) {
    const v = line.split('\t')[1] ?? '';
    const n = v === '--.--' ? NaN : Number(v.replace(',', '.'));
    return { type: 'CVRDQ', version: Number.isFinite(n) ? n : null };
  }
  if (line === 'OK') return { type: 'OK' };
  if (line === 'ERROR') return { type: 'ERROR' };
  if (line.startsWith('$PMTK')) return { type: 'PMTK', line };
  return { type: 'UNKNOWN', line };
}

export const CMD = Object.freeze({
  wake: ['P', '0', 'ACMD:002\r\n'],
  sync: '#CMDSY\r\n',
  ack: '#CMDOK\r\n',
  status: frame('#CEPSR\t00\t'),
  version: frame('#CVRRQ\t'),
  read: (addr, len) => frame(`#CEPRD\t${hex4(addr)}\t${hex2(len)}\t`),
  write: (addr, bytes) => frame(`#CEPWR\t${hex4(addr)}\t${hex2(bytes.length)}\t${bytesToHex(bytes)}\t`),
});

function hex4(n) { return n.toString(16).toUpperCase().padStart(4, '0'); }
function hex2(n) { return n.toString(16).toUpperCase().padStart(2, '0'); }

// ---------------------------------------------------------------- default image

// Every non-0xFF run in Yaesu's FTA-850_0352.ini factory image.
const DEFAULT_RUNS = [
  [0x0100, '03520100000000010001'],
  [0x010e, '000005070305010101030001000105'],
  [0x011f, '0101010100030100'],
  [0x012a, '0001000000'],
  [0x0130, '0002020000000000'],
  [0x013e, '00000101004000000000010003'],
  [0x0150, '0009'],
  [0x0160, '00000001010000'],
  [0x0170, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],
  [0x01ae, '0000'],
  [0x01c0, '4654412d383530'],
  [0x01d0, '41413030334e'],
  [0x01da, '00'],
  [0x01dc, '11'],
  [0x01df, '11'],
  [0x0200, '1f00005c115b00277f78a090b4e602c81f00005c115b00277f78a090b4e602c87f78a090b4e602'],
  [0x0230, 'c81ee6c803e6c803e6c803'],
  [0x0240, '0000d70200'],
  [0x0250, '00900098005a00c000c00060d702'],
  [0x0260, '00a000a3008500bb00bb0085d702'],
  [0x0270, '000000000000000000000000000000000000000005101010050000000000000000000000'],
  [0x02a0, '000000000000000000000000000505051010101015202020151010101010050000000000'],
  [0x02d0, '000000000000000505050505101515152020202025303030252020202020151010101005'],
  [0x0300, '47524f555031'],
  [0x0310, '47524f555032'],
  [0x0320, '47524f555033'],
  [0x0330, '47524f555034'],
  [0x0340, '47524f555035'],
  [0x0350, '47524f555036'],
  [0x0360, '47524f555037'],
  [0x0370, '47524f555038'],
  [0x0380, '47524f555039'],
  [0x03a0, '1414191e28323c4614141e28323c485500050a0f151a1f2000050a0f151a'],
  [0x03c0, '00010203040507090b0d0f1215181c20252a30363d454e58636f7c8a9aacc0'],
  [0x03e0, '00112233445566778899aabbccddee'],
  [0x0400, '0000'],
  [0x0403, '00c007'],
  [0x0500, '57583031'],
  [0x0510, '57583032'],
  [0x0520, '57583033'],
  [0x0530, '57583034'],
  [0x0540, '57583035'],
  [0x0550, '57583036'],
  [0x0560, '57583037'],
  [0x0570, '57583038'],
  [0x0580, '57583039'],
  [0x0590, '57583130'],
  [0x0712, '00118000'],
  [0x072f, '00'],
  [0x1500, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],
  [0x1540, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],
  [0x1600, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],
  [0x1640, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],
  [0x1680, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],
  [0x16c0, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],
  [0x1700, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],
  [0x1740, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],
  [0x1780, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],
  [0x17c0, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],
  [0x1800, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],
  [0x1840, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],
  [0x1900, '0000000000'],
  [0x1910, '0000000000'],
  [0x1920, '0000000000'],
  [0x1930, '0000000000'],
  [0x1940, '0000000000'],
  [0x1950, '0000000000'],
  [0x1960, '0000000000'],
  [0x1970, '0000000000'],
  [0x1980, '0000000000'],
  [0x1990, '0000000000'],
  [0x7c00, '7f'],
  [0x7c04, '003e194000000002'],
  [0x7c10, '3333333301367e4000000002'],
  [0x7c20, '7f'],
  [0x7c24, '003e194000000001'],
  [0x7c30, '4ccccccc01367e4000000001'],
  [0x7c40, '2ccccccc00ba4bc000000001'],
  [0x7c50, '19999999003e194000000001'],
  [0x7c60, '0ccccccc003e194000000001'],
  [0x7c70, '0000000100000000'],
  [0x7c80, '017000000100000001c000000170000000003e80'],
  [0x7ca0, '0000700000004000'],
  [0x7cb0, '00000002'],
  [0x7cc0, '0000200000001900000002000000040000000800'],
  [0x7ce0, '0000040000000080000000080000000700000006'],
  [0x7d00, '0791650af0dd35ed0791650af8cfbc1c0f155043'],
  [0x7d20, '074bded7f1684252074bded7f94af10f0e7a6c6a'],
  [0x7d40, '0197bd48032f7a900197bd48fc54f348054c1799'],
  [0x7d60, '014174ab0282e957014174abfcb2cd8306475fcf'],
  [0x7d80, '0773a820f118afbf0773a820f9069c5e0ed53ce0'],
  [0x7da0, '035e56c9fe2bda46035e56c90143526d0143526d'],
  [0x7dc0, '0186ed24030dda470186ed24fb353bfd06af0f74'],
  [0x7de0, '017cbf7202f97ee4017cbf72fb8a7fb90682827e'],
  [0x7ffe, '0352'],
];

export function defaultImage() {
  const b = new Uint8Array(IMAGE_SIZE).fill(0xff);
  for (const [off, hex] of DEFAULT_RUNS) b.set(hexToBytes(hex), off);
  return b;
}

// ---------------------------------------------------------------- text rules

const MARKS = [' ', '*', '+', ',', '/', '&', '-', '[', ']', '.'];
const isDigit = (c) => c >= '0' && c <= '9';
const isLetter = (c) => (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z');

export function compareChar(x, y) {
  if (x === y) return 0;
  if (x === ' ') return -1;
  if (y === ' ') return 1;
  if (isDigit(x)) return isDigit(y) ? (x < y ? -1 : 1) : -1;
  if (isDigit(y)) return 1;
  if (isLetter(x)) return isLetter(y) ? (x < y ? -1 : 1) : -1;
  if (isLetter(y)) return 1;
  const a = MARKS.indexOf(x), b = MARKS.indexOf(y);
  if (a >= 0) return a > b ? 1 : -1;
  if (b >= 0) return 1;
  return x < y ? -1 : 1;
}

export function compareTag(a, b) {
  const x = a.toUpperCase(), y = b.toUpperCase();
  if (x === y) return 0;
  for (let i = 0; i < x.length && i < y.length; i++) {
    const c = compareChar(x[i], y[i]);
    if (c !== 0) return c;
  }
  return x.length > y.length ? 1 : -1;
}

export function validateTag(tag) {
  if (!tag) return 'tag is empty';
  if (tag.length > TAG_LEN) return `tag is longer than ${TAG_LEN} characters`;
  for (const c of tag) {
    if (!(isDigit(c) || isLetter(c) || MARKS.includes(c))) return `character "${c}" is not allowed in a tag`;
  }
  return null;
}

export function validateGroupName(name) {
  if (!name) return 'group name is empty';
  if (name.length > GROUP_NAME_LEN) return `group name is longer than ${GROUP_NAME_LEN} characters`;
  for (const c of name) {
    if (!(isDigit(c) || isLetter(c) || MARKS.includes(c))) return `character "${c}" is not allowed in a group name`;
  }
  return null;
}

const STEP25 = [0, 25, 50, 75];
const STEP833 = [5, 10, 15, 30, 35, 40, 55, 60, 65, 80, 85, 90];

export function validateFrequency(freq, { allow833 = false } = {}) {
  if (!/^\d{6}$/.test(freq ?? '')) return 'frequency must be 6 digits (kHz), e.g. 118000';
  const n = Number(freq);
  if (!(n >= 108000 && n < 137000)) return 'frequency out of range (108.000-136.975 MHz)';
  const r = n % 100;
  if (STEP25.includes(r)) return null;
  if (allow833 && STEP833.includes(r)) return null;
  return allow833 ? 'frequency is not a 25 kHz or 8.33 kHz channel' : 'frequency is not a 25 kHz step (enable 8.33 kHz on the radio for 8.33 channels)';
}

export function freqToMHz(freq) {
  return freq ? `${freq.slice(0, 3)}.${freq.slice(3)}` : '';
}

export function mhzToFreq(text) {
  const t = String(text ?? '').trim();
  if (/^\d{6}$/.test(t)) return t;
  if (/^\d{3}$/.test(t)) return t + '000';
  const m = /^(\d{3})\.(\d{1,3})$/.exec(t);
  if (!m) return t;
  return m[1] + m[2].padEnd(3, '0');
}

// ---------------------------------------------------------------- image

// A cleared slot is all 0xFF, i.e. the factory pattern. (YCE46 leaves group=0
// behind after a delete; the radio treats either as empty since the enable bit
// is off, and 0xFF keeps untouched slots out of the write diff.)
const EMPTY_ENTRY = Object.freeze({
  address: 0xffff, group: 0xff, freq: '', lat: '', lon: '', nsew: 0xff, tag: '', trueCourse: '', shift: 0xff,
});

export class RadioImage {
  constructor(bytes) {
    if (!(bytes instanceof Uint8Array) || bytes.length !== IMAGE_SIZE) throw new Error(`image must be ${IMAGE_SIZE} bytes`);
    this.bytes = bytes;
  }

  static default() { return new RadioImage(defaultImage()); }
  clone() { return new RadioImage(new Uint8Array(this.bytes)); }

  modelCode() { return (this.bytes[OFF.model] << 8) | this.bytes[OFF.model + 1]; }
  footerModelCode() { return (this.bytes[OFF.footerModel] << 8) | this.bytes[OFF.footerModel + 1]; }
  is833Enabled() { return this.bytes[OFF.enable833] === 1; }

  // -- primitives (ports of YCE46 DataManager helpers)

  getString(pos, max) {
    let end = pos;
    while (end < pos + max && this.bytes[end] !== 0xff) end++;
    let s = '';
    for (let i = pos; i < end; i++) s += String.fromCharCode(this.bytes[i]);
    return s.replace(/\0+$/, '');
  }

  setString(pos, size, str) {
    this.bytes.fill(0xff, pos, pos + size);
    for (let i = 0; i < str.length && i < size; i++) this.bytes[pos + i] = str.charCodeAt(i) & 0xff;
  }

  getBCD(pos, size) {
    const hex = bytesToHex(this.bytes.subarray(pos, pos + size));
    if (/^\d+$/.test(hex)) return hex;
    if (/^F+$/.test(hex)) return '';
    throw new Error(`Frequency data error at ${pos}: ${hex}`);
  }

  setBCD(pos, size, value) {
    let v = value || '';
    if (!v) v = 'F'.repeat(size * 2);
    if (v.length % 2) v += '0';
    if (v.length !== size * 2 || !/^[0-9A-Fa-f]+$/.test(v)) throw new Error(`invalid BCD value "${value}" for ${size} bytes`);
    this.bytes.set(hexToBytes(v), pos);
  }

  getBool(pos, idx) { return (this.bytes[pos + (idx >> 3)] & (0x80 >> (idx & 7))) !== 0; }

  setBool(pos, idx, on) {
    const i = pos + (idx >> 3), m = 0x80 >> (idx & 7);
    if (on) this.bytes[i] |= m; else this.bytes[i] &= ~m & 0xff;
  }

  // -- 48-byte entries (memory book slots, last memory, flip-flop banks)

  readEntry(pos) {
    const b = this.bytes;
    return {
      address: (b[pos + 16] << 8) | b[pos + 17],
      group: b[pos + 18],
      freq: this.getBCD(pos + 19, 3),
      lat: this.getBCD(pos + 22, 4),
      lon: this.getBCD(pos + 26, 5),
      nsew: b[pos + 31],
      tag: this.getString(pos + 32, TAG_LEN),
      trueCourse: this.getBCD(pos + 13, 3),
      shift: b[pos + 47],
    };
  }

  writeEntry(pos, e) {
    const b = this.bytes;
    const addr = e.address ?? 0xffff;
    this.setBCD(pos + 13, 3, e.trueCourse ?? '');
    b[pos + 16] = (addr >> 8) & 0xff; b[pos + 17] = addr & 0xff;
    b[pos + 18] = e.group ?? 0;
    this.setBCD(pos + 19, 3, e.freq ?? '');
    this.setBCD(pos + 22, 4, e.lat ?? '');
    this.setBCD(pos + 26, 5, e.lon ?? '');
    b[pos + 31] = e.nsew ?? 0xff;
    this.setString(pos + 32, TAG_LEN, e.tag ?? '');
    b[pos + 47] = e.shift ?? 0xff;
  }

  getChannelSlot(slot) {
    const e = this.readEntry(OFF.memoryBook + OFF.entrySize * slot);
    return {
      slot, ...e,
      enable: this.getBool(OFF.enableBits, slot),
      freqEnable: this.getBool(OFF.freqEnableBits, slot),
      posEnable: this.getBool(OFF.posEnableBits, slot),
      scan: this.getBool(OFF.scanBits, slot),
    };
  }

  setChannelSlot(slot, ch) {
    if (slot < 0 || slot >= MAX_CHANNELS) throw new Error(`invalid slot ${slot}`);
    this.writeEntry(OFF.memoryBook + OFF.entrySize * slot, ch);
    this.setBool(OFF.enableBits, slot, !!ch.enable);
    for (let g = 1; g <= GROUP_COUNT; g++) this.setBool(OFF.enableBits + 64 * g, slot, g === ch.group);
    this.setBool(OFF.freqEnableBits, slot, !!ch.freqEnable);
    this.setBool(OFF.posEnableBits, slot, !!ch.posEnable);
    this.setBool(OFF.scanBits, slot, !!ch.scan);
  }

  channels() {
    const out = [];
    for (let s = 0; s < MAX_CHANNELS; s++) if (this.getBool(OFF.enableBits, s)) out.push(this.getChannelSlot(s));
    return out;
  }

  // Replace the whole memory book with `list`, the way YCE46 does after every
  // edit: sorted by tag, addresses kept for surviving entries and lowest-free
  // for new ones, empty slots cleared, recall copies refreshed by address.
  applyChannels(list) {
    if (list.length > MAX_CHANNELS) throw new Error(`memory book holds at most ${MAX_CHANNELS} channels`);
    const oldByAddr = new Map(this.channels().map((c) => [c.address, c]));
    const entries = list.map((c, i) => ({
      ...EMPTY_ENTRY, ...c,
      tag: c.tag ?? '',
      origIndex: c.slot ?? MAX_CHANNELS + i,
    }));
    entries.sort((a, b) => compareTag(a.tag, b.tag) || a.origIndex - b.origIndex);
    const assigned = new Set();
    for (const e of entries) {
      const keep = e.address != null && e.address !== 0xffff && oldByAddr.has(e.address) && !assigned.has(e.address);
      if (keep) assigned.add(e.address); else e.address = null;
    }
    let next = 1;
    for (const e of entries) {
      if (e.address != null) continue;
      while (assigned.has(next)) next++;
      e.address = next; assigned.add(next);
    }
    const newByAddr = new Map();
    entries.forEach((e, slot) => {
      const ch = {
        ...e, slot, enable: true,
        freqEnable: !!e.freq,
        posEnable: e.posEnable ?? !!(e.lat && e.lon && e.nsew !== 0xff),
        scan: !!e.scan,
        shift: e.shift === 0xff ? 0 : e.shift,
      };
      this.setChannelSlot(slot, ch);
      newByAddr.set(e.address, ch);
    });
    for (let slot = entries.length; slot < MAX_CHANNELS; slot++) this.setChannelSlot(slot, { ...EMPTY_ENTRY, enable: false });

    const last = this.readEntry(OFF.lastMemory);
    if (last.address !== 0xffff) {
      if (newByAddr.has(last.address)) this.writeEntry(OFF.lastMemory, newByAddr.get(last.address));
      else if (oldByAddr.has(last.address)) this.writeEntry(OFF.lastMemory, EMPTY_ENTRY);
    }
    const kept = [];
    for (let k = 0; k < 9; k++) {
      const ff = this.readEntry(OFF.flipFlop + 64 * k);
      if (ff.address !== 0xffff && newByAddr.has(ff.address)) kept.push(newByAddr.get(ff.address));
    }
    for (let k = 0; k < 9; k++) this.writeEntry(OFF.flipFlop + 64 * k, kept[k] ?? EMPTY_ENTRY);
  }

  groupNames() {
    const out = [];
    for (let g = 1; g <= GROUP_COUNT; g++) out.push(this.getString(OFF.groupNames + 16 * (g - 1), GROUP_NAME_LEN));
    return out;
  }

  setGroupName(g, name) {
    if (g < 1 || g > GROUP_COUNT) throw new Error(`invalid group ${g}`);
    const err = validateGroupName(name);
    if (err) throw new Error(err);
    this.setString(OFF.groupNames + 16 * (g - 1), GROUP_NAME_LEN, name);
  }

  weatherTags() {
    const out = [];
    for (let i = 0; i < 10; i++) out.push(this.getString(OFF.weather + 16 * i, TAG_LEN));
    return out;
  }
}

// ---------------------------------------------------------------- CSV

function csvEscape(s) {
  return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

export function channelsToCsv(list) {
  const lines = ['group,frequency,tag'];
  for (const c of list) lines.push(`${c.group},${freqToMHz(c.freq)},${csvEscape(c.tag)}`);
  return lines.join('\n') + '\n';
}

function parseCsvRows(text) {
  const rows = []; let row = [], field = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else q = false; }
      else field += c;
    } else if (c === '"') q = true;
    else if (c === ',') { row.push(field); field = ''; }
    else if (c === '\n' || c === '\r') {
      if (c === '\r' && text[i + 1] === '\n') i++;
      row.push(field); rows.push(row); row = []; field = '';
    } else field += c;
  }
  if (field !== '' || row.length) { row.push(field); rows.push(row); }
  return rows;
}

export function csvToChannels(text, { allow833 = false } = {}) {
  const rows = parseCsvRows(text);
  const out = [];
  rows.forEach((r, i) => {
    const line = i + 1;
    if (r.every((f) => f.trim() === '')) return;
    if (i === 0 && /^group$/i.test(r[0].trim())) return;
    if (r.length < 3) throw new Error(`line ${line}: expected group,frequency,tag`);
    const group = Number(r[0].trim());
    if (!Number.isInteger(group) || group < 1 || group > GROUP_COUNT) throw new Error(`line ${line}: group must be 1-${GROUP_COUNT}`);
    const freq = mhzToFreq(r[1]);
    const fe = validateFrequency(freq, { allow833 });
    if (fe) throw new Error(`line ${line}: ${fe}`);
    const tag = r.slice(2).join(',').trim().toUpperCase();
    const te = validateTag(tag);
    if (te) throw new Error(`line ${line}: ${te}`);
    out.push({ group, freq, tag });
  });
  return out;
}

// ---------------------------------------------------------------- regions

export function chunkRegions(regions, size = 64) {
  const out = [];
  for (const r of regions) for (let a = r.addr; a < r.addr + r.len; a += size) out.push({ addr: a, len: Math.min(size, r.addr + r.len - a) });
  return out;
}

export function diffChunks(before, after, regions, size = 64) {
  return chunkRegions(regions, size).filter((c) => {
    for (let i = c.addr; i < c.addr + c.len; i++) if (before[i] !== after[i]) return true;
    return false;
  });
}

// ---------------------------------------------------------------- protocol

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const encode = (s) => new Uint8Array([...s].map((c) => c.charCodeAt(0)));

const OK_TYPES = new Set(['CMDOK']);
const ERR_TYPES = new Set(['CMDER', 'CMDUN', 'CMDSM', 'BADSUM']);

/**
 * Drives an FTA-850 in CP mode over a byte transport:
 *   transport.write(Uint8Array) -> Promise, transport.read() -> Promise<Uint8Array|null>,
 *   transport.close() -> Promise.  Replies are line based (CRLF).
 */
export class Radio {
  constructor(transport, { timeout = 2000, retries = 5, retryInterval = 20, log = () => {} } = {}) {
    this.t = transport;
    this.timeout = timeout;
    this.retries = retries;
    this.retryInterval = retryInterval;
    this.log = log;
    this.queue = [];
    this.waiter = null;
    this.closed = false;
    this.pump = this.readLoop();
  }

  async readLoop() {
    let buf = '';
    try {
      for (;;) {
        const chunk = await this.t.read();
        if (chunk === null) break;
        for (const b of chunk) buf += String.fromCharCode(b);
        let i;
        while ((i = buf.indexOf('\r\n')) >= 0) {
          const line = buf.slice(0, i);
          buf = buf.slice(i + 2);
          if (!line) continue;
          const reply = parseReply(line);
          this.log('<', line);
          this.queue.push(reply);
          if (this.waiter) { const w = this.waiter; this.waiter = null; w(); }
        }
      }
    } catch (e) {
      this.log('!', `read loop ended: ${e.message}`);
    }
    this.closed = true;
    if (this.waiter) { const w = this.waiter; this.waiter = null; w(); }
  }

  async send(text) {
    this.log('>', text.replace(/\r\n$/, ''));
    await this.t.write(encode(text));
  }

  // Wait for the first reply of an interesting type; other replies are dropped.
  async expect(types, timeoutMs = this.timeout) {
    const deadline = Date.now() + timeoutMs;
    for (;;) {
      while (this.queue.length) {
        const r = this.queue.shift();
        if (types.has(r.type)) return r;
        this.log('?', `ignored ${r.type}${r.line ? ' ' + r.line : ''}`);
      }
      if (this.closed) throw new Error('port closed');
      const remaining = deadline - Date.now();
      if (remaining <= 0) return null;
      await new Promise((resolve) => {
        const timer = setTimeout(() => { this.waiter = null; resolve(); }, remaining);
        this.waiter = () => { clearTimeout(timer); resolve(); };
      });
    }
  }

  // Send `text`, expect one of okTypes; retry on error replies and timeouts.
  async command(text, okTypes, { ack = false, what = text.trim() } = {}) {
    let last = 'no reply';
    for (let attempt = 0; attempt < this.retries; attempt++) {
      this.queue.length = 0;
      await this.send(text);
      const r = await this.expect(new Set([...okTypes, ...ERR_TYPES]));
      if (r && ack) await this.send(CMD.ack);
      if (r && okTypes.has(r.type)) return r;
      last = r ? `radio replied ${r.type}` : 'timeout';
    }
    throw new Error(`${last} after ${this.retries} attempts (${what})`);
  }

  async connect() {
    for (const s of CMD.wake) await this.t.write(encode(s));
    this.log('>', 'P 0 ACMD:002');
    await this.command(CMD.sync, OK_TYPES, { what: 'sync' });
    await this.command(CMD.sync, OK_TYPES, { what: 'sync' });
    const v = await this.command(CMD.version, new Set(['CVRDQ']), { what: 'firmware version' });
    if (v.version === null || v.version < MIN_FIRMWARE) {
      throw new Error(`Firmware version ${v.version ?? '--.--'} is too old; the radio needs ${MIN_FIRMWARE} or later`);
    }
    this.version = v.version;
    return { version: v.version };
  }

  // Poll until the radio reports ready (status 00), backing off like YCE46.
  async waitReady() {
    let wait = this.retryInterval;
    let last = 'no reply';
    for (let attempt = 0; attempt < this.retries; attempt++) {
      this.queue.length = 0;
      await this.send(CMD.status);
      const r = await this.expect(new Set(['CEPSD', ...ERR_TYPES]));
      if (r) await this.send(CMD.ack);
      if (r && r.type === 'CEPSD' && r.status === '00') return;
      last = r ? (r.type === 'CEPSD' ? `status ${r.status}` : `radio replied ${r.type}`) : 'timeout';
      wait *= 2;
      await sleep(wait);
    }
    throw new Error(`radio not ready: ${last}`);
  }

  async readBlock(addr, len) {
    let last = 'no reply';
    for (let attempt = 0; attempt < this.retries; attempt++) {
      await this.waitReady();
      this.queue.length = 0;
      await this.send(CMD.read(addr, len));
      const r = await this.expect(new Set(['CEPDT', ...ERR_TYPES]));
      if (r) await this.send(CMD.ack);
      if (r && r.type === 'CEPDT' && r.addr === addr && r.data.length === len) return r.data;
      last = r ? (r.type === 'CEPDT' ? 'wrong block returned' : `radio replied ${r.type}`) : 'timeout';
    }
    throw new Error(`${last} reading block ${hex4(addr)}`);
  }

  async readImage(onProgress = () => {}) {
    const out = new Uint8Array(IMAGE_SIZE);
    for (let addr = 0; addr < IMAGE_SIZE; addr += 64) {
      onProgress(addr, IMAGE_SIZE);
      out.set(await this.readBlock(addr, 64), addr);
    }
    onProgress(IMAGE_SIZE, IMAGE_SIZE);
    return out;
  }

  async readChunks(chunks, onProgress = () => {}) {
    const out = new Map();
    let n = 0;
    for (const c of chunks) {
      onProgress(n++, chunks.length);
      out.set(c.addr, await this.readBlock(c.addr, c.len));
    }
    onProgress(chunks.length, chunks.length);
    return out;
  }

  async radioModelCode() {
    const head = await this.readBlock(OFF.model, 2);
    const foot = await this.readBlock(OFF.footerModel, 2);
    const h = (head[0] << 8) | head[1], f = (foot[0] << 8) | foot[1];
    if (h !== f) throw new Error(`radio model codes disagree (${hex4(h)} / ${hex4(f)})`);
    return h;
  }

  async writeChunks(image, chunks, onProgress = () => {}) {
    const imgModel = (image[OFF.model] << 8) | image[OFF.model + 1];
    const radioModel = await this.radioModelCode();
    if (radioModel !== imgModel) {
      throw new Error(`model mismatch: radio reports ${hex4(radioModel)}, data is for ${hex4(imgModel)}`);
    }
    let n = 0;
    for (const c of chunks) {
      onProgress(n++, chunks.length);
      const data = image.subarray(c.addr, c.addr + c.len);
      let last = 'no reply';
      let ok = false;
      for (let attempt = 0; attempt < this.retries && !ok; attempt++) {
        await this.waitReady();
        this.queue.length = 0;
        await this.send(CMD.write(c.addr, data));
        const r = await this.expect(new Set([...OK_TYPES, ...ERR_TYPES]));
        if (r && r.type === 'CMDOK') ok = true;
        else last = r ? `radio replied ${r.type}` : 'timeout';
      }
      if (!ok) throw new Error(`${last} writing block ${hex4(c.addr)}`);
    }
    onProgress(chunks.length, chunks.length);
  }

  async verifyChunks(image, chunks, onProgress) {
    const got = await this.readChunks(chunks, onProgress);
    return chunks.filter((c) => {
      const d = got.get(c.addr);
      for (let i = 0; i < c.len; i++) if (d[i] !== image[c.addr + i]) return true;
      return false;
    });
  }

  async close() {
    try { await this.t.close(); } catch { /* ignore */ }
    await this.pump;
  }
}

// WebSerial adapter: wraps an open SerialPort into the transport interface.
export function webSerialTransport(port) {
  const writer = port.writable.getWriter();
  const reader = port.readable.getReader();
  return {
    write: (bytes) => writer.write(bytes),
    read: async () => {
      const { value, done } = await reader.read();
      return done ? null : value;
    },
    close: async () => {
      try { await reader.cancel(); } catch { /* ignore */ }
      try { reader.releaseLock(); } catch { /* ignore */ }
      try { writer.releaseLock(); } catch { /* ignore */ }
      await port.close();
    },
  };
}
