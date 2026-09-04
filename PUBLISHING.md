# 發布到 Medium

`tools/medium_draft.sh` 會把一篇文章的 `publish/medium-paste.md` 灌成一份完整的
Medium 草稿：標題、內文、所有插圖，並在結束前逐塊比對確認沒有掉字。

比對的對象是轉換後的 payload，不是 markdown 原文——轉換本身的正確性由
`tools/test_tools.py` 顧。這一關擋的是「payload 到編輯器」之間會出的錯：
逐塊比對文字、清點連結數（innerText 看不到 `<a>`，掉連結的貼上讀起來一模一樣）、
以及比對每張圖落在第幾個 graf（只數張數的話，圖跑到別的章節照樣「全部相符」）。

```bash
./tools/medium_draft.sh 2026-09-agentic-engineering-platform        # publish/
./tools/medium_draft.sh 2026-09-agentic-engineering-platform en     # publish/en/
```

第二個參數選語言包。省略是預設的 `publish/`，給 `en` 就整包換成 `publish/en/`——
**內文與插圖一起換**。這個參數存在的理由就是後者：只把 paste 檔指到翻譯版、
圖片還是讀 `publish/images`，會把中文圖配到英文文章上，而且後面每一關都還是「全部相符」，
因為它們比對的是轉換後的 payload，不是語言。

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
| 破折號在線上裂成 `— —` | 內文用了中文習慣的 `——`，而 Medium 會在每個 em dash 兩側加 hair space | 內文一律用單個 `—`；`md2medium.py` 遇到 `——` 直接報錯（code block 例外，那裡不會裂） |

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
| `medium_patch.py` | 改**已發布**的文章：找到某幾個 graf、整段換掉、逐處換字串、換圖、刪圖 |
| `medium_draft.sh` | 把上面全部串起來；第二個參數選 `publish/<lang>/` 語言包，並在開瀏覽器前擋掉解析到 repo 外的路徑 |
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
W=$(mktemp -d)                                                     # 別用固定的 /tmp 檔名
python3 tools/medium_patch.py html frag.md > "$W/x.html"           # markdown → Medium HTML
python3 tools/medium_patch.py find "某段開頭"                       # 先確認錨點只中一個
python3 tools/medium_patch.py replace "起" "訖" "$W/x.html" --dry   # 先看會蓋掉哪幾段
python3 tools/medium_patch.py replace "起" "訖" "$W/x.html"         # 真的貼
```

產生的片段會餵進一個登入中的 Medium session，所以別寫到固定的 `/tmp/x.js`——
同機器上任何人都能先把那個檔名佔走或改掉。`medium_draft.sh` 用的就是 `mktemp -d`。

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

### 動手之前先確認「人在哪一篇」

`browse goto` 之後如果頁面還沒換好，接下來的 `eval` 會打在**上一篇**上。
實際發生過：連續處理兩篇英文版時第二次 goto 沒生效，於是 Part 3 的「系列導覽」
被貼進了 Part 2，而且 `replace` 回報 `{"replaced":1}` 看起來完全正常——
因為錨點 `Series:` 在兩篇裡都存在，它確實成功替換了，只是替換錯了文章。

抓到它的是下一步的逐塊比對（66 個區塊不符、圖片位置全錯），不是替換本身。
所以連續處理多篇時，goto 之後、動手之前，先斷言標題是對的再繼續：

```bash
eval "$(python3 tools/medium_js.py selectors)"   # EDITOR_SEL, 不要再抄一份選擇器
WANT="Part 3"                                    # ← 你正要改的那一篇，不是你剛改完的那一篇
guard=$(B js "(()=>{const t=document.querySelector('$EDITOR_SEL .graf').innerText;
               return new RegExp('$WANT').test(t)?'OK':'WRONG:'+t.slice(0,40)})()")
