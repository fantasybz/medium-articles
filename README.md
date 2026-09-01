# medium-articles

Medium articles by [@fantasybz](https://medium.com/@fantasybz) — long-form posts with Mermaid diagrams.

## Articles

| 日期 | 文章 | Medium | 發布紀錄 |
|---|---|---|---|
| 2026-09 | [別急著打造你的 Devin：Agentic Engineering 的組織策略與 90 天行動藍圖](2026-09-agentic-engineering-platform/article.md)（三部曲總論） | [已發布](https://fantasybz.medium.com/%E5%88%A5%E6%80%A5%E8%91%97%E6%89%93%E9%80%A0%E4%BD%A0%E7%9A%84-devin-agentic-engineering-%E7%9A%84%E7%B5%84%E7%B9%94%E7%AD%96%E7%95%A5%E8%88%87-90-%E5%A4%A9%E8%A1%8C%E5%8B%95%E8%97%8D%E5%9C%96-7342ababc417) | [PUBLISHED.md](2026-09-agentic-engineering-platform/publish/PUBLISHED.md) |
| 2026-09 | [三部曲（一）組織篇：誰來做？Platform + Federation 的組織設計實務](2026-09-agentic-org-design/article.md) | （發布後補連結） | — |
| 2026-10 | [三部曲（二）技術篇：Harness 藍圖——把系統變成 agent 讀得懂的地方](2026-10-agentic-harness-blueprint/article.md) | （發布後補連結） | — |
| 2026-11 | [三部曲（三）營運篇：Eval、單位經濟與規模化——把 agent 當產品營運](2026-11-agentic-eval-economics/article.md) | （發布後補連結） | — |

## Structure

每篇文章一個資料夾：

```
YYYY-MM-slug/
├── article.md          # 文章本體（GitHub 原生渲染 Mermaid）
└── publish/            # Medium 發布包
    ├── medium-paste.md # 貼上版全文（含發布指南與插圖標記）
    ├── images/         # Mermaid 圖與表格渲染成的 PNG
    └── PUBLISHED.md    # 發布後補：網址、tag、封面圖、核對結果
```

## Publishing

`publish/medium-paste.md` 可以自己手貼，也可以跑：

```bash
./tools/medium_draft.sh YYYY-MM-slug
```

它會建好一份完整草稿並比對內容，停在發布前一步。細節與踩過的坑見
[PUBLISHING.md](PUBLISHING.md)。
