(async () => {
  /* Text of one Notion page via loadPageChunk. Set window.__NOTION_PAGE_ID (dashed uuid) first with `browse js`. */
  const pageId = window.__NOTION_PAGE_ID; if (!pageId) return 'ERR no __NOTION_PAGE_ID';
  const flat = t => Array.isArray(t) ? t.map(x => Array.isArray(x) ? x[0] : '').join('') : '';
  const blocks = {}; let cursor = { stack: [] };
  for (let chunk = 0; chunk < 6; chunk++) {
    const j = await fetch('/api/v3/loadPageChunk', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ pageId, limit: 100, cursor, chunkNumber: chunk, verticalColumns: false }) }).then(r => r.json());
    Object.assign(blocks, (j.recordMap && j.recordMap.block) || {});
    if (!j.cursor || !j.cursor.stack || !j.cursor.stack.length) break; cursor = j.cursor;
  }
  const lines = [];
  const walk = (id, depth) => { const b = blocks[id]; if (!b) return; const v = b.value.value || b.value; const t = flat(v.properties && v.properties.title);
    if (depth > 0 && v.type === 'page') { lines.push('  '.repeat(depth - 1) + '[子頁面] ' + t); return; }
    if (t) lines.push('  '.repeat(Math.max(depth - 1, 0)) + (v.type === 'header' || v.type === 'sub_header' || v.type === 'sub_sub_header' ? '# ' : v.type === 'to_do' ? '☐ ' : '') + t);
    (v.content || []).forEach(c => walk(c, depth + 1)); };
  walk(pageId, 0);
  const root = blocks[pageId]; const rv = root && (root.value.value || root.value) || {};
  return JSON.stringify({ id: pageId, blocks: Object.keys(blocks).length, last_edited: rv.last_edited_time ? new Date(rv.last_edited_time).toISOString().slice(0, 10) : '', text: lines.join('\n').slice(0, 16000) });
})()
