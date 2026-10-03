# 2026-10-03 版本與驗證紀錄

本頁記錄讀者回饋修訂後的實際檢查；不表示作者已認可品質，也不表示已在 Medium 發布。完整版本資料見 [quality-record.json](quality-record.json)。

| 文章 | 正文 SHA-256 | 貼稿 SHA-256 | strict zh-TW MCP（正文／貼稿） |
|---|---|---|---|
| overview | `198d6ffd082bc73a244eee6ecf2286e0148db71a036a73706eb0f52aa4e0e596` | `d6f199384e51559ee1f4156fbb332f813cf91af8ab38ba2044435fc6eb308e0f` | 0 錯誤、0 警告；提示 49／49 項 |
| spec | `5753304291d0a4dffa0bedd11b65ecf22b63ac6be186429e2ae0d0cd80443a8c` | `6a705eeabe3971e19cadd9506b9f0931d688866a1ac078ce51b064c0104869d1` | 0 錯誤、0 警告；提示 42／41 項 |
| contract | `ceae48f523483da89cffbed7e9f941098ab36caa129845567229d461598a49f0` | `170f12fdaadae7f636db6830aff03a95c732e1d5c63fd7b110ad9e7f831cb4ac` | 0 錯誤、0 警告；提示 52／51 項 |
| variance | `da207fbc266bf9d903698f76713cb5eefa4d59e44a04e4b67cf1b44da9ac374a` | `b435f5627a31d8577332fa7b0f9b18c6f400cbfc4d1454818f4a5d0aa3b733a0` | 0 錯誤、0 警告；提示 48／46 項 |

八份文字都使用與 9/28 相同的 strict 設定，開啟 AI、翻譯腔、風格、一致性與 verify，錯誤與警告門檻皆為 0；回傳文字與送入文字完全相同。沒有擴大忽略詞清單；提示項按語境處理，詳見 JSON 的 info_review。verify 是實際請求的選項，不等於每一則提示都有外部驗證。

四份貼稿與轉換器輸出逐 byte 相符，圖表索引一致，本機相對連結目標存在。所有程式碼／Mermaid 區塊、表格文字與連結目標，均與本輪修改前一致。29 張 PNG 的 SHA-256 也與 9/28 公開紀錄一致，故沿用圖檔，沒有宣稱重新繪圖。

本機預覽檢查四篇的 1280 × 900 與 390 × 844 版面，圖片均載入，沒有水平溢位；主代理檢視了八張概念段落／結語截圖。截圖存於本機 `.context/`。這不是遠端 Medium 驗證，也不保證手機縮小後的寬表細字可讀。

工具測試 301 項、research scripts 測試 121 項通過；正式封存索引及 317 個檔案 SHA-256 全數相符。教學程式與示意程式未改，本輪沒有把 9/28 的教學重播寫成新實驗。

主稿仍來自 9/28 實際成功的四個 Claude Code Opus 5.5 max 請求；本輪由 Codex 主代理修訂，未新增 Claude 主寫或獨立代理審查。原主稿版本指紋與請求設定保存在[前輪紀錄](../rebuild-2026-09-28/quality-record.md)。
