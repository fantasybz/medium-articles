# 可靠度與付款實作篇：發布前精修紀錄

日期：2026-10-24。範圍為《綠燈不是驗收》第三篇〈可靠度篇〉、第四篇〈付款實作篇〉的中英文原稿、貼稿與受影響圖表。

依作者要求，這輪從讀者做判斷的過程檢查兩篇後續文章：先交代具體情境，再引入概念，說明證據能回答什麼問題，最後接到授權、人力或核准決策。既有的[共用風格](../../STYLE.md)與[當月風格摘要](style_brief.md)持續適用。

## 可靠度篇：從量測結果走到決策

| 原本容易產生的疑問 | 本輪補充 | 證據與適用範圍 |
|---|---|---|
| 一份 PR 已通過，為什麼還要量測可靠度？ | 開頭接續 Review 篇，區分單次驗收與擴大委派範圍的判斷 | 通過個別 PR 的證據，與同類任務反覆執行的證據分開記錄 |
| 重跑是否可以接著上一次修好的狀態？ | 各次嘗試回到相同起點，不沿用前次修改、答案或對話 | 獨立嘗試的比較與實務上修正後重跑各有用途，統計時要分開 |
| pass^k 能否直接以整體 pass@1 的 k 次方代替？ | 分清實際量測的連續成功率、簡化機率示意與至少成功一次的 pass@k | 公式示意不能取代同一組任務反覆執行的量測 |
| 同一份 PR 重跑多次，分母怎麼算？ | 示範固定記錄每份 PR 首個通過功能檢查並送驗的候選版本；保留版本與結果，重跑另列 | 真實 PR 的固定樣本與 golden set 實驗分開；證據缺失也另列 |
| 整體約束通過率高，能否接受個別失敗？ | 以假設的 100 個候選版本中 93 個通過、7 個失敗說明分母 | 整體指標供風險判斷，個別 PR 仍須通過自己的必要約束 |
| Review 分流矩陣是否自帶可靠度目標 T？ | T 改為團隊為該類任務明確設定的數值；矩陣決定責任與審查深度 | 0.95 等數字是示範假設，不能從矩陣的格子直接讀出 |
| 抽查公式算出比例，就能安排人力嗎？ | 補上模型前提與樣本選擇的影響，再換算 100 份、抽查 75%、每份 20 分鐘為 25 小時 | 工作量加倍為 50 小時；這仍未包含其他審閱工作。若只抽查自動檢查通過者，須在該選取政策下重新估計 p、c |
| 30 個案例與信賴區間能否支持擴權？ | 說明 30 例僅作為起步清單，信賴區間不會消除樣本選擇偏差 | G2 仍限低影響、可驗證的工作，每份 PR 保留人工核准 |
| 月報數字齊全，還缺什麼？ | 逐項解讀示範月報、指出缺少的證據及負責補件的人；YAML 加入範圍、約束樣本與 `on_missing: hold` | 月報中的示範數字沒有改寫為作者實測的 production 成效 |

兩種語言各重繪 `diagram-01.png`、`diagram-02.png` 與 `table-02.png`。圖中標示約 93%／67%，保留其他授權條件；英文圖表調整換行，公式與比較條件能完整閱讀。兩篇各仍有七張圖，封面仍選 `diagram-02.png`。

## 付款實作篇：讓測試、審閱與合併證據接得起來

第五節程式摘錄補上呼叫 provider 前的 pending 紀錄，與[隨文實作](../../examples/tea_payment/payment.py)對齊。文字先解釋 `Receipt`、`Attempt`，再帶讀者看連線錯誤為何跳過第二次寫入與回傳，最後連到 M7 的檢查目的。

重送保護的條件統一為：依序呼叫**同一個 `Checkout` 實例，且該實例仍保有先前紀錄**。即使沒有重啟行程，重新建立實例也會失去這份記憶。這個界線已寫進程式摘錄前、審閱示例與第九節。明確拒絕付款後，也不能直接為同一訂單換一個 key；重新授權或換卡屬於示範之外的新流程。

第八節沿用 Review 篇的付款重送情境，補足以下判斷鏈：

1. PR 沒有新 commit，目標分支或佇列仍可能改變合併候選版本。
2. 分開記錄 PR head、base、候選 commit 與 tree；check run 的所屬 commit 還要對應實際取出執行測試的版本。
3. 核准紀錄保留驗證資產版本、必要檢查的來源／執行 ID／結果，以及核准者的範圍、理由與時間。
4. 候選版本改變後重新確認證據，再依差異與風險安排人工審閱；核對後到合併前也要防止版本被換掉。
5. merge、squash、rebase 可能產生不同 commit；保留候選內容與最終內容的對應及合併後核對結果。

