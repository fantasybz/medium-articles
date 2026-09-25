<!--
Medium 發布指南（此註解區塊不要貼進 Medium）

自動化：`./tools/medium_draft.sh <article-dir>` 會建好草稿並比對內容，停在發布前一步。
細節見 repo 根目錄的 PUBLISHING.md。以下是手動流程與發布後必做的收尾。

【系列狀態】以各篇 publish/PUBLISHED.md 為準。Medium 限制同一作者 24 小時內最多發布或排程 2 篇，
見 PUBLISHING.md 的〈發文數量上限〉。

【手動流程】
1. 開新 story：https://medium.com/new-story
2. 貼上下方內容（從標題那行開始，不含本註解）。
3. 看到 📌【在此插入…】的行：刪掉該行，按 + 插入同目錄 images/ 裡對應的 PNG。
4. code block：在 Medium 選取後按 ``` 轉成 code block。
5. 封面圖選流程圖，不要選表格截圖（縮到卡片尺寸看不清）。
6. Tags 建議：AI, Software Engineering, Engineering Management, Agentic AI, DevOps

【發布後收尾—不做的話系列會斷】
7. 記下本篇 Medium URL，補進 repo 的 README 索引與 publish/PUBLISHED.md。
8. 把本篇兩處的系列連結換成真正的 Medium URL：
   (a) 開頭「系列導覽」那一行
   (b) 文末「系列文章」清單
   （尚未發布的篇在這裡是純文字「（即將發布）」，不是相對路徑；上線後換成真正的 URL）
9. 回頭編輯已發布的其他篇，把指向本篇的連結補上。
-->

# 綠燈不是驗收（四）付款實作篇：買一瓶無糖純喫綠茶，從 Review 約束走到 mutation score

> **TL;DR** — 想買一瓶無糖純喫綠茶，付款畫面卻遲遲沒有回應。再按一次會不會多扣一筆？這篇用一筆示範售價 35 元的訂單，把「綠燈不是驗收」的三道閘串起來：先依風險挑選 reviewer 與需要深讀的變更，再從 Review 意見中挑出值得長期保護的約束，把它們寫成測試，最後選擇相關程式碼做 mutation testing。隨文附上可執行的 Python 範例。實際執行七個指定 mutant，只測正常購買時殺死 2 個，mutation score 是 28.6%；補到 8 個測試、只缺逾時案例時，分數已達 85.7%，卻仍抓不到「把不確定的付款標成成功」；完整 9 個測試辨識出這七種變異。100% 只描述這次選定的範圍，也不能替並行、重新啟動與真實金流整合作保。

> 系列導覽：[總論：綠燈不是驗收](https://medium.com/p/582f24223eea) → [一、測試篇](https://medium.com/p/b01055139451) → [二、Review 篇](https://medium.com/p/ccbf0cbe2691) → [三、可靠度篇](https://medium.com/p/3c64a9622777) → **四、付款實作篇（本篇）**。本篇可以獨立閱讀，總論與前三篇則提供方法的研究背景與組織安排。

---

## 一、先把那一瓶綠茶買清楚

先想像一個很小的情境。你選了一瓶無糖純喫綠茶，確認金額，按下付款。畫面轉了一會兒，沒有顯示成功，也沒有明確說失敗。你手指停在付款按鈕上，接下來那一下，到底是在查詢上一筆交易，還是重新付一次錢？

這是為了教學而設計的情境，不是我的事故紀錄，也不是特定商家的付款實作。以下把示範售價設成 **35 元新台幣**，不代表商品的實際售價。金額以整數「元」表示；折扣、稅額、其他幣別與找零先不放進這個例子。

我想讓這一瓶綠茶承擔一件事：把抽象名詞還原成可以觀察的結果。對購買的人來說，期待很具體：訂單裡是無糖綠茶，金額是 35 元，不會因為重按按鈕多付一次，也不會在商家還不知道付款結果時，就收到一張宣稱成功的收據。

範例的起點，是後端已經完成身分授權、從伺服器讀出的訂單。商品代碼 SKU 用來辨識品項；`order_id` 辨識訂單；`key` 是這次付款嘗試的 idempotency key，讓重送的請求能對回同一次操作。這三個識別不能混為一談，也不把瀏覽器傳來的任意價格當成權威資料。

```python
# 示範資料：已授權、由伺服器讀出的不可變訂單。
# 完整程式在 examples/tea_payment/，不會呼叫真實金流。
order = Order(
    order_id="tea-001",
    sku="UNSWEETENED_PURE_GREEN_TEA",
    amount_ntd=35,
)
key = "buy-tea-001"
```

先由人確認這份付款契約，再請 agent 實作。正常付款要把訂單金額送到金流端，收到成功回覆後回傳 `PAID`，收據保留同一個訂單、SKU、金額與付款識別。相同訂單與 key 再送一次，要取得既有結果，不再發出新的扣款請求。key 不能移到另一張訂單；已開始付款的訂單，也不能靠換一個 key 或改寫內容重新開始。

拒絕與逾時則要分開。明確拒絕是 `DECLINED`；逾時只是我們沒有收到確定的回覆，金流端可能已經扣款，因此維持 `PENDING`。這份示範不會在逾時後自動重新扣款，也沒有實作查詢與對帳流程；後續必須由另外設計、驗證過的流程處理。

這些是本例約定的行為，不是所有金流 API 共同採用的狀態名稱。[Stripe 的官方文件](https://docs.stripe.com/error-handling#connection-errors)也提醒，連線錯誤留下的是不確定結果；但在它的 idempotency 契約下，可以使用相同 key 安全重試。這份示範沒有實作 provider 端的冪等能力，因此先保留待確認結果。兩者的差別在於重試受到什麼保證，不能把這裡的保守處理推成「真實金流一律不得重試」。

---

## 二、先挑誰來 Review，再決定要讀哪裡

假設 agent 送來一個 PR，說明是：「付款 API 現在支援重送，相同請求會拿到既有結果。」這句 intent 讓 reviewer 知道目標，卻還沒有回答實作是否達到目標。

我會先看改動碰到什麼責任：訂單識別、金額、扣款呼叫、付款狀態，以及用來驗收它們的測試。這些共用邏輯可能影響許多筆訂單，所以不能因為眼前的綠茶只值 35 元，就把整個 PR 當成低風險改字。反過來說，若 PR 真的只修改不影響付款流程的說明文字，也不該只因資料夾叫 `payment` 就要求相同深度的審查。

下面是這個付款邏輯 PR 的分工建議。角色可以由同一位具備相應能力的人兼任；需要的是責任與能力，不是湊滿職稱。

📌【在此插入表 table-01.png】

Reviewer agent 可以先整理 diff、找出扣款呼叫與例外處理，或提出反例，讓人更快進入問題。但它不能自行確認付款契約，也不能把自己的 approve 當成人類核准。沿用 Review 篇的建議，高風險付款邏輯由任務指派者以外、具備相關責任的人核准。

具體挑 hunk，也就是 diff 裡的一段變更時，我會優先讀「既有付款是否存在」的判斷、「哪一個金額被傳給金流」、「例外如何變成付款狀態」，以及這幾處相連的呼叫者。不能只讀被改色的那一行：guard 的位置、資料從哪裡來、例外在哪裡被吞掉，都可能在相鄰的程式碼裡。測試與驗證設定的變更也要一起看，確認這份綠燈沒有靠放寬斷言取得。

[Google 的 Code Review 指引](https://google.github.io/eng-practices/review/reviewer/looking-for.html)要求 reviewer 理解受託審閱的程式碼、必要時擴大閱讀脈絡，並找具備相應能力的人處理專門問題。上面的三種責任是我依付款情境提出的分工，不是 Google 規定的三人編制。誰只審了測試、誰確認了付款狀態，都應在核准紀錄裡寫清楚。

如果目前只有正常購買的測試，這個 PR 還缺少足夠的可機器驗證證據。我會先深入審閱相關 diff，補出重要約束；等報告真的涵蓋了那些要求，才有依據調整往後的審閱方式。不能先把人撤掉，再希望分數補上原本沒有人確認的事情。

---

## 三、哪些 Review 意見值得留下來變成測試？

現在假設 reviewer 留下幾則評論。以下都是教學用的評論，不是從某個真實 PR 複製出來的紀錄。

第一則問：「相同訂單連按兩次，會不會發出兩次扣款？」第二則問：「如果重試時 key 被換掉，或被拿去付另一張訂單呢？」第三則提醒：「逾時之前，金流端可能已經扣款。」另外還有兩則：「這個區域變數換個名字比較清楚」與「這個活動要不要提供退款？」

它們都可能有價值，但要走向不同的下一步。挑選的依據不是評論寫得多長、按讚數多少，也不是只收集曾經造成事故的問題。我會依序確認：它想避免什麼後果、要求是否跨越這次 PR 仍然成立、預期結果由誰確認，以及能否用穩定、可維護的方式觀察。

📌【在此插入表 table-02.png】

一條高影響的要求，即使第一次被提出，也值得保護；不必等第二次扣錯款才算「反覆出現的規則」。另一方面，單次遷移的暫時限制可能只需要有期限的檢查，不應永遠留在 CI 裡。

挑中的評論還要改寫成一張可追問的規則卡。以 C4 為例，來源是本次示範 Review 的「回覆遺失」風險，適用範圍是付款嘗試與重送，要求是「逾時維持結果未知，不標示成功，也不自動再扣一筆」。測試名稱是 `test_timeout_stays_pending_without_another_charge`；維護責任由 payment owner 承擔；provider 契約或對帳流程改變時，重新檢視這條規則。

真正的團隊應補上實際 PR、需求或事故的連結。`owner` 不是為了填欄位，而是讓下一位 reviewer 知道誰能解釋或修改預期結果。很久沒失敗，也不能單獨成為刪除付款安全規則的理由；可能正是因為規則持續有效，錯誤才沒有再進來。

---

## 四、把約束寫成會辨識錯誤的測試

**Constraint tests 描述的是測試的來源與保護責任，不是一種與功能測試互斥的技術。** 「同一筆付款不能重複扣款」既是產品行為，也是 reviewer 決定長期保留的約束；可以用 unit test、integration test 或其他合適的檢查來實作。把兩者分開報告，有助於追蹤責任，不能因此宣稱它們保護的是完全不同的世界。

本例先有兩個正常購買的測試：收據保留無糖綠茶的 SKU、35 元與付款識別；假金流記錄到一筆 35 元的成功扣款。後來再加入七個測試，涵蓋 C1 的重送、C2 的三種錯誤關聯、C3 的拒絕，以及 C4 的逾時與其他連線例外。C2 一條規則對應三個案例，所以規則數與測試數不必相同。

這裡的 `FakeGateway` 是測試替身。它分別記錄每一次扣款呼叫 `calls` 與成功扣款 `captures`，**刻意不替應用程式去重**。如果替身偷偷幫忙攔掉重複請求，應用程式即使少了 guard，測試也可能仍然全綠。

以下節錄完整範例中 `ConstraintTests` 的第一個測試。先用相同訂單與 key 呼叫兩次，再檢查結果與副作用；預期的 35 元直接來自前面約定的案例，沒有呼叫待測程式幫自己算答案。

```python
def test_same_attempt_is_not_charged_twice(self):
    gateway = FakeGateway()
    checkout = Checkout(gateway)
    first = checkout.pay(tea_order(), "buy-tea-001")
    second = checkout.pay(tea_order(), "buy-tea-001")
    self.assertEqual(second, first)
    self.assertEqual(gateway.calls, [("tea-001", 35)])
    self.assertEqual(gateway.captures, [("pay-1", "tea-001", 35)])
