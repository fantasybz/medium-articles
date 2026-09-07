(async () => {
  /* List the most recently edited pages in the user's main Notion workspace via the internal search API. | Optional: window.__NOTION_SPACE_ID / window.__NOTION_QUERY set beforehand with `browse js`. */
  const flat = t => Array.isArray(t) ? t.map(x => Array.isArray(x) ? x[0] : '').join('') : '';
  const post = (path, body) => fetch(path, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) }).then(r => r.json());
  let spaceId = window.__NOTION_SPACE_ID;
  if (!spaceId) {
    const j = await post('/api/v3/loadUserContent', {});
    const views = Object.values((j.recordMap || {}).space_view || {}).map(v => v.value.value || v.value);
    views.sort((a, b) => (b.private_pages || []).length - (a.private_pages || []).length);
    spaceId = views[0] && views[0].space_id;
  }
  const body = { type: 'BlocksInSpace', query: window.__NOTION_QUERY || '', spaceId, limit: 100,
    filters: { isDeletedOnly: false, excludeTemplates: false, navigableBlockContentOnly: true, requireEditPermissions: false, includePublicPagesWithoutExplicitAccess: false, ancestors: [], createdBy: [], editedBy: [], lastEditedTime: {}, createdTime: {}, inTeams: [] },
    sort: window.__NOTION_QUERY ? { field: 'relevance' } : { field: 'lastEdited', direction: 'desc' }, source: 'quick_find_input_change' };
  const j = await post('/api/v3/search', body);
  if (!j.results) return 'ERR ' + JSON.stringify(j).slice(0, 500);
  const blocks = (j.recordMap && j.recordMap.block) || {};
  const pages = j.results.map(x => { const b = blocks[x.id]; const v = b && (b.value.value || b.value) || {};
    return { id: x.id, title: (flat(v.properties && v.properties.title) || String((x.highlight || {}).title || '')).replace(/<[^>]+>/g, ''), type: v.type,
      last_edited: v.last_edited_time ? new Date(v.last_edited_time).toISOString().slice(0, 10) : '', created: v.created_time ? new Date(v.created_time).toISOString().slice(0, 10) : '' }; });
  return JSON.stringify({ spaceId, total: j.total, pages });
})()