這是核准政策的設計示例。程式沒有新增 approval service、merge queue 或真實付款 provider。本輪沒有修改可執行範例、測試或七個 mutant。

## 一手來源與查核界線

Git／GitHub 文件於本輪透過 gstack browse 重新查閱，原始文字快照留在 gitignored 的 `.context/reliability-payment-polish-2026-10-24/`。採用原則延續[合併候選版本與核准紀錄](review-approval-drift-evidence.md)：

- [Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)與 [git-merge-tree](https://git-scm.com/docs/git-merge-tree)：區分檔案樹內容與 commit 的歷史／中繼資料。
- [Checks API](https://docs.github.com/en/rest/checks/runs#create-a-check-run)：check run 對應 commit，需保留識別碼、狀態與結果。
- [Merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)與 [merge_group](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#merge_group)：候選組合會包含最新 base 與前方 PR；必要的 Actions 檢查須涵蓋對應事件。
- [Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)：平台可接受 skipped／neutral；付款測試必須實際執行且成功，是本文建議的更嚴格政策。沒有把所有 base 或 queue 變動說成必然自動撤銷所有核准。
- [Merge methods](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github)：最終 commit SHA 與候選 SHA 不一定相同。

可靠度篇的既有研究數字與研究限制保留。本輪著重原稿的定義、推論與讀者判斷過程，沒有重新執行論文實驗，也沒有重新查核所有外部引文。付款測試的設計與歷次修正仍見[付款實作研究紀錄](payment-example-evidence.md)。

## 審閱與本機驗證

Claude Code 審閱曾實際啟動，但回報 `Credit balance is too low`，沒有產生模型審閱結果。本輪另以新的唯讀 Codex CLI 工作階段完成技術與編輯審閱；編輯審閱指出同一 `Checkout` 實例及 T 的數值定義兩項問題，均已修正。最後一輪完整雙語審閱回覆 `NO_FINDINGS`。這些是同一提供者的獨立工作階段，不記成 Claude Code 或跨提供者審閱。

本機三套 `unittest` 通過：工具 301 項、研究腳本 121 項、付款與 mutation runner 21 項，合計 443 項。付款教學實驗另行重跑，同一組七個指定、非等價 mutant 的結果仍為：功能測試 2/7（28.6%）、移除逾時測試 6/7（85.7%）、完整約束測試 7/7（100%）。這些分數只描述這組測試對七種指定錯誤的辨識能力。

六張更新圖表逐張檢查文字、換行、尺寸與邊界；四份貼稿與圖表定義由原稿重新產生。測試紀錄與圖表檢查資料留在上述本機證據目錄。

## Medium 排程稿讀回

四份既有排程稿已更新。等待儲存後以新分頁讀回全文、連結、圖片與發布設定；全部仍為 `isPublished: false`。

| 排程稿 | Post ID | 發布時間（Asia/Taipei） | 文字區塊 | 連結 | 圖片 | 分隔線 |
|---|---|---|---:|---:|---:|---:|
| 可靠度篇（中） | `3c64a9622777` | 2026-10-27 09:00 | 169 | 22 | 7 | 10 |
| 可靠度篇（英） | `4b6d147bff0d` | 2026-10-29 09:00 | 169 | 23 | 7 | 10 |
| 付款實作篇（中） | `46377fd460fe` | 2026-11-03 09:00 | 157 | 32 | 7 | 11 |
| 付款實作篇（英） | `20452944263b` | 2026-11-05 09:00 | 157 | 33 | 7 | 11 |

付款篇七張原圖保留；可靠度篇每種語言替換三張更新圖表，封面仍選新版 `diagram-02.png`。正文標題、Topics、預覽標題與摘要、通知設定及原排程均保留。可靠度兩份稿件仍各有零個付款程式碼連結，付款篇各保留兩個；回填總論與前三篇仍以同語言第四篇實際公開為準。

初次新分頁讀回付款稿時，曾暫時缺少文末區塊；等待後再次唯讀核對即取得完整版本，沒有重新貼稿或把部分儲存當成完成。最終數字來自通過全文核對的讀回紀錄。逐篇證據另記於各語言發布包的 `PUBLISHED.md`，全系列時程見 [PUBLISHING.md](../../PUBLISHING.md)。
