# Review 篇：合併候選版本與核准紀錄

查閱日期：2026-10-23。範圍是《綠燈不是驗收》Review 篇中英文第七節，以及相應的 TL;DR、導入步驟、結語與參考資料。

## 回饋與要回答的問題

讀者 [Acemeridian 的回饋](https://medium.com/@acemeridian/a-useful-edge-case-is-base-branch-drift-a-pr-can-keep-the-same-head-sha-while-the-merge-candidate-819191ed1fea) 指出：PR 的 head SHA 不變，目標分支或合併佇列的變動仍可能改變合併候選版本。只記錄 PR 的 diff 與報告，未必能對應到最後合併的內容。作者已回覆會補充 exact merge tree、必要檢查及重新確認核准的條件；本輪沒有另行回覆讀者。

這次沿用 repo 的研究迴圈，做定向補強：讀取回饋與既有稿件 → 查閱 Git／GitHub 一手文件 → 區分平台行為與作者建議 → 雙語修訂 → 技術、語意與發布驗證。沒有重跑整月選題，也沒有擴寫成新的系列文章。

## 來源與採用範圍

| 一手來源 | 文件支持的內容 | 本文如何使用與限制 |
|---|---|---|
| [Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) | merge group 包含最新目標分支與佇列前面的 PR；佇列組合可能重建 | 說明 head 不變仍需要辨認新的整合候選版本；不宣稱佇列本身會撤銷所有人類核准 |
| [Actions：merge_group](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#merge_group) | 用 Actions 執行必要檢查的 workflow 要包含 merge_group；其 SHA 是 merge group 的 SHA | 區分 PR 上通過的檢查與佇列候選版本的檢查；沒有聲稱本 repo 已部署 merge queue |
| [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | stale approval 與受審 diff／merge base 的變動有關；必要檢查可接受 successful、skipped 或 neutral | 不把特定設定擴張成所有 base／queue 變動都會自動撤銷核准；要求付款測試實際執行並成功，是作者建議的政策 |
| [Checks API：Create a check run](https://docs.github.com/en/rest/checks/runs#create-a-check-run) | check run 以 head_sha 對應 commit，另有 ID、status、conclusion、App 等欄位 | 建議保留候選 commit／tree 與實際執行結果；報告所屬 SHA 還必須對應測試實際取出的版本 |
| [Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects) | commit 指向 tree，也保留父提交、作者等資訊 | 說明 tree 與 commit 的識別範圍不同，不把 tree 相同當成沿用 commit-bound checks 的充分條件 |
| [git-merge-tree](https://git-scm.com/docs/git-merge-tree) | 成功合併的輸出包含結果樹 OID；有衝突時還有額外資訊 | 只用於解釋合併結果樹，沒有提供忽略衝突退出碼的實作範例 |
| [About merge methods on GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github) | merge、squash、rebase 形成不同提交歷史，rebase 會建立新的 commit SHA | 不要求最後 commit SHA 必然等於候選 SHA；要求放行機制確保內容對應，並保留候選與最終版本的關係 |

原始頁面文字與發布前後快照只留在 gitignored 的 `.context/publication-review-2026-10-23/`。本文保留來源連結與採用範圍，不把原始網頁全文納入公開 repo。

## 論述與證據界線

- 先以示範售價 35 元的無糖純喫綠茶說明：付款重送 PR 沒變，但另一份 PR 改了共用函式的逾時行為。這是**假設整合情境**，不是作者遇過的事故，也不是現有付款範例已實測的情況。
- C1／C2 表格讓讀者先分清 PR、目標分支與候選版本，再引入 head SHA、base-branch drift、tree SHA 與 commit SHA。
- 核准紀錄保存人類決策、整合版本與驗證證據。必要檢查的來源、執行 ID、結果、所屬 commit、workflow 與政策版本要可核對；重跑結果不能只剩一個綠燈。
- 本文建議 base／head／queue 變動時先暫停沿用舊紀錄，重新確認候選版本、必要檢查與核准。依整合差異及風險安排人工重審，不要求每次重讀所有未變更的行。
- tree hash、報告上的 SHA 與歷史核准各有用途，任何一項都不單獨證明目前版本已正確驗證。尤其要確認實際執行測試的程式版本，並防止核對後換成另一個整合版本再合併。
- 核准機制仍是待 pilot 驗證的設計建議；未宣稱 CodeRabbit／Copilot 排除機制、merge queue 或候選版本核准服務已在本 repo／生產環境實作。
- 原有付款程式碼參考資料仍為第 28 項。總論及前三篇中英文繼續等待各語言第四篇實際發布後才公開程式碼連結。

## 審閱與交付紀錄

- Claude Code 已嘗試工具隔離的雙語技術／編輯審閱，但 CLI 回報 `Credit balance is too low`，沒有產生審閱結果；不把本次嘗試記成通過。
- 主代理依上述一手來源核對平台行為、核准政策與實作界線，並補清「報告掛在 C2、實際卻執行 C1」仍不構成 C2 的驗證。
- 中英文新增 `table-04.png`；原有四張流程圖、三張表與封面保留。表格由 `figures.json` 產生，文字與兩份原稿對應。
- 2026-10-23 已逐一讀取 22 個 Medium Post ID：14 篇已發布、8 篇仍排程；所有有讀取編輯器的正文均與更新前 repo 貼稿相符。Review 篇中文實際於 10/20 09:01、英文於 10/22 09:01 上線；四份後續《綠燈不是驗收》稿件與四份《同一份規格，跑十次》中文稿的排程不變。

六篇受影響公開頁已更新並完成讀回：總論中英各 206 個文字區塊／34 個連結／18 張圖／16 條分隔線；測試篇中英各 197／26／8／13；Review 中英各 240／48／8／12。正文逐塊、連結順序與目的地、原圖 metadata 及程式碼均核對相符。八個未來排程再次從新分頁讀回，與本輪基準相同。

中文版 Review 的舊預覽摘要在重發後持續被縮短，因此改成 92 字元的完整介紹，已逐字核對；這是本輪刻意更新的預覽設定。各篇的發布紀錄已區分正文、預覽與其他設定，沒有把所有欄位都寫成未變動。細節見 [Review 中文紀錄](../../2026-10-green-review/publish/PUBLISHED.md)、[英文紀錄](../../2026-10-green-review/publish/en/PUBLISHED.md)與 [全系列發布紀錄](../../PUBLISHING.md)。

離線驗證使用 repo 規定的工具、研究及付款範例三套測試。本輪未更動工具或付款程式；新增的 `.gstack/pregate.json` 僅將執行時才發現的圖表定義檔對應到既有研究測試，不取代完整測試或 Medium 的公開頁核對。
