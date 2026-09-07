(() => {
  const out = [];
  for (const a of document.querySelectorAll('article[data-testid="tweet"]')) {
    const userEl = a.querySelector('div[data-testid="User-Name"]');
    const ut = userEl ? userEl.innerText : '';
    const handle = (ut.match(/@\w+/) || [''])[0];
    const name = ut.split('\n')[0];
    const timeEl = a.querySelector('time');
    const time = timeEl ? timeEl.getAttribute('datetime') : '';
    const link = timeEl && timeEl.closest('a') ? timeEl.closest('a').href : '';
    const textEl = a.querySelector('div[data-testid="tweetText"]');
    const text = textEl ? textEl.innerText : '';
    const grp = a.querySelector('div[role="group"][aria-label]');
    const metrics = grp ? grp.getAttribute('aria-label') : '';
    const card = a.querySelector('[data-testid="card.wrapper"]');
    const cardText = card ? card.innerText.replace(/\s+/g, ' ').slice(0, 200) : '';
    const ext = [...a.querySelectorAll('a[href]')].map(x => x.href)
      .filter(h => !/https?:\/\/(x|twitter)\.com\//.test(h) && !h.startsWith('https://t.co')).slice(0, 3);
    const social = a.querySelector('[data-testid="socialContext"]');
    const quoted = a.querySelector('div[role="link"] div[data-testid="tweetText"]');
    out.push({ handle, name, time, link, text, metrics, cardText, ext,
      social: social ? social.innerText : '', quoted: quoted ? quoted.innerText.slice(0, 300) : '' });
  }
  return JSON.stringify(out);
})()
