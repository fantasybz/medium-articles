# Codex 校稿 — 2026-11-aaif-agent-handoffs/article.md（第 3 輪）

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-29 03:32. 原話照錄，未經摘要。

我會先讀寫作規範與前兩輪處置紀錄，核對已採用的修正，再逐段比對中英文；全程只讀，不修改檔案，也不存取你列出的禁讀目錄。
<!-- codex ran: /bin/zsh -lc pwd -->
<!-- codex ran: /bin/zsh -lc 'wc -l 2026-11-aaif-agent-handoffs/article.md 2026-11-aaif-agent-handoffs/article.en.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-handoffs-zh-r2.md .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-ha -->
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md research/2026-09/voice_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-handoffs-zh-r1.md .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-ha -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-09/voice_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-handoffs-zh-r1-disposition.md' -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^#|''^'"\\*\\*|"'^[0-9]+'"\\.|原文|問題：|建議改法|統計' research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-handoffs-zh-r2.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^#|''^'"\\*\\*|"'^[0-9]+'"\\.|原文|問題：|建議改法|統計' research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-handoffs-zh-r1.md" -->
<!-- codex ran: /bin/zsh -lc "nl -ba .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-handoffs-zh-r1-disposition.md | sed -n '55,148p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.en.md | sed -n '1,158p'" -->
第二輪的六項修正已落實，英文對應處也已同步；「整個升級流程」與 upgrade 子步驟的區分，目前沒有新增矛盾。我會接著檢查後半部的操作契約、表格，以及跨篇引用的節次。
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.en.md | sed -n '159,280p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.en.md | sed -n '281,431p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '74,167p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '168,281p'" -->
目前中英文的主張、數字與表格內容相符，未發現需要重提的前輪退回意見。剩下幾處可能影響閱讀的句法與指涉，我會再核對上下文，只保留有具體理由需要修改的項目。
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.en.md | sed -n '350,354p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '282,376p'" -->
<!-- codex ran: /bin/zsh -lc "rg --files -g article.md -g '"'!agents/**'"' -g '"'!.claude/skills/**'"' -g '"'!**/agents/**'"' -g '"'!**/.claude/skills/**'"'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '377,430p'" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |''^### |權威是|三道|G2|重啟|Quartic|egress|secret|RACI|義務表|高風險|擴大'"' 2026-10-green-review/article.md 2026-10-green-overview/article.md 2026 -->
<!-- codex ran: /bin/zsh -lc "rg -n -i 'tenant|token|hour|repo/docs|scope' .context/research/aaif-2026-10-23/slides/text/*pingcap*" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## 三|''^## 六|secret|egress|短效|短期|無法繞|不可繞|identity_broker|identity broker'"' 2026-10-agentic-harness-blueprint/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## 六|三道閘|''^## 五|Quartic|''^## 九|跨重啟|provider|保存期限'"' 2026-10-green-overview/article.md 2026-10-green-testing/article.md 2026-10-green-p -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
import re
s=Path(\"2026-11-aaif-agent-handoffs/article.md\").read_text()
print(\"雙破折號\", s.count(\"——\"))
 -->
已核對前兩輪處置紀錄與現行中英文稿；採用的修正均已落實，未見修正衍生的新問題。以下只列本輪仍存在的 **2 項，均為建議**；未修改任何檔案。

1. **［建議］§七〈檔案各自正確，合起來仍可能違反任務要求〉｜段首「用名額讓操作依序執行」**

   原文：「也因為身分已不是持有者而被拒絕」

   問題：本段的「身分」已明確指這輪 run 的執行識別；這裡卻改用「身分」表示持有者角色，容易混淆識別與角色。直接以 A 為主詞即可。

   建議改法：「也因為已不是目前持有者而被拒絕」

2. **［建議］§八〈共同元件仍需接上業務條件的檢查〉｜段首「三者共同留下的是業務」**

   原文：「每一跳如何縮小，仍要自己建。」

   問題：前面列的是三個待解決的問題，「建」的對象卻省略了；實際要建立的是處理這些問題的機制。英文對應句已有 `build their own mechanisms`，意思較完整。

   建議改法：「每一跳如何縮小權限，相關機制仍要由團隊自己建。」

統計依每項主要問題歸類，不重複計數：

| 類別 | 項數 |
|---|---:|
| 錯字、同音誤字、漏字、重複字 | 0 |
| 標點與空格 | 0 |
| 斷句與可讀性 | 1 |
| 指涉與承接 | 0 |
| 用詞與術語一致 | 1 |
| 前後一致、數字與跨節指涉 | 0 |
| 中英實質差異 | 0 |
| **合計** | **2** |

前兩輪修正後，全文、圖說、表格與中英文對照已相當穩定，未見新的必改問題。剩餘兩處是局部用詞與動作對象的補正；引號巢狀、全形括號及單一破折號的使用均未發現問題。

<!-- tokens: in 1397353 out 12815 -->
