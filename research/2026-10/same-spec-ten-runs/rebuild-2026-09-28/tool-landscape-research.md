# 規格工具與文件維護：第一手來源摘要

查證日：2026-09-28（臺北）。全部網頁使用 gstack browse 取得；私人 sources-root 保存全文文字快取及 SHA。工具文件只證明當前設計與功能，不作效果實驗。

## T1：Birgitta Böckeler：Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl

- 2025-10-15，作者的工具試用／概念分析；https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
- 對本系列真正有用的是三種不同承諾：spec-first 是先釐清一項工作的規格再生成；spec-anchored 是後續改變仍維護規格；spec-as-source 把規格當主要可編輯來源，程式是衍生物。它們不是同一套制度，也不能由一次生成成功一次選完。
- 作者區分任務規格與 repo 常駐的背景文件（memory bank）。前者對應建立或修改特定功能的工作，後者則可供多次 coding session 共同使用；文中以 spec-kit constitution 作為常駐背景文件的例子。
- 作者試用觀察包含小修補卻產生大量文件、需要讀者審閱更多 Markdown，以及 agent 未完全照規格做。這些是作者少量經驗，不是介入的平均因果效果。不得由它推論 SDD 必定拖慢或任何一工具沒有價值。
- 工具試用時間是 2025 年 9 月；不能拿舊版單一工作流批評 2026 年的工具。應和下面的當前文件分開。
- 本系列推論：常駐指引應記錄適用範圍與維護者，避免讓單次修補選擇變成所有工作一律遵守的限制。這是根據上述區分提出的治理建議，不是作者原文的規則。選工具之前，先決定要保留哪種決策、何時更新，以及由誰確認程式與文字仍一致。spec-first 有用並不自動證明 spec-as-source 適合既有 repo。

## T2：GitHub Spec Kit 當前 README

- https://github.com/github/spec-kit，2026-09-28 存取，動態文件，未鎖 commit；僅作存取日狀態，不給穩定版本宣稱。
- README 已區分 SDD、bugfix、idea assessment 三種入口；後兩者為 opt-in extensions。因此不要說該工具現在強迫所有工作走同一套 feature 流程。
- SDD 的文件順序把 what/why 放在 how 之前，包含專案 constitution 與 feature 的 specify、plan、tasks、implement、converge；文件要求審查中間成果。這只能證明工具把哪些決策分開，不證明使用後就能防止漏掉需求。
- 本文不需要安裝指令／命令逐字列表。以產品需求、實作計畫、任務拆解與驗證的責任區分即可，避免 article 成為短期版本教學。

## T3：Kiro 當前 specs overview

- https://kiro.dev/docs/specs/ ，頁面標記 2026-08-27 更新，2026-09-28 存取。
- 文件分 requirements.md／bugfix.md、design.md、tasks.md，也提供 requirements-first／design-first、bugfix 和 quick spec 等路徑。不能從流程存在推論模型會遵守。
- 它說明工具可以保存需求、設計與工作清單三種工件；團隊仍要確定產品行為、審查例外與實際驗收。

## T4：Kiro Correctness

- https://kiro.dev/docs/specs/correctness/ ，頁面標記 2026-08-04 更新，2026-09-28 存取。
- 描述從需求生成 property-based tests，輸入生成與 shrinking 協助找反例。文件明說 PBT 不等於 formal verification，弱或錯的 property 會在行為有問題時仍通過；也承認外部系統／非確定性情況需要其他方法。
- 文件顯示產生 PBT 為 optional；不能說所有 Kiro 工作都已執行並通過此檢查。
- 可引用這個「供應商自己的界線」，再由成熟測試來源說明機制。不要採用頁面較寬的 entire input space 用語，亦不將 fuzzing 與 PBT 完全等同。
- 本系列推論：從需求產生驗收能減少轉換成本，但由同一個錯誤需求派生出的規格與測試仍可能一致地錯；必須審查 property 要保護的行為。

## T5：Kiro Bugfix Specs

- https://kiro.dev/docs/specs/bugfix-specs/ ，頁面標記 2026-08-04 更新，2026-09-28 存取。
- bugfix 文件分 current behavior、expected behavior、unchanged behavior。「哪些地方照舊」必須被當作修補的一部分，並能對應回歸驗收。
- 可用來解釋 parser 的 legacy diagnostics、exit priority 與重複事件不是重構時可以順便替使用者重新決定的事。文件範本不保證相容性；結果仍待驗收。

## 如何進稿

總論只用 T1 的持續維護差別和 Lamport 等基礎建立 why；規格篇最多一段對照工具文件，重點是責任與文字種類，不寫工具排名。契約篇可用 T4 連到自動生成 property 的審查反例。R05／R13 自有案例承載推導，不用數個供應商術語取代例子。
