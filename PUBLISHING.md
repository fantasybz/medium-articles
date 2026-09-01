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

一次要發多篇時先看下面的〈發文數量上限〉：Medium 限制同一作者 24 小時內最多
**發布或排程 2 篇**，超過的那幾篇連草稿都建好了也送不出去。

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
| `medium_patch.py` | 改**已發布**的文章：找到某幾個 graf、整段換掉、換圖、刪圖 |
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

## 改已發布的文章

`medium_draft.sh` 只會建新草稿。文章上線之後要改，只能進 Medium 編輯器，
但同一套合成 paste 也能做得很精準——選一段 graf，把新的 HTML 貼上去蓋掉：

```bash
python3 tools/medium_patch.py html .context/frag/x.md > /tmp/x.html   # markdown → Medium HTML
python3 tools/medium_patch.py find "某段開頭"                          # 先確認錨點只中一個
python3 tools/medium_patch.py replace "起" "訖" /tmp/x.html --dry      # 先看會蓋掉哪幾段
python3 tools/medium_patch.py replace "起" "訖" /tmp/x.html            # 真的貼
```

危險的是選取，不是貼上：錨點只要中了兩個 graf（或零個），選到的範圍就會不一樣，
而這是在讀者看得到的文章上動刀。所以每個 snippet 都要求錨點**剛好中一個**，
中了別的數量就回報錯誤而不是猜；`--dry` 會把「將被蓋掉的每一段」印出來再決定。

改完用 repo 既有的那道關卡驗一次最保險：把 `medium-paste.md` 轉成 payload，
再用 `verify_draft.py` 跟編輯器的實際內容逐塊比對。

### 貼上的最後一塊會跟下一段合併

這一條踩過：選取 graf 63–65 貼上「小標＋段落＋code block＋新段落」之後，
**最後那個 `<p>` 併進了選取範圍後面那一段**，變成一段又臭又長的文字，
graf 總數也因此沒有如預期增加。

實測到會不會併，看的是「最後一個貼上的 block」與「選取範圍後面那個 graf」的組合，
而且**不對稱**——不是「同類型才併」那麼簡單：

| 最後貼上的 | 後面那個 graf | 結果 |
|---|---|---|
| `<p>` | `<p>` | **併** |
| `<h4>` | `<li>` | **併** |
| `<li>` | `<h4>` | 不併 |
| `<li>` | `<p>` | 不併 |
| `<p>` | `<h3>` | 不併 |
| `<p>` | `<figure>` | 不併 |
| 任何 | （沒有下一段，貼在文末） | 不併 |

與其背這張表，**可靠的做法是每次都數 graf**：貼之前記下總數，貼完再數一次，
和預期對不上就是併到了，回頭把那一段拆開。把選取範圍往後延伸、讓貼上的內容
結束在標題或圖片之前，通常就能避開。

延伸選取時要注意錨點會不會變得有歧義。實際遇過一次：`三、營運篇（本篇）`
同時出現在文末清單和開頭的「系列導覽」那行裡，`replace` 因此回報
`end anchor matched 2` 而拒絕動作——這正是它該做的事，換一個獨一無二的錨點就好。

### 換圖

換一張已經在線上的圖要兩步，因為 Medium 沒有「replace image」：

```bash
python3 tools/medium_patch.py image "圖後面那段的開頭" path/to/new.png   # 新圖插在該段之前
python3 tools/medium_patch.py drop  "1*舊圖的CDN檔名"                    # 選取舊圖
browse --headed press Backspace                                          # 刪掉
```

兩件事要注意。一是 `drop` 只負責**選取**、不會自己按鍵，按之前先確認回報的檔名
是不是你要刪的那張——這跟 `medium_draft.sh` 是同一個理由。二是用 DOM Range
選取 figure 之後按 Backspace **沒有作用**：Medium 有自己的一套選取，
要對 `<img>` 送出完整的 pointer/mouse 事件序列，讓 figure 拿到
`is-selected is-mediaFocused` 之後才刪得掉。刪完會留下一個空段落
（`graf--empty`），把游標放進去再按一次 Backspace 才乾淨。

存檔按的是 **Save and publish**。它算更新、不算新發布，
所以不會吃掉下面〈發文數量上限〉的配額。

## 發文數量上限

Medium 限制同一作者 **24 小時內最多發布或排程 2 篇**。撞到時 Publish 對話框會出現：

> The author of this story has published or scheduled the maximum of two stories
> in the past 24 hours. Please try to publish or schedule again in 24 hours.

幾件實測過的事：

- **排程不是繞道**。錯誤訊息裡的「or schedule」是認真的：把日期改成明天再按
  Schedule to publish，一樣被同一個計數器擋下來。三篇沒辦法在今晚一次排完。
- 撞到之後 Publish 與 Schedule 兩顆按鈕會變成 disabled，**重新整理才會恢復**，
  不然會誤以為是 UI 壞了。
- 計數器算的是「過去 24 小時」的滑動視窗，不是自然日。所以第三篇要等的是
  **最早那篇發布時間的 24 小時之後**，不是等到隔天午夜。
- 草稿本身不受限：內容、topics、封面圖都可以先設好放著，之後只差按 Publish。

因此一個系列要連續發布時，最省事的排法是**一天一篇**。

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

## 把一個系列剩下的篇數發完

系列文章互相連結，但每篇的網址要發布後才存在，而 Medium 一天只讓你發兩篇
（見上面〈發文數量上限〉）。所以順序是固定的，照著做就不會留下死連結：

1. **發下一篇**。只按該草稿的 Publish，**不要重跑 `medium_draft.sh`**——
   重建會換掉 Post ID 與網址，已發布的那篇還會再寄一次訂閱信。
   topics 與封面圖在建草稿時就設好了，不用再動。
2. **記下它的真實網址**。
3. **回頭補連結**。用 `medium_patch.py` 把其他各篇裡對應的
   「…（即將發布）」純文字換成真正的 Medium 連結；已發布的那幾篇改完按
   **Save and publish**（算更新，不吃發文配額、不會重寄信）。
4. **再發下一篇之前**，先把它草稿裡指向「已經上線的那幾篇」的連結補好，
   這樣它一上線就是完整的，不必事後再改。
5. 每篇改完都逐塊比對一次，並確認整篇已經沒有 `article.md` 開頭的 href、
   也沒有殘留的「（即將發布）」。

哪幾處還要補，記在各篇的 `publish/PUBLISHED.md` 裡（草稿那幾篇連草稿網址、
已設好的 topics 與封面圖也一起記著）。那些檔案就是這件事的狀態機——
先讀它們，不要憑印象。

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
