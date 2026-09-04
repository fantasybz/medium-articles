# medium-articles

Medium articles by [@fantasybz](https://medium.com/@fantasybz) — long-form posts with Mermaid diagrams.

## Articles

| 日期 | 文章 | 英文版 | Medium | 發布紀錄 |
|---|---|---|---|---|
| 2026-09 | [別急著打造你的 Devin：Agentic Engineering 的組織策略與 90 天行動藍圖](2026-09-agentic-engineering-platform/article.md)（三部曲總論） | [EN](https://fantasybz.medium.com/dont-build-your-own-devin-org-strategy-and-a-90-day-blueprint-for-agentic-engineering-8187e7ec80f9) | [已發布](https://fantasybz.medium.com/%E5%88%A5%E6%80%A5%E8%91%97%E6%89%93%E9%80%A0%E4%BD%A0%E7%9A%84-devin-agentic-engineering-%E7%9A%84%E7%B5%84%E7%B9%94%E7%AD%96%E7%95%A5%E8%88%87-90-%E5%A4%A9%E8%A1%8C%E5%8B%95%E8%97%8D%E5%9C%96-7342ababc417) | [PUBLISHED.md](2026-09-agentic-engineering-platform/publish/PUBLISHED.md) |
| 2026-09 | [三部曲（一）組織篇：誰來做？Platform + Federation 的組織設計實務](2026-09-agentic-org-design/article.md) | [EN](https://fantasybz.medium.com/agentic-engineering-part-1-who-does-this-platform-plus-federation-in-practice-92343384d987) | [已發布](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%80-%E8%AA%B0%E4%BE%86%E5%81%9A-platform-federation-%E7%9A%84%E7%B5%84%E7%B9%94%E8%A8%AD%E8%A8%88%E5%AF%A6%E5%8B%99-9d9353ef7f3a) | [PUBLISHED.md](2026-09-agentic-org-design/publish/PUBLISHED.md) |
| 2026-10 | [三部曲（二）技術篇：Harness 藍圖—把系統變成 agent 讀得懂的地方](2026-10-agentic-harness-blueprint/article.md) | [EN](2026-10-agentic-harness-blueprint/article.en.md) | [已發布](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%BA%8C-harness-%E8%97%8D%E5%9C%96-%E6%8A%8A%E7%B3%BB%E7%B5%B1%E8%AE%8A%E6%88%90-agent-%E8%AE%80%E5%BE%97%E6%87%82%E7%9A%84%E5%9C%B0%E6%96%B9-f2a139f5b561) | [PUBLISHED.md](2026-10-agentic-harness-blueprint/publish/PUBLISHED.md) |
| 2026-11 | [三部曲（三）營運篇：Eval、單位經濟與規模化—把 agent 當產品營運](2026-11-agentic-eval-economics/article.md) | [EN](2026-11-agentic-eval-economics/article.en.md) | [已發布](https://fantasybz.medium.com/agentic-engineering-%E4%B8%89%E9%83%A8%E6%9B%B2-%E4%B8%89-eval-%E5%96%AE%E4%BD%8D%E7%B6%93%E6%BF%9F%E8%88%87%E8%A6%8F%E6%A8%A1%E5%8C%96-%E6%8A%8A-agent-%E7%95%B6%E7%94%A2%E5%93%81%E7%87%9F%E9%81%8B-d6d9623c2dc6) | [PUBLISHED.md](2026-11-agentic-eval-economics/publish/PUBLISHED.md) |

## Structure

每篇文章一個資料夾：

```
YYYY-MM-slug/
├── article.md          # 中文版本體（GitHub 原生渲染 Mermaid）
├── article.en.md       # 英文版本體
└── publish/            # Medium 發布包
    ├── medium-paste.md # 中文貼上版（含發布指南與插圖標記）
    ├── images/         # 中文版的 Mermaid 圖與表格 PNG
    ├── PUBLISHED.md    # 發布後補：網址、tag、封面圖、核對結果
    └── en/             # 英文發布包（結構同上，圖表為英文版）
        ├── medium-paste.md
        ├── images/     # 英文版有自己的圖，不與上層共用
        └── PUBLISHED.md
```

## Publishing

`publish/medium-paste.md` 可以自己手貼，也可以跑：

```bash
./tools/medium_draft.sh YYYY-MM-slug        # 中文包 publish/
./tools/medium_draft.sh YYYY-MM-slug en     # 英文包 publish/en/（內文與圖片一起換）
```

它會建好一份完整草稿並比對內容，停在發布前一步。細節與踩過的坑見
[PUBLISHING.md](PUBLISHING.md)。
