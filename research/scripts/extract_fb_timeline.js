(() => {
  const AUTHOR = window.__FB_AUTHOR || '';
  const main = document.querySelector('[role="main"]') || document.body;
  let t = main.innerText.replace(/[͏​‌‍﻿]/g, '');
  const lines = t.split('\n').map(s => s.trim()).filter(s => s && s !== 'Facebook');
  const out = []; let cur = null;
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (l === AUTHOR && lines[i + 1] && /[·分鐘小時天週月年日]|\d/.test(lines[i + 1]) && lines[i+1].length < 40) {
      if (cur && cur.text.length > 40) out.push(cur);
      cur = { link: '', text: '', time: lines[i + 1] };
      i++; continue;
    }
    if (cur) cur.text += l + '\n';
  }
  if (cur && cur.text.length > 40) out.push(cur);
  return JSON.stringify(out.map(p => ({ link: 'fb:' + p.time + ':' + p.text.replace(/\s+/g, ' ').slice(0, 80), time: p.time, text: p.text.slice(0, 2500) })));
})()