```

只比較兩次收據相同還不夠：程式也可能先多扣一次錢，再回傳舊收據。因此測試另外檢查金流呼叫與成功扣款的紀錄。反過來，只有 `assert checkout.pay(...)` 也太弱；收到任何非空物件就會通過，並沒有確認關鍵行為。

下一個測試保護 key 的邊界。第二張訂單不是第一張訂單的重送，必須拒絕；而且拒絕不能發生在另一筆扣款之後。

```python
def test_key_cannot_move_to_another_order(self):
    gateway = FakeGateway()
    checkout = Checkout(gateway)
    checkout.pay(tea_order(), "buy-tea-001")
    with self.assertRaises(PaymentConflict):
        checkout.pay(tea_order("tea-002"), "buy-tea-001")
    self.assertEqual(gateway.calls, [("tea-001", 35)])
```

最容易漏掉的是逾時的替身怎麼安排。完整測試涵蓋「還沒扣款就逾時」與「**金流已經記錄一筆成功扣款，回覆才遺失**」兩種情境。下面把後者單獨寫出來，完整程式則使用 `subTest` 同時涵蓋兩種情境。應用程式不知道那筆扣款是否完成，所以對外保留 `PENDING`。重送仍然查到同一個待確認結果，不產生第二次扣款。

```python
def test_timeout_stays_pending_without_another_charge(self):
    gateway = FakeGateway("timeout_after_capture")
    checkout = Checkout(gateway)
    first = checkout.pay(tea_order(), "buy-tea-001")
    second = checkout.pay(tea_order(), "buy-tea-001")
    self.assertEqual(first.status, "PENDING")
    self.assertIsNone(first.payment_id)
    self.assertEqual(second, first)
    self.assertEqual(gateway.calls, [("tea-001", 35)])
    self.assertEqual(gateway.captures, [("pay-1", "tea-001", 35)])
