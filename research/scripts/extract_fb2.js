(() => {
  const feed = document.querySelector('div[role="feed"]');
  const nodes = feed ? [...feed.children] : [...document.querySelectorAll('div[aria-posinset]')];
  const out = [];
  for (const n of nodes) {
    let t = (n.innerText || '').replace(/[͏​‌‍﻿]/g, '').replace(/\n(?=[^\n]{1,2}\n)/g, '');
    t = t.split('\n').map(s => s.trim()).filter(s => s && s !== 'Facebook').join('\n');
    if (t.length < 60) continue;
    const links = [...n.querySelectorAll('a[href]')].map(x => x.href);
    const permalink = links.find(h => /\/posts\/|story_fbid|\/permalink\/|\/groups\/[^/]+\/posts\//.test(h)) || '';
    const ext = links.filter(h => !h.includes('facebook.com') && !h.includes('fb.com')).slice(0, 3);
    out.push({ link: (permalink || ('fb:' + t.replace(/\s+/g, ' ').slice(0, 90))).split('?')[0], text: t.slice(0, 1800), ext });
  }
  return JSON.stringify(out);
})()
