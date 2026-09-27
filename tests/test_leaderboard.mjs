// Execute the actual page script against lightweight DOM controls.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const elements = new Map(['search', 'family', 'source', 'reset', 'rows', 'status'].map(id => [id, {
  value: id === 'source' ? 'paper' : '', innerHTML: '', textContent: '', listeners: {},
  addEventListener(event, callback) { this.listeners[event] = callback; }
}]));
const context = vm.createContext({ document: {
  querySelector(selector) { return elements.get(selector.slice(1)); },
  querySelectorAll() { return []; }
} });
const page = fs.readFileSync(path.join(root, 'leaderboard.html'), 'utf8');
const inline = page.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
vm.runInContext(fs.readFileSync(path.join(root, 'data/leaderboard.js'), 'utf8'), context);
vm.runInContext(inline, context);
const run = expression => vm.runInContext(expression, context);

assert.equal(run('models.length'), 59);
assert.match(elements.get('status').textContent, /^58 models · current results/);
assert.equal(run('selectRows("", "", "paper", 19, "desc")[0][0]'), 'GLM-5.3-Flash');
assert.equal(run('selectRows("", "", "paper", 4, "desc")[0][0]'), 'TeleOCR');
assert.equal(run('selectRows("", "", "paper", 14, "desc")[0][0]'), 'Gemini 3.6 Flash');
assert.equal(run('selectRows("", "Pipeline", "paper", 19, "desc").length'), 13);
assert.equal(run('selectRows("", "End-to-End", "paper", 19, "desc").length'), 19);
assert.equal(run('selectRows("", "General VLM", "paper", 19, "desc").length'), 26);
assert.equal(run('selectRows("wevisdoc", "", "paper", 19, "desc").length'), 2);
assert.equal(run('selectRows("", "", "community", 19, "desc")[0][0]'), 'NaviDC-OCR');
for (const order of ['asc', 'desc']) {
  assert.equal(run(`selectRows("", "", "", 8, "${order}").at(-1)[0]`), 'NaviDC-OCR');
}
elements.get('source').value = 'community';
elements.get('source').listeners.change();
assert.match(elements.get('rows').innerHTML, /Community · author-reported/);
assert.match(elements.get('status').textContent, /^1 models · community results/);
elements.get('reset').listeners.click();
assert.equal(elements.get('source').value, 'paper');
assert.match(elements.get('status').textContent, /^58 models · current results/);
assert.equal(run('formatScore(null, 8)'), '—');
assert.equal(run('formatScore(0.123456, 8)'), '0.123');
console.log('Leaderboard passed: current/community filters, model search, architecture filters, track/Avg3 leaders, missing-last sorting, formatting, and reset.');
