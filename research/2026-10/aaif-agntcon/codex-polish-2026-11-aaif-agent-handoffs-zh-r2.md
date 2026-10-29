# Codex 校稿 — 2026-11-aaif-agent-handoffs/article.md（第 2 輪）

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-29 03:10. 原話照錄，未經摘要。

我會先核對風格規範與上一輪處置紀錄，再逐段比對中英文，只列出本輪仍存在的問題。全程僅讀取 repository 內的檔案，不做修改。
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-handoffs-zh-r1.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-09/voice_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'cat .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-handoffs-zh-r1-disposition.md' -->
<!-- codex ran: /bin/zsh -lc 'wc -l STYLE.md research/2026-09/voice_brief.md research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-handoffs-zh-r1.md .context/research/a -->
<!-- codex ran: /bin/zsh -lc "sed -n '65,200p' research/2026-09/voice_brief.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-agent-handoffs-zh-r1.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,140p' .context/research/aaif-2026-10-28-polish/2026-11-aaif-agent-handoffs-zh-r1-disposition.md" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.en.md | sed -n '1,139p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.en.md | sed -n '1,75p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.en.md | sed -n '140,237p'" -->
上一輪採用的中文修正已在現稿中落實，處置紀錄列出的幾項英文待同步內容也已更新。我正核對後半部的交接紀錄與驗收情境，確認表格、正文及中英文使用同一套判準。
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.en.md | sed -n '179,195p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.en.md | sed -n '238,296p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.en.md | sed -n '297,370p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.en.md | sed -n '371,431p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '74,168p'" -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path; import re; p=Path(\"2026-11-aaif-agent-handoffs/article.md\"); s=p.read_text(); print(\"雙破折號\",s.count(\" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '168,247p'" -->
目前未發現錯字或「——」；圖說與表格中上一輪要求修正的內容也已對齊。仍需釐清的是少數指涉與動作範圍，例如「節點未被修改」是否專指升級步驟，以及核准失效後禁止送出的，是否僅指新的補救操作。
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '248,313p'" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |''^### |義務表|權威是|辨識力|G2|Quartic|冪等|重啟|跨重|RACI|egress'"' 2026-10-green-overview/article.md 2026-10-green-review/article.md 2026-10-gre -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '314,376p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '377,430p'" -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path; import re; tasks={\"2026-10-green-overview/article.md\":[\"六\"],\"2026-10-green-review/article.md\":[\"六\ -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-agent-handoffs/article.md | sed -n '1,73p'" -->
全文已核對到文末註記，未發現跨節小標或數字指錯，也沒有另需列出的中英實質差異。最後會保留六項問題，集中在動作範圍、指涉與句法；上一輪已解決的項目不再列出。
已核對前輪處置紀錄與現行中英文稿；採用的修正均已落實，未發現由這些修正新增的問題。以下只列本輪仍存在的 **6 項：必改 1、建議 5**；未修改任何檔案。

1. **［建議］§五〈修復之後，重新確認評估與核准〉｜段首「我會把這個設計再延伸」**

   原文：「核准紀錄應對應到哪個叢集、哪一版計畫，以及哪份環境觀察。」

   問題：「應對應到哪個……」留下問句形式，但這裡是在提出設計要求，缺少「寫明對應對象」的完整動作。

   建議改法：「核准紀錄應寫明對應的叢集、計畫版本，以及環境觀察。」

2. **［建議］§八〈共同元件仍需接上業務條件的檢查〉｜段首「三者共同留下的是業務」**

   原文：「不證明核准，時間線與核准紀錄，單獨哪一份都會留下稽核空白。」

   問題：前面已承載多層說明，這裡又用逗號接入另一個判斷；「時間線與核准紀錄，單獨哪一份」也有語序停滯。

   建議改法：「不證明核准。單靠時間線或核准紀錄其中一份，都會留下稽核空白。」

3. **［建議］§八〈讓 task、run 與 tool call 對回同一份授權〉｜段首「一次委託可能經過重試」**

   原文：「在送出前檢查必要條件，並在失敗時阻止動作。」

   問題：「失敗」沒有明說是檢查失敗，容易短暫讀成訂購操作失敗。英文的 `when the check fails` 已明確限定。

   建議改法：「在送出前檢查必要條件，並在檢查未通過時阻止動作。」

4. **［建議］§九〈中斷後如何判斷下一步〉｜段首「接著讓這個操作在目標」**

   原文：「接著讓這個操作在目標系統完成」；「在這個操作上可能多一次驅逐」。

   問題：前文的「升級節點 N」包含三個子步驟，緊接的表格則停在 upgrade 執行中。「這個操作」沒有分清整體流程與子步驟，後面的重跑風險也因此混在一起。

   建議改法：依前表的狀態，第一處改為「接著讓已送出的 upgrade 子步驟在目標系統完成」；第二處改為「若重跑整個節點升級流程，就可能多一次驅逐」。英文的 `this operation` 兩處也應同步區分子步驟與整體流程。

5. **［必改］§九〈中斷後如何判斷下一步〉｜段首「真正困難的切點在中間」；〈哪些結果支持開放操作〉驗收表第三列**

   原文：正文「節點確認未被修改而且健康」；表格「確認未修改且健康才恢復排程」。

   問題：同一情境已明說排空完成、節點停止排程，因此節點並非完全「未被修改」。這裡真正要辨識的是**升級步驟是否已改動節點**；泛稱「未修改」會使恢復排程的條件範圍不清。

   建議改法：正文改為「確認節點未被升級步驟修改，而且健康」；表格改為「確認升級步驟未改動節點且節點健康，才恢復排程」。英文正文及表格的 `unmodified` 同步限定為 `unmodified by the upgrade`。

6. **［建議］§九〈中斷後如何判斷下一步〉｜段首「真正困難的切點在中間」**

   原文：「核准失效之後，三種補救都不能再由 agent 自行送出」。

   問題：第三種補救是「維持隔離，交人處理」，並非必然要送出新操作；「三種補救」與「送出」的搭配把停止、交接也包了進去。

   建議改法：「核准失效之後，補救所需的新操作都不能再由 agent 自行送出」。英文的 `any of the three` 同步改為 `any new remediation operation`。

統計依主要問題歸類，同一項不重複計數：

| 類別 | 項數 |
|---|---:|
| 錯字、同音誤字、漏字、重複字 | 0 |
| 標點與空格 | 0 |
| 斷句與可讀性 | 3 |
| 指涉與承接 | 2 |
| 用詞與術語一致 | 0 |
| 前後一致、正文與表格對照 | 1 |
| 中英實質差異 | 0 |
| **合計** | **6** |

前輪修正後，全文的論述與中英文對應已穩定，圖說、數字及跨節指涉未發現新的錯置。付印前最需要處理的是「未被修改」的範圍，其餘以局部句法與指涉修整為主。未發現「——」或需要更動的引號巢狀、全形括號問題。

<!-- tokens: in 1474278 out 13622 -->
