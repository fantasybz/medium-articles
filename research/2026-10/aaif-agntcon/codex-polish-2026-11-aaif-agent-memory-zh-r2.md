# Codex 校稿 — 2026-11-aaif-agent-memory/article.md（第 2 輪）

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-29 05:49. 原話照錄，未經摘要。

我會先核對寫作規範、第一輪處置紀錄與中英兩版，再逐段檢查本輪仍存在的問題；全程只讀取這個 repository，不修改檔案。
<!-- codex ran: /bin/zsh -lc pwd -->
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md research/2026-09/voice_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-memory-zh-r1.md .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-memo -->
<!-- codex ran: /bin/zsh -lc "wc -l 2026-11-aaif-agent-memory/article.md 2026-11-aaif-agent-memory/article.en.md; rg --files -g 'AGENTS.md' -g '*agent-memory*' -g '*memory*' re -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-memory-zh-r1.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,205p' .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-memory-zh-r1-disposition.md" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.en.md | sed -n '1,150p'" -->
<!-- codex ran: /bin/zsh -lc "sed -n '55,180p' research/2026-09/voice_brief.md; rg --files research/2026-10 research/2026-11 -g 'style_brief.md' -g '"'!agents/**'"' -g '"'!.cla -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.en.md | sed -n '151,265p'" -->
第一輪採用的修正已在現稿落實，撤回後的取回契約、測試叢集的觀察範圍與英文同步項目也已對齊。我會保留作者已說明理由的取捨，接著細查後半部的案例、驗收表與跨篇指涉。
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.en.md | sed -n '267,379p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.md | sed -n '73,260p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.md | sed -n '262,335p'" -->
<!-- codex ran: /bin/zsh -lc "cat research/2026-10/style_brief.md; rg --files -g 'AGENTS.md' -g '"'!agents/**'"' -g '"'!**/agents/**'"' -g '"'!.claude/**'"' -g '"'!**/.claude/* -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-memory/article.md | sed -n '336,378p'; sed -n '175,185p' 2026-11-aaif-agent-memory/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,170p' .context/research/aaif-2026-10-24/third-article/agentmemory-code/consolidation-pipeline.ts; rg -n 'similar|isLatest|concept|1000|s -->
<!-- codex ran: /bin/zsh -lc "rg --files -g 'article.md' -g '"'!agents/**'"' -g '"'!**/agents/**'"' -g '"'!.claude/**'"' -g '"'!**/.claude/**'"' -g '"'!**/node_modules/**'"' -g -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |三層|公司共通|單次交代|常駐指引|平台|domain team|owner|到期日|frozen holdout|授權擴張'"' 2026-10-agentic-harness-blueprint/article.md 2026-09-agentic-org-d -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |oracle|第三種|三種重查|量尺|交付方法|產出超過|審閱能力|replay|PagerDuty|校準|judge'"' 2026-11-same-spec-contract/article.md 2026-11-same-spec-variance/arti -->
中英兩版的正文、圖說與表格已比對完，暫未發現新的實質增漏。另有一處驗收步驟值得收緊：第五節的交錯案例明定重建程序先讀取 J-17，第六節目前只寫「先啟動程序」，未必能測到同一個情況；我會再核對這類條件省略與局部語句。
<!-- codex ran: /bin/zsh -lc "sed -n '74,153p' .context/research/aaif-2026-10-24/third-article/agentmemory-code/auto-forget.ts; rg -n 'rrf|RRF|weight|bonus|60|bm25|vector' .con -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## 二|第三種|共享|誤解|oracle'"' 2026-11-same-spec-contract/article.md | head -n 18; sed -n '232,246p' 2026-11-same-spec-variance/article.md; rg -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
import re
s=Path(\"2026-11-aaif-agent-memory/article.md\").read_text()
for n,line in enumerate(s.splitline -->
<!-- codex ran: /bin/zsh -lc "sed -n '236,246p' 2026-11-same-spec-variance/article.md; rg -n '常駐|單次交代|"'^## 十'"' 2026-11-same-spec-overview/article.md; sed -n '27,36p' 2026-10- -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
import re
s=Path(\"2026-11-aaif-agent-memory/article.md\").read_text()
stack=[]
match={\"」\":\"「\",\"』\":\ -->
本輪仍有 **4 項：必改 0、建議 4、可選 0**。以下不重提前輪已解決或已有充分理由保留的項目。

1. **［建議］§五〈在結果出現前，先決定怎樣才算有支持〉＋「第 35 頁接著把查核……」**

   原文：「要先分清，『版本都保存』才會變成維護決策。」

   問題：「保存版本」是保存紀錄的動作，「維護決策」則是根據紀錄作出的判斷；兩者用「變成」連接，意思過於跳躍。

   建議改法：「要先分清，才能根據保存的各版紀錄作出維護決策。」

2. **［建議］§五〈讓更正沿引用關係，傳到下一份摘要〉＋「我會借用這種主張……」後表格，J-17 列**

   原文：「報表在演練期間暫停、沒有結果卻被整理成全過」

   問題：「暫停」之後接的是帶有轉折的分句，使用頓號容易讀成並列項目；此處宜用逗號。

   建議改法：「報表在演練期間暫停，沒有結果卻被整理成全過」

3. **［建議］§五〈讓更正沿引用關係，傳到下一份摘要〉＋「還有一個會讓舊結論……」**

   原文：「在生效時點前載入舊 context、稍後才輸出的回答」

   問題：前輪同步後，時間關係已交代，但「載入舊 context」直接修飾「回答」，容易讀成由回答執行載入。英文清楚區分了先載入的 context 與稍後產生的回答。

   建議改法：「根據生效時點前載入的舊 context 產生、稍後才輸出的回答」

4. **［建議］§六〈更正有沒有走到回答，要一層一層查〉＋「更正案例就沿用前一節……」**

   原文：「在撤回完成前先啟動一個重建 P-9 的程序，撤回完成後讓它寫回」

   問題：程序先啟動，不代表它已在撤回前讀取 J-17；如果撤回後才讀取，就沒有測到第五節所述的舊版本寫回情況。此處應補回前文已定義的事件順序。

   建議改法：「先讓重建 P-9 的程序讀取 J-17，再完成撤回，最後讓程序寫回摘要」

   英文相應片語同步改為：「have the process read J-17 to start rebuilding P-9, then complete the withdrawal, and only afterward let the process write back the summary」

統計依主要問題歸類，不重複計數：

| 類別 | 項數 |
|---|---:|
| 錯字、同音誤字、漏字、重複字 | 0 |
| 標點 | 1 |
| 斷句與可讀性 | 2 |
| 指涉與承接 | 0 |
| 用詞一致、術語引入 | 0 |
| 前後一致 | 1 |
| 中英對照 | 0 |
| **合計** | **4** |

前輪採用的修正與英文同步已落實，本輪未發現新的實質中英落差、數字矛盾或跨節指錯。剩餘問題集中在局部語句、標點與交錯測試條件的表述；未見明顯錯字、「——」或引號、括號失配。

<!-- tokens: in 1277749 out 12426 -->
