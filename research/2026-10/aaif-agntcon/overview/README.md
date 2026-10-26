# AAIF 東京筆記系列總覽

這張圖讓讀者在三篇開場看見同一條主線：工具開始行動後，需要知道操作結果；工作交接後，需要分清已完成與待查的部分；經驗留到下一次任務，還要重新檢查來源與適用條件。共同的問題，是讓下一位接手者有依據決定下一步。

依作者要求，中英文三篇開場都加入對應語言的總覽，並另存附有標題、圖例與作者署名的分享圖片。圖中各階段整理自文章分析，不是 AAIF 官方架構，也沒有把不同場次寫成同一次實驗。

| 用途 | 中文 | English |
|---|---|---|
| 獨立分享圖片 | [PNG](series-overview-share.zh-TW.png) | [PNG](series-overview-share.en.png) |
| 文章內總覽 | [PNG](series-overview.zh-TW.png) | [PNG](series-overview.en.png) |
| 向量圖 | [SVG](series-overview.zh-TW.svg) | [SVG](series-overview.en.svg) |
| 可編輯圖稿 | [Mermaid](series-overview.zh-TW.mmd) | [Mermaid](series-overview.en.mmd) |
| 分享版面來源 | [HTML](series-overview-share.zh-TW.html) | [HTML](series-overview-share.en.html) |

圖中的第一篇處理行動授權、外部結果與完成證據；第二篇處理委派、狀態與復原；第三篇處理記憶的來源、版本、適用條件，以及更正與刪除如何影響下一次檢索。最後的藍色節點接回新的任務：接手者依當下條件重新查核，再決定可以交出多少工作。箭頭表達文章論述的接續，不代表所有任務都會依這個順序執行。

來源為[第一篇](../../../../2026-11-aaif-after-tokyo/article.md)、[第二篇](../../../../2026-11-aaif-agent-handoffs/article.md)與[第三篇](../../../../2026-11-aaif-agent-memory/article.md)。第一篇以 App crash 調查推導判斷；後兩篇沿用 Kubernetes 升級的假設情境。總覽沒有將兩個案例合併為作者親歷。

## 版面與檢查

依 [MERMAID.md](../../../../MERMAID.md) 製作，使用 Mermaid 11.17.2；圖內字級為 16 px，字型由算繪工具注入。每張圖有 7 個節點，每個節點最多 3 行，中文每行不超過 14 字。標題、圖例與作者資訊放在分享版面外框，沒有塞進圖內節點。

| 語言 | SVG viewBox | 高／寬 | 文章 PNG | 分享 PNG |
|---|---|---:|---|---|
| 中文 | 546×796 CSS px | 1.46 | 1156×1664 px | 1360×2440 px |
| English | 741×796 CSS px | 1.07 | 1546×1664 px | 1640×2342 px |

算繪沿用 repo 的檢查腳本；本次工作區副本另在截圖前，將 SVG 的實際寬高設為 viewBox 尺寸，避免百分比寬度在容器中縮成 300 px。PNG 以兩倍解析度輸出，正文發布包的 `diagram-01.png` 與對應語言總覽逐位元相同。照片來源與 story image 保持原有選擇。

中文圖中文字、圖例及新增導讀已另行送交 zh-TW MCP，結果為 0 errors、1 warning、2 info。提示分別涉及圖內三個獨立標籤被連成一句、圖例的名詞用法，以及確實對應三篇的階段敘述，核對語境後保留。三份中文原稿及三份 Medium 貼稿也完成全稿 MCP 檢查，均為 0 errors；警告與提示保留在本輪核對紀錄，不稱為全部無警告。

兩張最終分享 PNG 已逐張檢視，確認標題、三個階段、連線、圖例及署名完整且可辨識。文章內的總覽與分享圖使用相同的圖稿，三篇同語言發布包中的總覽 PNG 雜湊一致。

截至 2026-10-24，圖片可獨立分享，三篇中英六版均已排程。第三篇中文為 11/16、英文為 11/18，皆為臺北時間上午 9 點；第一、二篇維持原有時段。文章仍未公開，實際狀態見[發布紀錄](../publication.md)及各篇 `publish/PUBLISHED.md`。
