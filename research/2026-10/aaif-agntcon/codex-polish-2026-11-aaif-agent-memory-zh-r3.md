# Codex 校稿 — 2026-11-aaif-agent-memory/article.md（第 3 輪）

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-29 05:59. 原話照錄，未經摘要。

我會先讀寫作規範與前兩輪處置紀錄，確認已採用的修正，再逐段核對中英文、圖說與表格；全程只讀，不修改檔案，也不讀取你列出的禁用目錄。
<!-- codex ran: /bin/zsh -lc "cat 'research/2026-09/voice_brief.md'" -->
<!-- codex ran: /bin/zsh -lc "cat 'STYLE.md'" -->
<!-- codex ran: /bin/zsh -lc "cat 'research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-memory-zh-r1.md'" -->
<!-- codex ran: /bin/zsh -lc "cat 'research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-memory-zh-r2.md'" -->
<!-- codex ran: /bin/zsh -lc "cat '.context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-memory-zh-r2-disposition.md'" -->
<!-- codex ran: /bin/zsh -lc "cat '.context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-memory-zh-r1-disposition.md'" -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-memory-zh-r1.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '65,200p' research/2026-09/voice_brief.md" -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-memory-zh-r1-disposition.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '30,112p' .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-memory-zh-r1-disposition.md" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.en.md | sed -n '1,171p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.md | sed -n '1,171p'" -->
前兩輪處置紀錄已核對；被拒絕的四項都有明確理由，我不會重提。第二輪四項修正已在中文現稿落實，接著會核對英文同步，以及後半部案例與驗收表的範圍是否一致。
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.en.md | sed -n '1,90p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.md | sed -n '145,263p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.en.md | sed -n '172,265p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.md | sed -n '264,390p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.en.md | sed -n '267,390p'" -->
中英文正文、圖說與五張表格已比對完，第二輪的交錯測試條件也已同步。目前未見新的實質中英落差；我正核對跨篇節次，並檢查剩餘的局部用詞，避免把個人修辭偏好列成問題。
<!-- codex ran: /bin/zsh -lc "rg --files -g 'article.md' -g '"'!agents/**'"' -g '"'!**/agents/**'"' -g '"'!.claude/**'"' -g '"'!**/.claude/**'"' -g '"'!**/node_modules/**'"' -g -->
<!-- codex ran: /bin/zsh -lc "rg --files -g 'article.md' -g '"'!agents/**'"' -g '"'!**/agents/**'"' -g '"'!.claude/**'"' -g '"'!**/.claude/**'"' -g '"'!**/node_modules/**'"' -g -->
<!-- codex ran: /bin/zsh -lc "sed -n '232,246p' 2026-11-same-spec-variance/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |PagerDuty|校準'"' 2026-11-aaif-after-tokyo/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |owner|到期日|frozen holdout'"' 2026-10-green-reliability/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## 十|常駐|單次交代|診斷 pilot|部署 trial|預設採用'"' 2026-11-same-spec-overview/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## 二|第三種|共享|誤解|oracle'"' 2026-11-same-spec-contract/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '25,71p' 2026-09-agentic-org-design/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '57,70p' 2026-10-agentic-harness-blueprint/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,30p' 2026-10-green-review/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## 七|replay 卻|replay 沒|replay.*未|未.*replay'"' 2026-10-green-testing/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## 二|三個陷阱|校準|judge'"' 2026-11-agentic-eval-economics/article.md | head -n 12" -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
import re
p=Path(\"2026-11-aaif-agent-memory/article.md\")
s=p.read_text()
body=re.sub(r\""'```['"\\s\\S]* -->
本輪仍有 **2 項：必改 0、建議 2、可選 0**。第二輪四項修正均已落實，未見修正衍生的新問題；前輪不採用的意見不重提。

1. **［建議］§六〈哪些結果支持擴大使用記憶〉＋「這些測試也要避免獎勵……」**

   原文：「少查幾次工具不必然省時。」

   問題：此處指透過工具查詢資料的次數；「查工具」的動詞與受詞搭配不準，容易讀成查驗工具本身。

   建議改法：「少做幾次工具查詢不必然省時。」

2. **［建議］§七〈讓經驗留下來，也讓下一個人有理由修正它〉＋「這次核對改變了我願意……」**

   原文：「排程與剩餘風險由權責人決定。」

   問題：「決定剩餘風險」省略了決策內容；權責人決定的是如何處置風險，並非風險本身。

   建議改法：「排程與剩餘風險的處置，由權責人決定。」

統計依主要問題歸類，不重複計數：

| 類別 | 項數 |
|---|---:|
| 錯字、同音誤字、漏字、重複字 | 0 |
| 標點 | 0 |
| 斷句與可讀性 | 2 |
| 指涉與承接 | 0 |
| 用詞一致、術語引入 | 0 |
| 前後一致、跨節指涉 | 0 |
| 中英對照 | 0 |
| **合計** | **2** |

本輪未發現新的實質中英落差、數字矛盾或跨節指錯，圖說、表格與正文的範圍也一致。未見明顯錯字、「——」或引號、括號失配；剩餘兩項皆為局部動詞搭配與動作對象的精確化。

<!-- tokens: in 1833623 out 9736 -->