case "$guard" in OK*) ;; *) echo "ABORT: $guard" >&2; exit 1;; esac
```

`WANT` 要填**目標**那一篇的標題片段。填成上一篇的話，這個守衛會在 bug 真的發生時
（頁面還停在上一篇）通過、在 goto 成功時中止——剛好反過來，等於沒有守衛。

教訓有兩層：一是 `{"replaced":1}` 只證明「找到並替換了一個 graf」，不證明
「替換在對的文章、對的位置」；二是**每一步都逐塊比對**的價值就在這裡——
這次是它把錯誤擋在草稿階段，沒有流到讀者眼前。

### 換圖

換一張已經在線上的圖要兩步，因為 Medium 沒有「replace image」：

```bash
# 1. 貼新圖（插在指定那段之前）
python3 tools/medium_patch.py image "圖後面那段的開頭" path/to/new.png
# 2. 等上傳完成——沒傳完之前 <img> 還是 blob URL，這時就刪舊圖會刪錯
#    輪詢到 figure 數 +1 且沒有壞掉的 src 為止（medium_draft.sh 裡有現成寫法）
# 3. 選取舊圖，確認回報的檔名真的是你要刪的那張
python3 tools/medium_patch.py drop "1*舊圖的CDN檔名"
# 4. 讓 Medium 自己的選取生效，再按 Backspace（見下）
```

三件事要注意。

一是 `drop` 只負責**選取**、不會自己按鍵；按之前先確認它回報的檔名是不是你要刪的
那張——這跟 `medium_draft.sh` 是同一個理由。

二是**光用 DOM Range 選取 figure 之後按 Backspace 沒有作用**。Medium 有自己的
一套選取，要先對 `<img>` 送出完整的 pointer/mouse 事件序列
（`pointerdown`／`mousedown`／`pointerup`／`mouseup`／`click`），讓 figure 拿到
`is-selected is-mediaFocused`，Backspace 才刪得掉。所以上面第 4 步不是單純一個
`browse press Backspace`。刪完還會留下一個空段落（`graf--empty`），把游標放進去
再按一次 Backspace 才乾淨。

三是 `image` 一送出 paste 就回傳，**不會等上傳完成**。第 2 步的等待要自己做，
不然第 3 步會在新圖還沒落地時就把舊圖刪掉。

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

一個系列要連續發布時的排法見下面〈把一個系列剩下的篇數發完〉：**能發幾篇就發幾篇**
（2026-09-02 決定，原本是一天一篇）。因為視窗是滾動的，實際上每天常常只空出一個名額。

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
5. 每篇改完都逐塊比對一次，並確認整篇已經沒有 `article*.md` 開頭的 href、
   也沒有殘留的「（即將發布）」／`(coming soon)`。repo 這一側每次都要改**兩份**
   （`article*.md` 與由它產生的 `medium-paste.md`）；只改一份會被 `test_tools.py`
   的 lockstep 掃描擋下來——它比對每一對的連結清單與未發布標記的出現次數。

### 目前的發布佇列（2026-09-02 決定）

中文四篇已於 2026-09-03 全部上線並完全互連。英文版 Overview 與 Part 1 也已上線，
剩下 Part 2、Part 3。

| 順位 | 文章 | Post ID | 狀態 |
|---:|---|---|---|
| — | 總論（中） | `7342ababc417` | 已發布 |
| — | 組織篇（中） | `9d9353ef7f3a` | 已發布 |
| — | 技術篇（中） | `f2a139f5b561` | 已發布 2026-09-02 |
| — | 營運篇（中） | `d6d9623c2dc6` | 已發布 2026-09-03（一上線即完整） |
| — | Overview（英） | `8187e7ec80f9` | 已發布 2026-09-03 |
| — | Part 1 Org Design（英） | `92343384d987` | 已發布 2026-09-04 |
| 1 | Part 2 Harness（英） | `3facc281f633` | 草稿，備妥 |
| 2 | Part 3 Evals（英） | `1cb1855a2046` | 草稿，備妥 |

**能發幾篇就發幾篇**（2026-09-02 決定，原本是一天一篇）。上限允許就繼續發，被擋下來再停。

實際節奏比當初估的慢，因為 24 小時視窗是滾動的、不是自然日，每天真正空出的名額
常常只有一個：09-02 技術篇、09-03 營運篇＋EN Overview、09-04 EN Part 1。

一次要連發兩篇時，順序不能只是「發完再補」：**下一篇發布之前，先把它草稿裡
指向剛上線那篇的連結補好**，它才會一上線就是完整的。補完再發，發完再回頭補
其他已上線的篇。理由見上面第 3、4 點。

一次發兩篇代表訂閱者一天收到兩封信；這是已經確認過的取捨。

中英互連（Medium 沒有原生多語言功能，互連是唯一做法）：每篇英文版的
「Originally published in Chinese」要指向對應中文版，每篇中文版也要加一行指向
英文版。兩邊都要等對方上線才填得進去。

哪幾處還要補，記在各篇的 `publish/PUBLISHED.md` 裡（草稿那幾篇連草稿網址、
已設好的 topics 與封面圖也一起記著）。那些檔案就是這件事的狀態機——
先讀它們，不要憑印象。

## Medium 會改動的排版

Medium 會在**每一個** em dash 前後塞進 hair space（U+200A）。這是它對所有作者
都會做的處理，不是貼上時掉字，`verify_draft.py` 因此會把 em dash 周圍的空白
收回來；一併正規化掉的還有 thin space／hair space／BOM、NBSP、彎引號，
以及 code block 的 `Auto (…)` 語言標籤。連續空白只會被收成一個、不會被刪掉，
所以真的把字黏在一起的貼上失敗還是會被抓到。

**這些排版摺疊只套用在內文，code block 例外。** Medium 在 `<pre>` 裡不做任何
排版改寫（這正是 `——` 在那裡能原樣存活的原因），所以在 code block 裡摺疊不可能
修好 Medium 的改寫，只可能藏住真的改寫——彎引號跑進範例程式碼，讀者複製過去就是
語法錯誤，而這道比對是唯一擋得到的關卡。code block 只會被拿掉語言標籤（那是
Medium 的介面、不是內容）並收合空白。哪些區塊算 code block 是從 payload 那一側
判斷（`<pre>` 開頭），再依位置套到編輯器那一側。

### 破折號一律用單個 `—`，不要用 `——`

中文排版習慣用兩個 em dash 當破折號，但因為 Medium 會在**每一個** em dash
兩側都加 hair space，`——` 上線後會變成 `— —`：本來該是一筆到底的破折號，
中間裂開一道明顯的縫。單個 `—` 則只是兩側各鬆一點，看起來正常。

這件事後面沒有任何一關會攔到——`verify_draft.py` 正是為了不把 hair space
誤判成貼上失敗，才刻意把 em dash 周圍的空白收掉，於是 `——` 會一路過關，
只有讀者看得到。所以檢查放在最前面：`md2medium.py` 遇到 `——` 直接報錯，
連 payload 都不會產出。

**code block 例外。** Medium 不會在 `<pre>` 裡加 hair space，所以 code block
裡的 `——` 上線後就是原樣的 `——`，不會裂開；那裡本來就該用中文的雙破折號。
檢查因此會跳過 fence 內的行——fence 的判斷跟 parser 共用同一組 regex，
免得兩邊對「哪裡算 code block」的認知會分岔。

已發布的文章要改的話用 `medium_patch.py subst` 逐處換，不必整篇重貼。
但要換**兩種形式**，只換一種會以為改完了其實沒有：

```bash
# 1) 算繪後的形式：Medium 把 `——` 存成 HAIR — HAIR — SPACE，兩個 dash 中間隔著
#    hair space，所以直接找 `——` 在內文裡一個都找不到
python3 tools/medium_patch.py subst " — — " " — "
# 2) 原字形式：只有 code block 裡才有，Medium 不會在 code block 加 hair space
#    ——但 code block 的 `——` 是對的，不要動它，所以這一段通常根本不該跑
```

每一種都要迴圈跑到回報 `remaining: 0`。`subst` 找不到字面值時會另外回報
兩件事：`split`（字串跨了兩個 text node，這支工具處理不了）與 `rendered`
（把 hair space 這類隱形字元剝掉之後還數得到幾處）。**兩個只要不是 0／false
就代表還沒改完**，只是你拿去比對的字串形式不對——這兩個回報存在的理由，
就是不讓「找不到」被誤讀成「改完了」。

還有兩個實際踩過的坑：

- **新字串不能包含舊字串**，否則迴圈會一直比中自己剛換上去的結果，永遠不收斂。
  想把 `—X` 換成 `——X` 就是這種情況。繞法是走一個中繼符號：先 `—X` → `⟦DD⟧X`，
  再 `⟦DD⟧` → `——`，兩步都不自我匹配。
- **Medium 會把行內 `` `code` `` 切成獨立的 text node**，即使在 code block 裡也一樣。
  所以錨點跨過一個反引號就會回報 `split: true`；換一個落在同一個 text node
  裡的錨點即可。

---

## 已發布

見 [README.md](README.md) 的文章表，以及各篇的 `publish/PUBLISHED.md`
（英文版另有 `publish/en/PUBLISHED.md`）。
