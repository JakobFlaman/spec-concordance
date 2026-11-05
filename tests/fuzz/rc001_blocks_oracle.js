// Orakel für tests/fuzz/rc001_blocks.py (CommonMark über markdown-it, HTML erlaubt).
// Copyright (c) 2026 Jakob Flaman · SPDX-License-Identifier: MIT
const md=require(process.argv[3]||'markdown-it')({html:true});
const cases=JSON.parse(require('fs').readFileSync(process.argv[2]));
let bad=0, err=0;
function vis(ts){let o='';for(const t of ts){if(t.type==='code_inline'||t.type==='code_block'||t.type==='fence'){o+=' ';continue;}
 if(t.type==='html_block'||t.type==='html_inline'){o+=' '+t.content.replace(/<!--[\s\S]*?-->/g,' ').replace(/<script[\s\S]*?<\/script>/gi,' ').replace(/<[^>]*>/g,' ')+' ';continue;}
 if(t.type==='softbreak'||t.type==='hardbreak'||t.block)o+=' '; o+=t.children?vis(t.children):(t.content||''); if(t.attrs)o+=' '+t.attrs.map(a=>a[1]).join(' ')+' ';}return o;}
for(const c of cases){ if(c.rc===2){err++;continue;}
  const v=vis(md.parse(c.t,{})).replace(/«[^»\n]*»|“[^”\n]*”|„[^“”\n]*[“”]/g,' ');
  if(/(?<![A-Za-z0-9])(SHOULD|MAY)(?![A-Za-z0-9])/.test(v) && c.rc===0){bad++; if(bad<=6) console.log('STILL:',JSON.stringify(c.t));}}
console.log(`Fälle ${cases.length}, Exit 2: ${err}, stille Durchlässe ${bad}`); process.exitCode = bad ? 1 : 0;
