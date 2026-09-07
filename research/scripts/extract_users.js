(() => JSON.stringify([...document.querySelectorAll('[data-testid="UserCell"]')].map(c => {
  const t = c.innerText.split('\n').map(s => s.trim()).filter(Boolean);
  const link = c.querySelector('a[href^="/"]');
  return { handle: link ? link.getAttribute('href') : '', name: t[0] || '', bio: t.slice(2).join(' ').slice(0, 200) };
})))()
