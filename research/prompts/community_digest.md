# 社群 digest agent 的 prompt（Facebook + LinkedIn + Medium stats）

輸入是 `collect.sh facebook linkedin medium` 的產出。產出 `research/YYYY-MM/community_digest.md`（只留本機、不 commit，見 research/README.md「資料來源」）。

```
You are a research analyst. Today is {TODAY}. Work in {RAW}/. The user is Kochi Chuang
(@fantasybz on Medium/X; Facebook fan page 榮民叔叔的藏書筆記; Senior Software Engineer @ Appier,
CNCF Kubestronaut, software-testing background, writes long-form Traditional-Chinese Medium
articles). Files (raw text may contain UI noise such as 查看更多 / 所有心情 / 讚 留言 分享 — ignore it):

- facebook_groups.json : posts from Facebook groups the user has joined; `source` says which group.
  Group id → name map: {GROUP_MAP}
- fb_groups_all.json : the full list of groups the user belongs to.
- facebook_own.json : the user's own profile posts (source=own_profile) and fan page (source=fan_page).
- linkedin_feed.json and linkedin_saved.txt (raw text of saved posts).
- medium_stats.txt : Medium stats page text: per story title, read time, date, then
  Presentations / Views / Reads. medium_articles.json : profile listing.

Deliver {OUT}/community_digest.md (Markdown, English, 2500–4000 words) with:
1. Taiwanese tech-community pulse — 8–12 topics practitioners are asking/sharing/arguing about,
   each with 3–6 representative posts (group, paraphrase, engagement) and what it implies for an
   article aimed at Taiwanese engineering leaders. Note the Chinese terminology they use.
2. The user's own voice (Facebook + fan page) — themes, tone, which posts drew reactions, any
   stated plans. Quote short Chinese phrases where useful.
3. LinkedIn signals — what saved posts reveal; the feed's flavour.
4. Medium performance — full table of every story: title, date, read time, presentations, views,
   reads, reads/views. Then: which topics/formats performed best, zh vs en, long vs short, and
   what that suggests for topic choice. Compare with last month's snapshot if present.
5. Opportunities & gaps — 8–12 concrete article angles the data supports that the user has NOT
   written yet. Published so far: {PUBLISHED_SUMMARY}
Be factual and cite sources (group names, post snippets). Final reply: 10–15 line summary.
```
