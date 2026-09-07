(() => {
  const main = document.querySelector('main') || document.body;
  const parts = main.innerText.split(/\nFeed post\n/).slice(1);
  return JSON.stringify(parts.map(p => {
    const lines = p.split('\n').map(s => s.trim()).filter(Boolean);
    const body = lines.join('\n');
    return { link: 'li:' + body.replace(/\s+/g, ' ').slice(0, 90), head: lines.slice(0, 5).join(' | ').slice(0, 220), text: body.slice(0, 1800) };
  }));
})()
