// Orakel für tests/fuzz/rc001_cases.py: CommonMark-Lesart über markdown-it.
// Copyright (c) 2026 Jakob Flaman · SPDX-License-Identifier: MIT
const md = require(process.argv[2] || 'markdown-it')();
const rl = require('readline').createInterface({ input: process.stdin });
let n = 0, silent = 0;
function visible(tokens) { // dargestellter Text ausserhalb von Inline-Code, inkl. HTML und Attribute
  let out = '';
  for (const t of tokens) {
    if (t.type === 'code_inline' || t.type === 'code_block' || t.type === 'fence') { out += ' '; continue; }
    if (t.type === 'softbreak' || t.type === 'hardbreak' || t.block) out += ' ';
    out += t.children ? visible(t.children) : (t.content || '');   // inline ohne Trenner: SH<em>OUL</em>D
    if (t.attrs) out += ' ' + t.attrs.map(a => a[1]).join(' ') + ' ';
  }
  return out;
}
rl.on('line', line => {
  const c = JSON.parse(line); n++;
  const v = visible(md.parse(c.t, {})).replace(/[\p{Cf}\u034f\u115f\u1160\u3164\uffa0]/gu, '').replace(/«[^»\n]*»|“[^”\n]*”|„[^“”\n]*[“”]/g, ' ');
  if (/(?<![A-Za-z0-9])(SHOULD|MAY)(?![A-Za-z0-9])/.test(v) && !c.flag) {
    silent++; if (silent <= 10) console.log('STILLER DURCHLASS:', JSON.stringify(c.t));
  }
});
rl.on('close', () => { console.log(`Fälle ${n}, stille Durchlässe ${silent}`); process.exitCode = silent ? 1 : 0; });
