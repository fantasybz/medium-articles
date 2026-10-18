# 2026-10-03：公開附件與固定版本連結

四份 spec、逐行差異、完整任務輸入與研究資料，已推到既有的 public repo `fantasybz/medium-articles`。附件固定在 commit `774759192ab0e0b2da3d8b163eb3f07f3d12f4c3`，入口是[全文與逐行差異導讀](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/experiments/same-spec-ten-runs/SPECS.md)。四篇中文稿及貼稿均已把研究附件改成固定版本網址；成稿狀態頁保留分支連結，方便持續更新。

## 公開可讀性

已用 gstack `/browse` 在未登入的 GitHub 頁面開啟導讀，確認 A0／A／B／C 四個入口均指向同一次提交。另以 `credentials: omit` 下載 36 份附件，全部回傳 HTTP 200，SHA-256 與提交內容逐一相符。核對範圍包含四份 spec、四份 packet、system prompt、三組 diff、比較指紋與文章引用的其他研究檔案。檔案原文不因建立公開連結而改寫。

## 最新文字與驗證

| 文章 | 正文 SHA-256 | 貼稿 SHA-256 | MCP 提示數（正文／貼稿） |
|---|---|---|---|
| overview | `d9c7cf8928ed7562be3d36dd8b3cdb97d45f221354027764916c288d2476d2dc` | `f0ca9da1bbfd0c90743ac27f327a45a66d8b0cdb84f8d7012f772701f17d7aba` | 49／49 |
| spec | `ffd453e40eaab9ed6210fb1fc782d52baf65441a075a62035144525bf1fa3852` | `bd31b7a98dd80eaeb26db7d059c6a0b2f3ac17428c26263ae8c3d09c24f17699` | 43／42 |
| contract | `778c9f40f83ef5d0f75f3aa6b7cf74e89f2438cb0ee92c2d6dd3081f4b346e99` | `03d82f35c91aba339d3e47204d752eba2b84898cd6589246675d3b8a746b708e` | 52／51 |
| variance | `daedac357e46ba7c966b9f37ed99ed12bd58a60904beb77271ad31aaac97e29e` | `a753226fdcac00c43d84b779e005425d615f1017d16d5a23e3b23148782b3cd0` | 48／46 |

四篇正文、四份貼稿與導讀，共九份最新文字均通過實際 strict zh-TW MCP，為 0 錯誤、0 警告，回傳文字與輸入相同。沿用 AI 敏感度 low、翻譯腔、風格、一致性、verify 與零警告門檻，沒有增加忽略詞；提示依語境審閱。

四份文章僅更換研究連結，反向替換後與修改前正文逐 byte 相符。四份貼稿與轉換器一致，圖表索引、29 張 PNG 及正式封存的 317 個檔案雜湊均相符。301 項工具測試、121 項研究腳本測試及 83 項實驗工具測試通過。實驗目錄第一次選到系統 Python 3.9.6，低於文件要求而失敗；指定與封存相同的 Python 3.14.5 後全數通過，未修改實驗程式來繞過版本檢查。

為保留科學圖表、歷史工具回應與逐行差異的原始位元組，`.gitattributes` 僅針對這些既有工件設定空白檢查例外，沒有重寫封存內容。推送 hook 未略過；抽查非阻擋提示，對應到章節編號、量測數字及圖形座標；另逐一定位唯一的 wallet 與 env 提示，分別是語言檢查識別碼與正規表示式。這不等於逐筆語意審閱全部 2,043 項提示；另外執行的憑證格式掃描沒有匹配項目。

詳細網址、版本與檢查結果見 [JSON 紀錄](public-links-2026-10-03.json)。[前輪全文入口紀錄](spec-access-2026-10-03.md)保留尚未推送時的狀態與雜湊。本次完成 GitHub 分支推送與附件連結，未合併 main，尚未建立 Medium 遠端草稿或發布；也沒有新增研究樣本、Claude 主寫或獨立代理審查。
