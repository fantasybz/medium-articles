# 發布到 Medium

`tools/medium_draft.sh` 會把一篇文章的 `publish/medium-paste.md` 灌成一份完整的
Medium 草稿：標題、內文、所有插圖，並在結束前逐塊比對確認沒有掉字。

比對的對象是轉換後的 payload，不是 markdown 原文——轉換本身的正確性由
`tools/test_tools.py` 顧。這一關擋的是「payload 到編輯器」之間會出的錯：
逐塊比對文字、清點連結數（innerText 看不到 `<a>`，掉連結的貼上讀起來一模一樣）、
以及比對每張圖落在第幾個 graf（只數張數的話，圖跑到別的章節照樣「全部相符」）。

```bash
./tools/medium_draft.sh 2026-09-agentic-engineering-platform
```

跑完會印出草稿網址。**它刻意不設 tag、不選封面圖、不發布**——那三件事需要人看過再決定，
而且發布會寄信給所有訂閱者且無法收回。

前置需求：macOS（要用 `security` 讀 Keychain、`openssl` 解密）、`python3`、Chrome 已登入 Medium、gstack 的 `browse`。

---

## 為什麼是這條路

Medium 的 API 早就形同廢棄，所以只能開瀏覽器。中間踩過的坑值得記下來，
因為每一個都會讓流程停在不同的地方：

| 症狀 | 原因 | 解法 |
|---|---|---|
| `medium.com` 回 403 “you have been blocked” | Cloudflare 擋 headless Chromium | `browse --headed`（要先 `browse disconnect`，而且**每一次呼叫**都要帶 `--headed`） |
| 匯入 cookie 後仍然是登出狀態 | `cookie-import-browser chrome` 在 macOS 解不開加密的 cookie，只匯進明文那幾個 | `tools/chrome_cookies.py` 自己從 Keychain 解密 |
| `cookie-import` 整包被拒 | 匯出的 cookie 含 `fantasybz.medium.com` 這種子網域，不是當前頁面網域的後綴 | `chrome_cookies.py` 預設只留 `medium.com` / `.medium.com`（真的要子網域才加 `--subdomains`） |
| 標題開頭少幾個字 | placeholder span 會吃掉最初幾個 keystroke | 標題也用 paste 送進去，不要用 type |
| 小標跟章節標題一樣大 | Medium 把 `<h1>/<h2>/<h3>` 都對到 `graf--h3` | `##` 出 `<h2>`、`###` 出 `<h4>` |
| code block 被切成好幾塊 | `<pre>` 裡的空行會拆 graf | 空行換成一個空白字元 |
| 圖沒進去但流程說成功 | 📌 那行的檔名不符 `[A-Za-z0-9-]+.png`，被當成一般段落 | `md2medium.py` 現在直接報錯，不再默默放行 |

核心手法是**合成 paste 事件**。Medium 的舊版編輯器不檢查 `event.isTrusted`，
所以 `DataTransfer` 上掛 `text/html` 就能一次貼進整篇排版好的內文，
掛一個 `File` 就能上傳圖片。這比逐段模擬打字可靠太多。

---

## 流程各步驟

`tools/` 底下每支腳本都可以單獨跑，debug 時很有用：

| 腳本 | 做什麼 |
|---|---|
| `md2medium.py` | `medium-paste.md` → `{title, html, images}` 的 JSON |
| `chrome_cookies.py` | 從 macOS Chrome 解密匯出某網域的 cookie |
| `medium_js.py` | 產生餵給 `browse eval` 的瀏覽器片段（標題／內文／圖片／placeholder）；另有 `selectors` 子指令，吐出給 shell `eval` 的選擇器變數 |
| `verify_draft.py` | 把編輯器裡的實際內容跟轉換後的 payload 逐塊比對，清點連結數，並比對每張圖落在第幾個 graf |
| `medium_draft.sh` | 把上面全部串起來 |
| `test_tools.py` | 這些腳本的單元測試：`python3 tools/test_tools.py` |

先確認抓得到登入中的 session：

```bash
python3 tools/chrome_cookies.py medium.com --list
# Default      10 cookies  logged in
# Profile 1     8 cookies  logged out
# Profile 2     0 cookies  no uid
```

判斷依據是 `uid` cookie：以 `lo_` 開頭代表那個 profile 是登出狀態。目前登入的是
**Default**，`medium_draft.sh` 寫死用它；換 profile 時改那一行。

第一次跑可能會跳 Keychain 授權視窗（要讀 "Chrome Safe Storage"），按允許即可。

匯出的 cookie 檔是一份可用的登入 session。它建立時就是 0600、放在私有的暫存目錄，
`medium_draft.sh` 跑完會自己刪掉；手動跑的話匯入完就刪。**不要把它或任何
cookie 值貼進 repo。**

---

## 圖片是怎麼進去的

`medium-paste.md` 裡的 `📌【在此插入圖 diagram-01.png】` 會先變成一段
`IMGSLOT-diagram-01.png-ENDSLOT` 的佔位段落，隨內文一起貼進去。之後每張圖：

1. 找到對應的佔位段落，把游標放上去，貼上 PNG。
2. 等上傳完成——沒傳完之前 `<img>` 的 src 還是 blob URL，
   傳完會變成 `cdn-images` 或 `miro.medium` 的網址。同時要數 figure 張數：
   只檢查「沒有壞掉的 src」的話，新的 figure 還沒出現時就會先通過。
3. 刪掉佔位段落：Medium 是把 figure 插在游標段落的**上面**，
   佔位段落還在。第一次 Backspace 清掉選取的文字，第二次刪掉空段落。
   按下去之前會先確認選到的真的是那個 marker——沒選到就中止，
   否則那兩下會吃掉正文。每張圖處理完也會馬上確認佔位段落真的消失了。

順序因此天然正確：figure 落在它原本 📌 標記的位置，最後再由 `verify_draft.py`
用 graf index 驗一次。

---

## 收尾（手動）

草稿好了之後，在 Publish 對話框裡：

1. **Topics** 最多五個。Medium 會改大小寫（`Agentic AI` → `Agentic Ai`），這正常。
2. **封面圖** Medium 預設抓第一張 figure，常常是表格截圖，縮成卡片後字會糊掉。
   換一張圖表比較好。注意 picker 的按鈕順序跟 snapshot 的 `@e` 編號不一定對齊，
   用 img 的 CDN 檔名去比對才不會選錯。
3. **Notify your subscribers** 預設勾選，寄出後收不回來。
4. Publish。

---

## Medium 會改動的排版

`——` 會被塞進 hair space（U+200A）變成看起來鬆一點的長破折號。這是 Medium
對所有作者的 em dash 都會做的處理，不是貼上時掉字，`verify_draft.py` 因此會把
**em dash 周圍**的空白收回來；一併正規化掉的還有 thin space／hair space／BOM、
NBSP、彎引號，以及 code block 的 `Auto (…)` 語言標籤。連續空白只會被收成一個、
不會被刪掉，所以真的把字黏在一起的貼上失敗還是會被抓到。想維持原樣只能在
Medium 編輯器裡逐處手動改，不建議。

---

## 已發布

見 [README.md](README.md) 的文章表，以及各篇的 `publish/PUBLISHED.md`。
