# Codex 校稿 — 2026-11-aaif-after-tokyo/article.md（第 3 輪）

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-29 00:39. 原話照錄，未經摘要。

我會先讀 STYLE.md、口吻摘要與前兩輪校稿及處置紀錄，再逐段核對中英文稿；全程只讀取此 repository 內的檔案，不修改任何內容，也不讀取你列出的禁用路徑。這輪只列仍存在的問題，並優先檢查已採用的修正是否引入新問題。
<!-- codex ran: /bin/zsh -lc pwd -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-after-tokyo-zh-r1.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-after-tokyo-zh-r1-disposition.md' -->
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-09/voice_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-after-tokyo-zh-r2-disposition.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-after-tokyo-zh-r2.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-09/voice_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-aaif-after-tokyo/article.md 2026-11-aaif-after-tokyo/article.en.md research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-after-tok -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-after-tokyo-zh-r1.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,169p' 2026-11-aaif-after-tokyo/article.en.md" -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-after-tokyo-zh-r1-disposition.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-after-tokyo-zh-r2.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,100p' 2026-11-aaif-after-tokyo/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,45p' research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-after-tokyo-zh-r2.md" -->
前兩輪採用的修正已在現稿中核對到，英文也已同步第 2 輪的來源說明。作者不採用的三處意見，我會依處置理由保留；接下來重點核對後半部表格、結語與中英文的條件及語意。
<!-- codex ran: /bin/zsh -lc "sed -n '170,267p' 2026-11-aaif-after-tokyo/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '268,363p' 2026-11-aaif-after-tokyo/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '364,465p' 2026-11-aaif-after-tokyo/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '466,533p' 2026-11-aaif-after-tokyo/article.en.md" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.md | sed -n '1,168p'" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |Org|Repo|Dir|golden tasks|白名單|legibility'"' 2026-10-agentic-harness-blueprint/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |red-then-green'"' 2026-10-green-testing/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |G2|G3|frozen holdout|constraint tests|Red Line Rate'"' 2026-10-green-reliability/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '170,267p' 2026-11-aaif-after-tokyo/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |G2|G3|LLM-as-judge|人工抽查'"' 2026-11-agentic-eval-economics/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |規格修改卡'"' 2026-11-same-spec/article.md 2026-11-same-spec-variance/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg --files -g article.md -g '"'!**/agents/**'"' -g '"'!**/.agents/**'"' -g '"'!**/.claude/**'"' 2026-09* 2026-11*" -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path; import re; s=Path(\"2026-11-aaif-after-tokyo/article.md\").read_text(); print(\"雙破折號\", s.count(\"——\")); -->
兩版的表格、主要數字與結尾狀態已核對，未見新的實質中英落差；第十一節也已說清楚「暫緩」看數量、「修補」看比例的區別。目前只留下少數局部用語與標點疑點，正在核對跨篇節次，並刪除純屬偏好的修改。
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |規格修改卡|預期改善|撤回條件'"' 2026-11-same-spec-spec/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |委派|完成|人工投入|品質'"' 2026-09-agentic-engineering-platform/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '268,389p' 2026-11-aaif-after-tokyo/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '390,532p' 2026-11-aaif-after-tokyo/article.md" -->
全文與跨篇節次核對完成，前輪採用的修正未見新問題，也未發現「——」、引號或括號不成對。這輪保留三處局部句法與動作對象的建議；其中「重現原因」在英文也有相同用法，若採用修正，兩版需一起調整。
<!-- codex ran: /bin/zsh -lc "rg -n '哪個觀察足以支持哪個結論|決定由誰作出的約定|尚未重現原因|cause not yet reproduced|judgment of which observation|agreement about who makes the decision' 2026-11-aaif-a -->
已核對前兩輪處置、中英文全文、圖說、表格、Mermaid 文字與文末註記；未修改檔案。前輪採用的修正已落實，未見新增問題；不採用的意見不重提。本輪保留以下 3 項。

1. **［建議］§四〈讓回饋能分辨真正的改善〉＋段首「分群之後仍可能有偏差」**  
   原文：「哪個觀察足以支持哪個結論，仍來自團隊對問題的理解。」  
   問題：前半提出待判斷的問題，直接接「仍來自」，句法略有懸空；來自團隊理解的是對證據的判斷。  
   建議改法：「哪個觀察足以支持哪個結論，仍要靠團隊對問題的理解來判斷。」

2. **［建議］§五〈驗證更新時，把授權要求留在比較裡〉＋段首「程序效果因此還要另外驗證」**  
   原文：「決定由誰作出的約定已經變了。」  
   問題：「決定」容易先被讀成動詞，讀到「約定」才需要重新解析；調整語序即可清楚表達決策者變更。  
   建議改法：「由誰作決定的約定已經變了。」

3. **［建議］§十二〈離開澀谷之後〉＋段首「我在《綠燈不是驗收》」**  
   原文：「已確認影響範圍，尚未重現原因」  
   問題：「重現」的對象應是閃退現象；原因則是調查、確認的對象。此處也未沿用第八節「重現原來的錯誤」的說法。這是作者自擬的報告示例，不是他人引文。  
   建議改法：「已確認影響範圍，尚未重現閃退」  
   英文同處的「cause not yet reproduced」同步改為「crash not yet reproduced」；這是兩版共有的搭配問題，不計為中英意思差異。

各項依主要問題計一次：

| 類別 | 項數 |
|---|---:|
| 錯字、同音誤字、漏字、重複字 | 0 |
| 標點 | 0 |
| 斷句與可讀性 | 3 |
| 指涉與承接 | 0 |
| 用詞、術語一致 | 0 |
| 前後一致 | 0 |
| 中英實質意思差異 | 0 |
| **合計** | **3** |

嚴重程度：**必改 0、建議 3、可選 0**。未發現「——」、引號巢狀錯誤或括號不成對。

全文的作者口吻、證據界線與跨節承接已相當穩定。這輪餘項都是局部句法與動作對象的精修，無須調整主張或結構。

<!-- tokens: in 1781364 out 8965 -->