```

`captures` 有一筆、收據卻沒有 payment ID，正是這個 fixture 想保留的不對稱：測試能看見替身內部發生的事，應用程式只能依它收到的回覆判斷。不能因為測試知道扣款成功，就要求應用程式在失去回覆時也宣稱成功。

---

## 五、先看付款程式如何回應，再故意改壞它

範例把付款結果存在記憶體裡。每次先確認 key 沒有被拿去付另一張訂單，再查這張訂單是否已有付款嘗試；有的話核對 key 與訂單內容，直接回傳既有結果。只有新的、有效的嘗試才會呼叫金流，並且在呼叫前先留下 `PENDING`。

以下節錄扣款與狀態處理，完整 guard 與資料結構在隨文程式碼中。這幾行值得 reviewer 深讀，因為一個看似方便的例外處理，就能把「不知道結果」改成「已付款」。

```python
try:
    payment_id = self.gateway.charge(order.order_id, order.amount_ntd)
except Declined:
    receipt = replace(receipt, status="DECLINED")
except TimeoutError:
    receipt = replace(receipt, status="PENDING")
else:
    receipt = replace(receipt, status="PAID", payment_id=payment_id)
```

若要理解這段程式，先沿著回覆種類讀這張圖。它描述的是本例在付款邊界能知道的狀態，不是金流端的完整交易生命週期。

📌【在此插入圖 diagram-01.png】

圖中保留 `PENDING` 的分支，沒有直接通往 `PAID` 的箭頭。查詢與對帳需要新的證據，這份示範尚未實作。保存 `PENDING` 是為了讓後續處理有明確的起點，不是把未解決的付款永遠擱著就算完成。

其他未被這兩個分支處理的 provider 例外會向外傳遞，但呼叫前留下的 `PENDING` 仍然存在，相同請求重送時不會再發出扣款。這個前置紀錄本身也需要測試保護。整理範例時，Claude Code 的獨立 Review 提醒了這個缺口，範例因此補入「扣款後發生其他連線例外」的測試，以及刪除前置紀錄的 M7。Review 在這裡增加了原本沒選到的風險，下一步才用 mutation 驗證新增的測試能否保護它。

先確認未修改的程式通過所選測試，再每次只改一處，執行同一組測試，最後丟棄那份變異程式。測試因預期行為差異失敗，代表這個 mutant 被辨識，通常稱為 killed。本例的簡化 runner 把沒有被辨識的變異統一標為 survived；它沒有量測覆蓋率，因此這個標籤也包含根本沒有執行到的分支。正式工具會再區分 NoCoverage 與執行過卻未被辨識的 Survived，讀取下表時要記得這個差別。

---

## 六、依 Review 風險挑選 mutation 的範圍

第三種「挑選」，是決定哪些程式碼與變異值得執行。我的起點是前面已確認的付款要求，再對回實作它們的程式位置：扣款金額、既有嘗試的 guard、key 的綁定、例外處理與收據內容。

這次只變異 `payment.py`，不修改斷言、fixture、`FakeGateway` 或 mutation runner。否則就可能把題目或裁判一起改掉，無法回答產品程式是否受到測試保護。若真實 PR 改的是共用付款 helper，也要沿呼叫關係選出會受影響的測試，不能把 diff-scoped 誤解成「只看新增那幾行，其他都不必管」。

這種限縮 mutation 範圍的做法，也有較早的實務研究可以參照。Google 的 [Practical Mutation Testing at Scale](https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/)（2021）描述了在 Code Review 中針對變更執行 mutation、過濾較無用的變異，並依歷史表現選擇運算子的做法。它支持的是把成本與可採取行動的結果一起考量，不是為本文的七個 mutant 或 70% 門檻背書。

為了讓讀者能逐項核對，本例**人工指定七個 mutant**。它們是實際執行的變異，不是 Stryker、PIT 或 mutmut 自動產生的完整清單，也不代表已涵蓋所有可能的付款缺陷。

📌【在此插入表 table-03.png】

七個變異都有可以指出的行為差異，這次沒有排除的等價變異。若換用正式 mutation 工具，還要記錄工具版本、變異運算子、檔案範圍與測試選擇；把無法編譯、沒有覆蓋、逾時及確認等價的結果分開。例如 [Stryker 的計分文件](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/)把 killed 與 timeout 都列入 detected，沒有覆蓋的有效變異則仍在一般 mutation score 的分母裡。把 timeout 和 no coverage 都當成無效結果刪掉，分數的定義就變了，不能再直接與別人的報告比較。

一個存活的 mutant 也不會自動告訴你該增加哪個斷言。先讀它改了什麼，再找能呈現差異的輸入與副作用。例如 M2 需要第二次呼叫，M5 需要逾時情境；完整測試把扣款前、扣款後的逾時都納入，才沒有把結果未知誤解成一定扣到錢。在正常付款的測試裡多加五個 `PAID` 斷言，仍然碰不到這些情境。

若找不到反例，要釐清是需求未定義、輸入不可達、測試缺口，還是行為確實等價。「目前沒測到」不能當成等價證明。[Stryker 的等價變異說明](https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/)也提醒，工具無法替所有這類情況作出判定。團隊若決定排除，必須留下適用的輸入範圍、理由與審閱紀錄；高後果的存活變異，則要在核准前處理或明確承擔，不能躲在總分裡。

---

## 七、把 mutation score 算完，也把它沒有回答的事說完

在本例，七個 mutant 都能執行、都不等價，所以分母固定是 7。mutation score 就是被測試辨識的個數除以 7，再乘上 100%。分母是變異數，不是測試數；它也不是產品沒有 bug 的機率。

隨文的 `mutation_demo.py` 已實際執行三組測試選擇，原始程式在每一組都先通過。結果如下：

📌【在此插入表 table-04.png】

第一列的兩個測試都是真的，也都會執行付款；它們只是沒有要求程式處理重送、key 衝突、拒絕與逾時。M2、M3、M7 改動的位置有被執行，測試卻沒有辨識出行為差異，這是 mutation 比「那一行有跑過」多問的一步。M4、M5 則根本沒有進入對應的例外分支，單看分支覆蓋率也能發現這部分缺口。

第二列更值得停一下。如果團隊只採用測試篇提出的 70% 起始建議，85.7% 已經超過門檻。但 C4 的逾時情境仍然沒有被保護：M5 把 `PENDING` 改成 `PAID`，但這八個測試沒有執行逾時分支，因此無法辨識這個錯誤。**總分過線，不能抵銷尚未驗證的關鍵付款約束。** 這筆 PR 應先補足逾時案例，並確認它真的會對 M5 失敗。

這裡借用 70% 作為對照，是為了呈現「看總分卻漏看關鍵存活者」的問題。手選七個 mutant 與工具針對改動行產生的集合不同，分數也會隨選擇而改變；不能把這個小分母直接拿來校準或套用真實 repo 的門檻。

第三列補回 C4 的逾時測試，所以七個變異都被辨識。這可以支持「這九個測試抓得到這七種指定改動」；不能延伸成「付款服務可靠度是 100%」。沒有在範圍內的並行、重新啟動與 provider 整合，不會因為分母中的七個全被辨識，就自動得到驗證。

100% 也不能證明每一個測試各自有效。M2 會同時讓多個測試失敗；在隔離副本中，把 C1 的重送測試，以及 C2 的換 key、改訂單內容測試都改成空的 `pass`，三組分數仍然是 28.6%、85.7%、100%。其餘測試仍會辨識 M2，總分因此藏住了三個已失去斷言的測試。這個反例已實際執行，原始範例沒有被改弱。審閱時還要讀取斷言與逐項失敗測試，必要時單獨執行某條約束的測試，確認它確實會攔住違反該要求的版本。

Mutation 報告也要說明判定依據。本例 runner 先確認原始程式通過，核對各組測試數量與逾時測試名稱；再把每個 mutant 放進獨立的暫存目錄執行，區分斷言失敗與執行錯誤，列出失敗的測試名稱。它沒有逐一鎖定全部測試的身分，也沒有把斷言訊息寫入 JSON。若發生 import／執行錯誤、沒有收集到測試，或執行逾時，就中止示範，不把這些情況悄悄算成 killed。這是本教學採用的保守計分方式，不是所有正式工具的預設分類。

這裡要分清楚兩個層次：M5 改的是付款程式收到 `TimeoutError` 時的處理，測試本身會正常完成；mutation 工具所說的執行 timeout，則是等待 mutant 的測試行程超過時限。Stryker 將後者列為 detected，本例 runner 則直接中止；兩者都不是「付款逾時就算抓到 bug」。

把三組結果並列，是為了比較測試選擇；它不是一個可以讓 PR 作者隨意刪掉不利測試的 CI 開關。真正的驗收流程要固定測試範圍、保護規則與執行器，變更這些依據時另行審查。

---

## 八、把同一份證據交回 Review，再談可靠度

走到這裡，reviewer 收到的應該不只是一個百分比。這份付款 PR 至少需要一起呈現：它要支援什麼重送行為、C1 到 C4 的來源與 owner、九個測試的結果、七個 mutant 的逐項狀態，以及尚未驗證的系統邊界。

在 85.7% 那個版本，人的判斷是具體的：M5 會讓結果未知的付款被標為成功，C4 尚缺逾時測試，因此不能只因總分達標就核准。補上測試後，還要看它是否驗證對的事情；若它只檢查替身預設的字串，沒有經過 `Checkout.pay()`，仍然無法保護真正的狀態處理。

規則與程式之間也需要保留獨立性。候選 PR 可以提出約束修改，但不能自行改弱測試，再用改過的綠燈證明自己合規。正式流程應讓人核准規則變更，從受保護的規則與 runner 版本評估候選程式碼，並把核准紀錄對應到實際審閱的 revision。把測試放進 `constraints/` 目錄，本身不會產生這些權限保護。

本例的九個測試只描述一份候選程式在選定情境下的表現。若接著要量測 agent 的 constraint pass rate，單位要改成多個候選修補：在功能檢查通過的候選修補中，有多少也通過全部適用的約束。單一修補通過七個約束測試，不等於已經量測出 agent 的長期通過率。

同樣地，pass^k 是讓 agent 對相同任務獨立產生並驗證多次成果，依事先固定的功能與約束要求判定每次是否成功。它不是把同一份確定性的 unittest 重跑五次，也不是對七個 mutant 各跑一次。本篇沒有進行這組 agent 重複執行實驗，因此不提供虛構的 pass^5 數字。

這也是三道閘在這瓶綠茶上的分工。test gate 提供測試保護力的證據；review gate 判斷要求、證據與尚未處理的風險；reliability gate 再用一組固定任務的多次結果，支持任務授權的討論。前一步的資料可以交給下一步，分母與問題卻不能跟著偷換。

---

## 九、讀者可以重跑什麼，還不能拿它做什麼？

完整程式、九個付款測試、七個 mutant 與規則對照，放在 [examples/tea_payment](https://github.com/fantasybz/medium-articles/tree/main/examples/tea_payment)。使用 Python 3.10 以上版本，從儲存庫根目錄執行：

```bash
python3 -B -m unittest discover -s examples/tea_payment -p test_payment.py -v
python3 -B examples/tea_payment/mutation_demo.py
```

第一個命令執行九個測試；第二個命令輸出三組實驗的 JSON，包含 baseline 測試數、killed 個數、固定分母與各 mutant 對應的失敗測試。過程只使用標準函式庫與本機暫存檔，不會接觸真實帳號或扣款。

目錄裡另有十二個 runner 回歸測試，涵蓋載入失敗、異常測試結果、測試數量變動、逾時測試缺失等選定情境，並核對預期被辨識的 mutant 集合。它們不計入九個付款測試，也不計入七個 mutant 的分母；若用 `test_*.py` 執行整個目錄，合計會看到 21 個測試。

這份實作以記憶體字典保存付款嘗試，驗證的是**同一個行程、依序呼叫**的情境。兩個服務行程不會共用這份記憶體；行程重新啟動後也會失去紀錄。即使重複請求在示範裡被擋住，仍不能宣稱已經實現 production 的 exactly-once 扣款。

如果要把同樣的要求帶進真實服務，下一步應補上共享且持久的付款狀態、資料庫唯一性與交易邊界，再用並行請求驗證競態；模擬在扣款前後中斷行程，核對重新啟動後如何復原；依 provider 契約驗證 idempotency、查詢、對帳與 webhook 的重複或亂序事件。拒絕付款後如何經授權重新開始一次嘗試，也需要另外定義。這些都不在本例的 100% 分數裡。

識別碼的生命週期也需要明確設計。[AWS Builders’ Library](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)討論了相同 request ID 帶入不同意圖、延遲抵達的請求等問題；[Stripe 的 idempotency 文件](https://docs.stripe.com/api/idempotent_requests)則說明，key 保存至少 24 小時後可能被清除，清除後重用會產生新的請求。應用程式不能只記得「曾經用過這個 key」，卻不確認 provider 還記不記得它。這也是記憶體字典無法代替真實整合測試的原因。

身分授權同樣不能從 fixture 推論出來。真實服務還要拒絕跨帳號讀取或支付訂單；收據上的 SKU 正確，也不代表倉儲真的交付了那瓶無糖綠茶。把這些界線寫出來，是為了讓接手的人知道下一份證據該從哪裡補起。

---

## 十、回到那個等著付款結果的人

開場那位等著付款結果的人，只是想買一瓶茶。對方不需要知道 mutation score 的分母，也不應該靠猜測決定可不可以再按一次付款。這些判斷應該先在需求、程式與驗收流程裡被處理清楚。

對工程團隊來說，這個例子把三種挑選接在一起：依付款風險挑選 reviewer 與深讀範圍；從評論中挑出有長期價值、可判定且有人維護的約束；再把約束對回程式碼，挑選能檢驗測試保護力的變異。每一步都需要說明理由，才能讓下一個接手的人繼續判斷。

我想留下的，不是「補到 100% 就好」這句新口號，而是第二列那個 85.7%。數字看起來已經足夠漂亮，付款結果卻仍然可能被說錯。當 reviewer 能指出是哪個情境、哪條規則與哪個 mutant 尚未被保護，綠燈才開始成為有內容的證據。

四部曲談了測試、Review 與可靠度，最後仍要回到那個等著付款結果的人。那瓶綠茶的價格在這裡只是示範。值得被認真對待的，是有人把付款交給了這套系統，而團隊需要能解釋：我們確認過什麼，還有哪些問題需要繼續驗證。

---

### 系列文章

- [總論：綠燈不是驗收](https://medium.com/p/582f24223eea)：三道閘與導入順序。
- [一、測試篇](https://medium.com/p/b01055139451)：如何確認測試真的辨識得出錯誤。
- [二、Review 篇](https://medium.com/p/ccbf0cbe2691)：人的判斷、風險分流與核准責任。
- [三、可靠度篇](https://medium.com/p/3c64a9622777)：把 reviewer 約束留下來，量測候選成果與重複執行。
- **四、付款實作篇（本篇）**：用同一瓶無糖純喫綠茶，把選擇、測試與證據連起來。

### References

1. 隨文實作 — [付款、constraint tests 與七個指定 mutant](https://github.com/fantasybz/medium-articles/tree/main/examples/tea_payment)〔第四至九節；本例為教學設計，非 production 系統〕
2. Stryker 官方文件 — [Mutant states and metrics](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/)〔第六、七節；正式工具的狀態與計分定義〕
3. Stripe 官方文件 — [Idempotent requests](https://docs.stripe.com/api/idempotent_requests)〔第一、九節；provider 契約的實務對照，示範並未串接 Stripe〕
4. Stripe 官方文件 — [Handle errors](https://docs.stripe.com/error-handling)〔第一節；連線錯誤的不確定結果與同 key 重試〕
5. Google — [What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)〔第二節；審閱範圍、脈絡與能力〕
6. Petrović 等 — [Practical Mutation Testing at Scale: A view from Google](https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/)（2021）〔第六節；增量執行、變異過濾與選擇〕
7. Stryker 官方文件 — [Equivalent mutants](https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/)〔第六節；等價變異的判讀限制〕
8. AWS Builders’ Library — [Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)〔第九節；識別碼、不同意圖與延遲請求〕

### AI 協作說明

本文與隨文程式使用 AI 協助整理、撰寫、翻譯與檢查。付款情境與 Review 評論均明確標為教學示例；測試與 mutation 數字來自隨文程式的實際執行，不是虛構的 production 成效。

*Kochi Chuang，榮民叔叔的藏書筆記。*
