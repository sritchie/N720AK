import {
  RadioImage, Radio, webSerialTransport, IMAGE_SIZE, MODEL_CODE, MAX_CHANNELS, GROUP_COUNT,
  USB_VENDOR_ID, WRITE_REGIONS, diffChunks, validateFrequency, validateTag, validateGroupName,
  freqToMHz, mhzToFreq, channelsToCsv, csvToChannels,
} from './fta850.js';

const $ = (id) => document.getElementById(id);

const state = {
  base: null,        // Uint8Array: the image edits are applied on top of
  baseLabel: '',
  channels: [],      // editable rows; hidden fields (lat/lon/...) ride along untouched
  groups: [],
  dirty: false,
  port: null,
  radio: null,
  busy: false,
};

// ------------------------------------------------------------ helpers

function status(msg, kind = '') {
  const el = $('status');
  el.textContent = msg;
  el.className = 'status ' + kind;
}

function progress(done, total) {
  const bar = $('progress');
  bar.hidden = total === 0;
  bar.max = total || 1;
  bar.value = done;
}

const logLines = [];
function log(dir, text) {
  if (dir) {
    logLines.push(`${new Date().toISOString().slice(11, 23)} ${dir} ${text}`);
    if (logLines.length > 3000) logLines.splice(0, logLines.length - 3000);
  }
  if (!$('log-details').open) return;
  const el = $('log');
  el.textContent = logLines.slice(-400).join('\n');
  el.scrollTop = el.scrollHeight;
}

function download(name, bytes, type = 'application/octet-stream') {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([bytes], { type }));
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

function readFile(file) {
  return new Promise((resolve, reject) => {
    const r = new FileReader();
    r.onload = () => resolve(r.result);
    r.onerror = () => reject(r.error);
    r.readAsArrayBuffer(file);
  });
}

function allow833() {
  return state.base ? new RadioImage(state.base).is833Enabled() : false;
}

function setDirty(d) {
  state.dirty = d;
  $('dirty').hidden = !d;
}

// ------------------------------------------------------------ model

function loadImage(bytes, label) {
  const img = new RadioImage(bytes);
  if (img.modelCode() !== MODEL_CODE || img.footerModelCode() !== MODEL_CODE) {
    if (!confirm(`This data has model code ${img.modelCode().toString(16)} (expected ${MODEL_CODE.toString(16)} for the FTA-850). Load it anyway?`)) return false;
  }
  let channels;
  try {
    channels = img.channels();
  } catch (e) {
    alert(`Could not decode the memory book: ${e.message}`);
    return false;
  }
  state.base = bytes;
  state.baseLabel = label;
  state.channels = channels.map((c) => ({ ...c, error: null }));
  state.groups = img.groupNames();
  setDirty(false);
  render();
  return true;
}

function buildImage() {
  const img = new RadioImage(new Uint8Array(state.base));
  state.groups.forEach((g, i) => img.setGroupName(i + 1, g));
  img.applyChannels(state.channels);
  return img;
}

function validateAll() {
  const errors = [];
  state.groups.forEach((g, i) => { const e = validateGroupName(g); if (e) errors.push(`Group ${i + 1}: ${e}`); });
  const a833 = allow833();
  state.channels.forEach((c, i) => {
    const errs = [];
    if (!(c.group >= 1 && c.group <= GROUP_COUNT)) errs.push('group must be 1-9');
    const fe = validateFrequency(c.freq, { allow833: a833 });
    if (fe) errs.push(fe);
    const te = validateTag(c.tag);
    if (te) errs.push(te);
    c.error = errs.length ? errs.join('; ') : null;
    if (c.error) errors.push(`Row ${i + 1} (${c.tag || 'untitled'}): ${c.error}`);
  });
  if (state.channels.length > MAX_CHANNELS) errors.push(`${state.channels.length} channels; the radio holds ${MAX_CHANNELS}`);
  return errors;
}

// ------------------------------------------------------------ render

function render() {
  $('source').textContent = state.base ? state.baseLabel : 'nothing loaded';
  renderGroups();
  renderTable();
  updateButtons();
}

function renderGroups() {
  const box = $('groups');
  box.innerHTML = '';
  state.groups.forEach((name, i) => {
    const label = document.createElement('label');
    label.innerHTML = `<span>${i + 1}</span>`;
    const input = document.createElement('input');
    input.value = name;
    input.maxLength = 10;
    input.addEventListener('input', () => {
      state.groups[i] = input.value.toUpperCase();
      input.value = state.groups[i];
      input.classList.toggle('bad', !!validateGroupName(state.groups[i]));
      setDirty(true);
      renderGroupOptions();
    });
    label.appendChild(input);
    box.appendChild(label);
  });
}

function groupOptionsHtml(selected) {
  return state.groups.map((g, i) => `<option value="${i + 1}"${i + 1 === selected ? ' selected' : ''}>${i + 1} ${g}</option>`).join('');
}

