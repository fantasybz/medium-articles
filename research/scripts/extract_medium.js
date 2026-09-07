(() => JSON.stringify([...document.querySelectorAll('article')].map(a => {
  const h = a.querySelector('h2, h3');
  const link = [...a.querySelectorAll('a[href]')].map(x => x.href).find(x => /\/[a-z0-9-]+-[0-9a-f]{8,}(\?|$)/.test(x)) || '';
  const t = a.innerText.split('\n').map(s => s.trim()).filter(Boolean);
  return { link: link.split('?')[0], title: h ? h.innerText.trim() : (t[0] || ''), lines: t.slice(0, 8).join(' | ').slice(0, 300) };
})))()
