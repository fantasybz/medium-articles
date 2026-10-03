# 2026-10-03：補上四份 spec 的全文入口

作者指出，讀者找不到 A0／A／B／C 全文，就無法自行核對差異。本次把四份凍結原文連結放到規格篇第三節開頭，也在總論與變異篇首次介紹四份規格時提供入口，並同步三份 Medium 貼稿。

新增[全文與逐行差異導讀](../../experiments/same-spec-ten-runs/SPECS.md)，說明各份內容、閱讀順序、十三條要求的主題、規格與完整任務輸入的區別。三組 diff 直接由凍結原文產生；已實際套用差異，確認各自能逐 byte 還原下一份檔案。B 保留 A 全文、C 保留 B 全文也已核對。A0／A 的 CLI 範圍差異另行說明，沒有把四份文字寫成語義完全等價。

## 最新文字版本

| 文章 | 正文 SHA-256 | 貼稿 SHA-256 | MCP 提示數（正文／貼稿） |
|---|---|---|---|
| overview | `54499176d9eded4875cbaf7e61054c722aaf1ba555b45e07e9099d01ad35f497` | `032c41c16a970a70f0b5ab0b420ed0e254c49efc75852376cf630a6cbce4822e` | 49／49 |
| spec | `7284e7e2f3550d3b774730c3ed20aac8b77d441d4841cb1a7a01b3db6aba67b4` | `ed9de0669be34c86bc66db6d9c8fd287462412676761e85be9f3c5b773f9f39e` | 43／42 |
| contract | `ceae48f523483da89cffbed7e9f941098ab36caa129845567229d461598a49f0` | `170f12fdaadae7f636db6830aff03a95c732e1d5c63fd7b110ad9e7f831cb4ac` | 52／51 |
| variance | `7c65b972f8cb70168f0cb58a5a3d5036d56a40f6b54b5eb2bc9d9180600b41b8` | `6bc05e38c9700bbad498bfeb303202b8fd020fe80a569a641117f37f2695a776` | 48／46 |

三篇更新正文、三份貼稿與新增導讀，共七份重新執行 strict zh-TW MCP，均為 0 錯誤、0 警告，回傳文字與輸入逐字相同。沿用 AI 敏感度 low、翻譯腔、風格、一致性、verify 與零警告門檻，沒有擴大忽略詞清單。契約篇兩份文字未改，雜湊仍符合[前輪語言紀錄](readability-2026-10-03/quality-record.md)。新增提示依語境保留：三步比較適合平行列表，「開頭」不是 C/C++ header，「通過」指 pass。

四份貼稿與轉換器逐 byte 相符，所有全文與導讀連結都保留在貼稿文字中，本機連結目標存在。程式碼區塊、圖表索引與 29 張 PNG 都未改。Repo 工具測試 301 項、research scripts 測試 121 項通過，正式封存索引及 317 個檔案 SHA-256 一致。詳細版本、原始 spec 與 diff 指紋見 [JSON 紀錄](spec-access-2026-10-03.json)。

本次由 Codex 主代理補充入口與導讀；沿用既有 Claude Code max 主稿，未新增主寫、獨立代理審查、研究樣本或視覺檢查。所有連結目前都是 repo 內附件；固定版本的公開網址、未登入可讀性與 Medium 發布仍未完成。完整語言回應、修改前快照及測試輸出留在本機 `.context/same-spec-ten-runs/spec-access-2026-10-03/`。
