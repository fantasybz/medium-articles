# 四篇全文與敘事修訂品質紀錄

更新：2026-09-28（本輪於 9/27 開始）。四篇已依作者讀後意見重新撰寫，完成本機交付，尚未發布。Claude Code `claude-opus-5-5`、**max effort** 主寫；Codex 主代理依現行風格逐段潤飾與來源核對，再處理 Claude Code **xhigh** 的全系列讀者審查。

## 這次修正了什麼

作者指出上一版缺少研究動機、系列連貫與故事性，也看不出四份 spec 的實際內容。這次以共同的[敘事 brief](narrative-revision-brief.md)重寫四篇：

- **研究為什麼做**：從已記錄的工作坊驗收缺口，接到「單次結果無法描述反覆交付」；用真實 repo 的 parser 缺陷，說明為何選這個窄案例。沒有補造作者親歷、對話或生產事故。
- **想回答什麼**：總論列出重複完成、文件條件與資源、通過後的實作差異三個問題；變異篇逐一回答，並分清已觀察的結果與仍待量測的人力成本。
- **四份文件差在哪裡**：規格篇逐段節譯 A0/A 的 R05、B 的理由與六組自查、C 的可選流程與 helper 建議；附凍結英文原文，保留 A 已有部分理由、C 可不採用，以及 CLI 範圍措辭並不完全等價的事實。
- **四篇如何接下去**：總論提出問題，規格篇交代模型讀到什麼，契約篇沿同一條 R05 建立外部驗收，變異篇由兩份真實候選讀結果。回顧 Agentic Engineering 與已完成但尚待發布的「綠燈不是驗收」，各自承接相關問題。
- **讀者如何走到判斷**：依作者後續提醒，補上相同輸入如何核對 A0／A、規格已寫明卻實作錯誤時如何選擇文件修改、兩行 JSON 如何依 R05／R03／R08／R11／R12 推到三個出口，以及十次全過、hash、cosine 與成本表能支持哪些判斷。簡化例明標假設，觀察與建議之間交代理由和適用條件，見[編修差異](narrative-2026-09-27/reader-reasoning-delta.json)與[後續處置](narrative-2026-09-27/reader-reasoning-review-delta.json)。

## 主寫與逐段編輯

本輪最初四次請求遇到 session 額度限制。作者確認額度恢復後，四個新 max 請求均完成，實際 CLI 版本為 2.1.283。總論與變異篇跨 CLI 自動續接，完整主稿由最後正文文字區塊精確接合；沒有只取最後一段而遺漏前文。初稿、續接與編輯前後雜湊見[主寫來源](writer-provenance.json)。含思考內容的原始回應只保存在 gitignored `.context/`。

主代理按 [STYLE.md](../../../../STYLE.md)、[style brief](../../style_brief.md)與[聲音手冊](../../../2026-09/voice_brief.md)，讀完各篇開場、全部章節、引文、表格、結語、References 與 AI 協作說明，再核對跨篇承接。段落紀錄包含後半部與結語，不以「零警告」代替閱讀判斷，見[逐段潤飾紀錄](narrative-2026-09-27/paragraph-polish.json)。

本輪 Claude xhigh 以四篇全文與作者風格獨立審查敘事，沒有讀取主代理處置結論。報告保留實際輸入版本，後續修改另有逐項處置與差異紀錄，見[讀者審查](narrative-2026-09-27/reader-review.md)與[處置](narrative-2026-09-27/review-resolution.json)。先前一個提早啟動、讀到尚未安裝新版正文的請求已中止，沒有採用其結果。

補強判斷過程後，再以 Claude Code xhigh 複核指定章節，處理 R12 摘要規則、假設錯誤的指涉、cosine 的解讀次序，以及每名額預算門檻四項問題；見[複核報告](narrative-2026-09-27/reader-reasoning-review.md)、[實際輸入與呼叫紀錄](narrative-2026-09-27/reader-reasoning-invocation.json)及[逐項處置](narrative-2026-09-27/reader-reasoning-resolution.json)。這次是指定段落的閱讀複核，沒有宣稱第二次全文事實稽核。最終四篇由主代理重新通讀，包括後半部與結語。

## 正文、貼稿與嚴格繁中檢查

八份最終文本都實際呼叫 zh-TW MCP：`profile=strict`、`ai_threshold=low`、翻譯腔技術領域、一致性、風格檢查、`verify=true`，門檻為零 errors、零 warnings。沒有整批自動替換。

| 篇目 | 本機發布包 | 正文 | 貼稿 |
|---|---|---|---|
| [總論](../../../../2026-11-same-spec-overview/article.md) | [貼稿](../../../../2026-11-same-spec-overview/publish/medium-paste.md)；2 張圖表 | [0 錯誤／0 警告；37 提示](narrative-2026-09-27/overview-source-06.json) | [0 錯誤／0 警告；37 提示](narrative-2026-09-27/overview-paste-03.json) |
| [規格篇](../../../../2026-11-same-spec-spec/article.md) | [貼稿](../../../../2026-11-same-spec-spec/publish/medium-paste.md)；3 張圖表 | [0 錯誤／0 警告；17 提示](narrative-2026-09-27/spec-source-06.json) | [0 錯誤／0 警告；17 提示](narrative-2026-09-27/spec-paste-03.json) |
| [契約篇](../../../../2026-11-same-spec-contract/article.md) | [貼稿](../../../../2026-11-same-spec-contract/publish/medium-paste.md)；3 張圖表 | [0 錯誤／0 警告；36 提示](narrative-2026-09-27/contract-source-08.json) | [0 錯誤／0 警告；33 提示](narrative-2026-09-27/contract-paste-04.json) |
| [變異篇](../../../../2026-11-same-spec-variance/article.md) | [貼稿](../../../../2026-11-same-spec-variance/publish/medium-paste.md)；4 張圖表 | [0 錯誤／0 警告；61 提示](narrative-2026-09-27/variance-source-06.json) | [0 錯誤／0 警告；60 提示](narrative-2026-09-27/variance-paste-03.json) |

八份均為 `accepted=true`。資訊提示逐項依語境判讀，例如表示 pass 的「通過」、真實的條文優先順序、正式篇名、檔名 `.json`，以及有比較用途的清單；保留理由見[語言處置](narrative-2026-09-27/language-adjudication.json)。英文論文題名只使用完整正式題名作專名設定，沒有全面忽略問號或翻譯腔規則。語言工具不替代證據核對。

## 發布包與資料完整性

四篇共 12 張 PNG，均已開啟檢視。貼稿由正文重新產生，圖表索引與轉換輸出一致；表格內來源連結移到正文，轉成 PNG 後仍可點選。桌面與 390 px 手機預覽圖片全部載入、沒有水平溢出。F1 保留核准 Mermaid，F2 保留原始 PNG 位元組。全部本機連結存在。

317 份正式封存檔案的雜湊無差異；沒有新增研究樣本。發布工具 301 項、研究工具 121 項測試通過，diff 空白檢查通過。完整雜湊、審查版本、預覽與驗證見[交付驗證](narrative-2026-09-27/delivery-validation.json)。正式實驗仍是 CLI 2.1.282、high effort，寫作與 review 不計入正式四十次生成或研究費用。

交付範圍是中文全文與本機發布包。尚未建立 Medium 草稿、排程或發布；公開發文前，需要把 repo 附件換成版本固定的公開入口。上一版的三種角度 AI 複核與品質紀錄另存於 [2026-09-25 歷史紀錄](STATUS-2026-09-25.md)，不冒充本輪全文審查。這些 AI 檢查也不等於真人盲審或外部重現。