function renderGroupOptions() {
  document.querySelectorAll('#rows select').forEach((sel) => {
    const v = Number(sel.value);
    sel.innerHTML = groupOptionsHtml(v);
  });
}

function renderTable() {
  const tbody = $('rows');
  tbody.innerHTML = '';
  const a833 = allow833();
  state.channels.forEach((c, i) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td class="num">${i + 1}</td>
      <td class="num">${c.address && c.address !== 0xffff ? c.address : '<span class="muted">new</span>'}</td>
      <td><select></select></td>
      <td><input class="freq" value="${freqToMHz(c.freq)}" placeholder="118.000" inputmode="decimal"></td>
      <td><input class="tag" value="${c.tag.replace(/"/g, '&quot;')}" maxlength="14" placeholder="TAG NAME"></td>
      <td class="extra">${c.lat && c.lon ? 'waypoint' : ''}${c.scan ? ' scan' : ''}</td>
      <td><button class="del" title="Delete row">&times;</button></td>`;
    const sel = tr.querySelector('select');
    sel.innerHTML = groupOptionsHtml(c.group);
    sel.addEventListener('change', () => { c.group = Number(sel.value); setDirty(true); });
    const freq = tr.querySelector('.freq');
    const tag = tr.querySelector('.tag');
    const check = () => {
      const fe = validateFrequency(c.freq, { allow833: a833 });
      const te = validateTag(c.tag);
      freq.classList.toggle('bad', !!fe); freq.title = fe || '';
      tag.classList.toggle('bad', !!te); tag.title = te || '';
    };
    freq.addEventListener('input', () => { c.freq = mhzToFreq(freq.value); setDirty(true); check(); });
    freq.addEventListener('blur', () => { if (!validateFrequency(c.freq, { allow833: a833 })) freq.value = freqToMHz(c.freq); });
    tag.addEventListener('input', () => {
      const pos = tag.selectionStart;
      c.tag = tag.value.toUpperCase();
      tag.value = c.tag; tag.setSelectionRange(pos, pos);
      setDirty(true); check();
    });
    tr.querySelector('.del').addEventListener('click', () => {
      state.channels.splice(i, 1); setDirty(true); renderTable(); updateButtons();
    });
    check();
    tbody.appendChild(tr);
  });
  $('count').textContent = `${state.channels.length} / ${MAX_CHANNELS}`;
}

function updateButtons() {
  const loaded = !!state.base;
  const connected = !!state.radio;
  const busy = state.busy;
  $('btn-connect').disabled = busy || connected || !navigator.serial;
  $('btn-disconnect').disabled = busy || !connected;
  $('btn-read').disabled = busy || !navigator.serial;
  $('btn-program').disabled = busy || !loaded || !navigator.serial;
  for (const id of ['btn-save', 'btn-export', 'btn-add', 'btn-import']) $(id).disabled = busy || !loaded;
  $('btn-new').disabled = busy;
  $('btn-open').disabled = busy;
}

async function withBusy(fn) {
  if (state.busy) return;
  state.busy = true; updateButtons();
  try { await fn(); }
  catch (e) { status(e.message, 'error'); log('!', e.message); console.error(e); }
  finally { state.busy = false; progress(0, 0); updateButtons(); }
}

// ------------------------------------------------------------ radio

async function ensureConnected() {
  if (state.radio) return;
  if (!navigator.serial) throw new Error('This browser has no Web Serial support. Use Chrome or Edge.');
  status('Choose the FTA-850 in the port picker…');
  const port = await navigator.serial.requestPort({ filters: [{ usbVendorId: USB_VENDOR_ID }] });
  await port.open({ baudRate: 115200 });
  port.addEventListener('disconnect', () => { state.radio = null; state.port = null; status('Radio unplugged', 'error'); updateButtons(); });
  state.port = port;
  state.radio = new Radio(webSerialTransport(port), { log });
  status('Connecting…');
  try {
    const { version } = await state.radio.connect();
    status(`Connected. Firmware ${version.toFixed(2)}`, 'ok');
  } catch (e) {
    await disconnect();
    throw new Error(`${e.message}. Is the radio in CP mode (hold SQL while powering on)?`);
  }
  updateButtons();
}

async function disconnect() {
  const r = state.radio;
  state.radio = null; state.port = null;
  if (r) await r.close();
  updateButtons();
}

async function readFromRadio() {
  if (state.dirty && !confirm('Discard unsaved edits and read the radio?')) return;
  await ensureConnected();
  status('Reading memory…');
  const bytes = await state.radio.readImage(progress);
  if (loadImage(bytes, `radio (firmware ${state.radio.version.toFixed(2)}, read ${new Date().toLocaleTimeString()})`)) {
    status(`Read ${state.channels.length} channels from the radio`, 'ok');
  }
}

async function programRadio() {
  const errors = validateAll();
  renderTable();
  if (errors.length) { status(`Fix ${errors.length} problem(s) first: ${errors[0]}`, 'error'); return; }
  const after = buildImage();
  const chunks = diffChunks(state.base, after.bytes, WRITE_REGIONS);
  if (!chunks.length) { status('Nothing to write: the radio already has this memory book', 'ok'); return; }
  const bytes = chunks.reduce((n, c) => n + c.len, 0);
  const warn = state.baseLabel.startsWith('radio') ? '' : '\n\nNote: the loaded data did not come from this radio. Its memory book will be replaced with this list.';
  if (!confirm(`Write ${state.channels.length} channels and group names to the radio?\n${chunks.length} blocks, ${bytes} bytes. Only memory-book areas are written.${warn}`)) return;
  await ensureConnected();
  status('Programming…');
  await state.radio.writeChunks(after.bytes, chunks, progress);
  status('Verifying…');
  const bad = await state.radio.verifyChunks(after.bytes, chunks, progress);
  if (bad.length) throw new Error(`Verification failed: ${bad.length} block(s) differ (first at 0x${bad[0].addr.toString(16)}). Do not trust the radio memory until re-programmed.`);
  loadImage(after.bytes, `radio (programmed ${new Date().toLocaleTimeString()})`);
  status(`Programmed and verified ${chunks.length} blocks. Power-cycle the radio to leave CP mode.`, 'ok');
}

// ------------------------------------------------------------ files

async function openDat(file) {
  const buf = new Uint8Array(await readFile(file));
  if (buf.length !== IMAGE_SIZE) throw new Error(`${file.name} is ${buf.length} bytes; an FTA-850 .dat file is ${IMAGE_SIZE}`);
  if (loadImage(buf, `file ${file.name}`)) status(`Loaded ${state.channels.length} channels from ${file.name}`, 'ok');
}

function saveDat() {
  const errors = validateAll(); renderTable();
  if (errors.length) { status(`Fix ${errors.length} problem(s) first: ${errors[0]}`, 'error'); return; }
  download('FTA-850.dat', buildImage().bytes);
  status('Saved FTA-850.dat (YCE46-compatible)', 'ok');
}

async function importCsv(file) {
  const text = new TextDecoder().decode(await readFile(file));
  const rows = csvToChannels(text, { allow833: allow833() });
  if (state.channels.length && !confirm(`Replace the current ${state.channels.length} channels with ${rows.length} from ${file.name}?`)) return;
  state.channels = rows.map((r) => ({ ...r, error: null }));
  setDirty(true); renderTable(); updateButtons();
  status(`Imported ${rows.length} channels from ${file.name}`, 'ok');
}

function exportCsv() {
  download('FTA-850-channels.csv', channelsToCsv(state.channels), 'text/csv');
}

// ------------------------------------------------------------ wiring

function wire() {
  $('btn-connect').addEventListener('click', () => withBusy(ensureConnected));
  $('btn-disconnect').addEventListener('click', () => withBusy(async () => { await disconnect(); status('Disconnected'); }));
  $('btn-read').addEventListener('click', () => withBusy(readFromRadio));
  $('btn-program').addEventListener('click', () => withBusy(programRadio));
  $('btn-new').addEventListener('click', () => {
    if (state.dirty && !confirm('Discard unsaved edits?')) return;
    loadImage(RadioImage.default().bytes, 'factory default image');
    status('Loaded the factory default image (empty memory book)', 'ok');
  });
  $('btn-open').addEventListener('click', () => $('file-dat').click());
  $('file-dat').addEventListener('change', (e) => { const f = e.target.files[0]; e.target.value = ''; if (f) withBusy(() => openDat(f)); });
  $('btn-save').addEventListener('click', saveDat);
  $('btn-import').addEventListener('click', () => $('file-csv').click());
  $('file-csv').addEventListener('change', (e) => { const f = e.target.files[0]; e.target.value = ''; if (f) withBusy(() => importCsv(f)); });
  $('btn-export').addEventListener('click', exportCsv);
  $('btn-add').addEventListener('click', () => {
    if (state.channels.length >= MAX_CHANNELS) { status(`The radio holds ${MAX_CHANNELS} channels`, 'error'); return; }
    state.channels.push({ address: 0xffff, group: 1, freq: '', tag: '', lat: '', lon: '', nsew: 0xff, trueCourse: '', shift: 0, scan: false, error: null });
    setDirty(true); renderTable(); updateButtons();
    const inputs = $('rows').querySelectorAll('input.freq');
    inputs[inputs.length - 1]?.focus();
  });
  $('log-details').addEventListener('toggle', () => log());
  window.addEventListener('beforeunload', (e) => { if (state.dirty) { e.preventDefault(); e.returnValue = ''; } });
  if (!navigator.serial) $('no-serial').hidden = false;
  loadImage(RadioImage.default().bytes, 'factory default image');
  status(navigator.serial
    ? 'Editing the factory default image. Read from radio to start from what the radio holds.'
    : 'Editing the factory default image. This browser cannot talk to the radio.');
}

wire();
