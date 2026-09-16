# Backlog：2027 年起的主題候選（2026-10 迴圈）

> 接續 `research/2026-09/backlog.md`（2026-09-05 建立）。本圈是**期中加圈**，不是新的選題：10–12 月三個主題、排序與四條 12 月修正全部沿用 `research/2026-10/selection.md`，這份檔案只更新「2027 年之後寫什麼」的狀態機。輸入：`research/2026-10/` 的六份 digest（`conference_digest.md`，特別是 §9 的 backlog 更新；`book_ai_agent_book.md`；`arxiv.md`；`x_digest.md`；`community_digest.md`；`notion_digest.md`）與 `selection.md`。窗口是 2026-09-01 → 09-15，只有兩週，所以多數條目的正確答案是「觀察中」而不是「升級」。
>
> 兩件本圈才有的事：作者 2026-09-10–11 到現場參加 **AGNTCon + MCPCon Japan 2026**（東京），以及李博杰《深入理解 AI Agent》**v2.0**（2026-09-06，Apache-2.0）讀完。會議與書帶進來的是**新主題**與**機制解釋**，不是新的台灣需求訊號—台灣社團對東京這場的貼文是**零**（`community_digest.md` 監看清單），這件事本身變成一個新條目與一個插曲。

## 使用規則

- **狀態**：`候選`（可進下月提案池）、`觀察中`（證據不足，不主動提案，但持續監看）、`插曲`（單篇，不佔主題席位）。
- **升級**：條目列出的「升級證據」任一項出現，就標記日期並進下月提案池，由 judge 重新打分。
- **降級**：連續三個月沒有新證據的 `候選` 降為 `觀察中`；`觀察中` 六個月沒動就刪除（留在 git 歷史即可）。**期中加圈不計入那三個月**—本圈只記錄「這兩週有沒有新證據」，月份的計數器以每月 1 日那一圈為準。
- **月份**：「最早月份」是依賴關係推出來的下限（哪一篇要先發、哪本書要先讀完、哪個實驗要先跑），不是排程；實際排期由當月 Select 決定。
- **編號固定**：1–9 沿用 2026-09 的編號不動（`conference_digest.md` §9.1 依編號引用），新條目從 10 開始接。**一句話總表的列序才是本圈順位**，不是編號。
- **分數**：本圈不重新打分。「上次評分」欄一律是上一次 judge 的分數，括號內補本圈的證據走向；真正的重評在下一次 Select。
- **數字的出身**：會議與書的數字要標出身—organiser-reported、vendor-reported、team-reported、book [measured] 或 [cited]—不得當成第三方量測。二手轉引（投影片引用別人的論文）要標「來自投影片的引用」。
- **人名**：社團成員一律只寫角色（「搞笑談軟工的版主」「Backend 台灣的常貼作者」「Scrum Community 的管理員」），不寫名字；會議講者與公開出版品作者是公開紀錄，可以寫。
- **回填**：每月底 `collect.sh medium` 之後，把 10–12 月四篇的 reads／完讀率寫進文末「成效權重」表，供 judge 調整 demand 與 format 的權重。

## 一句話總表

| # | 條目 | 狀態 | 上次評分 | 最早月份 | 一句話 |
|---|---|---|---|---|---|
| 1 | Coding Agent 的爆炸半徑 | 候選 | 34.8（未駁倒；本圈拿到盛行率與防禦兩組實測，未重評） | 2027-01 | 漏洞在 harness 不在 model；寫在 prose 裡的規則不是控制，harness 外的 reference monitor 才是 |
| 4 | Skills、Memory 與 Compaction | 候選 | 33.5（本圈證據增幅最大；skills 從「檔案」變成「可擾動的系統」） | 2027-03 | context 的第二層治理：skill 准入靠配對實測、memory 當資料庫管、規則在壓縮中蒸發 |
| 3 | Agent runtime 是平台產品 | 候選 | 未評（東京補上脊椎：agent 的工作區是儲存產品） | 2027-02（建議 03） | sandbox fleet、state、memory、agent config as IaC—platform team 的 2027 build list |
| 2 | 知識流失與維護債 | 候選 | 33.0（軼事側變強，縱向研究側本圈掛零） | 2027-01（建議 02） | 吞吐量免費之後，組織付的帳是共同理解與可維護性，agent 一樣都不會幫你補 |
| 10 | Agent identity 與委派授權 | 候選 | 未評（新） | 2027-02 | 一千個員工沒有一個有名字：爆炸半徑要先有一個 principal 可以畫 |
| 8 | 艦隊不是免費的：multi-agent 拓樸 | **候選**（自觀察中升級） | 未評（新軸：證據根數，不是拓樸選型） | 2027-04 | 多一個 agent 不等於多一份證據—32 份報告共用一個證據根，覆蓋率從 0.94 掉到 0.26 |
| 5 | Agent 的探索式測試 | 候選 | 未評（東京給出第一個 agent 去「用」agent 產品的實例） | 2027-04 | testing 不能自動化—tester 拿 computer-use agent 去「用」agent 做出來的東西 |
| 11 | 免費的 tool call 有人在付：MCP 生態的可用性 | 候選 | 未評（新） | 2027-03 | 先當 uptime 問題再當經濟問題：三天後有 41.6% 不見了，你的 harness 依賴它 |
| 6 | Model 供應是上游依賴 | 觀察中 | 28.5（讀者錯位仍在；但出現一條繞開錯位的重切） | 2027-03 | 席位、額度、斷線、本地混合—把 vendor 當 dependency 做 SRE；重切成「harness 的模型可攜性」 |
| 7 | 棕地的設計維度：DDD 與 Event Storming | 候選（第一次空手） | 未評 | 2027-05 | 總論與技術篇的 brownfield 三階段之後，agent 在 legacy 上做出來的邊界對不對 |
| 12 | MCP task lifecycle 與長時間工作 | 觀察中 | 未評（新） | 2027-02 | request/response 的心智模型壞了：一個會等幾小時的 tool 要怎麼觀測、怎麼驗收 |
| 13 | 碳與成本感知的 agent 工程 | 觀察中 | 未評（新） | 2027-Q2 | 先是可靠度控制，才是綠色議題—有界重試、right-sizing，加上會議上唯一一份自己公布範圍限制的量測 |
| 14 | 日本作為需求訊號 | 觀察中 | 未評（新） | 2027-Q2 | 兩千人報名一場給業務用的 Claude Code 講座、一本講「控制 AI 波動」的書排第一—zh-TW／ja 跨海的讀者假說 |
| 9 | 去技能化 | 插曲 | 未評（本圈第一次有行為面的量測） | 2027-Q1 | 單篇文化長文，與不確定性共舞的續集 |
| — | 東京現場筆記：AGNTCon + MCPCon Japan 給台灣讀者 | 插曲（**時效性**） | — | 2026-10（越晚越沒用） | 台灣社團零貼文、繁中零覆蓋；作者是唯一在場的人 |
| — | PSTN、語音與物理世界的動作空間 | 插曲 | — | 2027-Q2 | 兩天裡最完整的一條 end-to-end harness 故事，且三個主題都碰不到 |
| — | 我的 Golden Kubestronaut 之路 ＋ 認證地圖 | 插曲 | — | CNPE 過關後的下一個月 | 不要跟 2026-12 撞；CNPE 第二次考試截至 09-14 仍未記錄結果 |

**本圈的移動，四筆。** (a) 第 8 條自 `觀察中` 升 `候選`，軸從「拓樸選型表」換成「證據根數」，因為 2609.01873 那條不依賴 model 版本；(b) 第 4 條在排序上超過第 3、第 2 條—skills 這兩週拿到方法論、誠實的 null、以及一個 vendor 原生的准入閘；(c) 新增第 10–14 條，全部來自東京或書，不是來自台灣需求；(d) 第 7 條本圈第一次沒有社群訊號，記第一次空手，若 2026-11、2026-12 兩圈仍無新證據則降為 `觀察中`。**沒有任何一條達成升級條件的第一順位**：台灣仍然沒有公開的 agent 事故，CNPE 仍然沒有結果，`Fb temp` 仍然沒有貼上粉絲團。

---

## 1. Coding Agent 的爆炸半徑：漏洞在 harness，不在 model

**title_zh**：Coding Agent 的爆炸半徑：漏洞在 harness，不在 model

**pitch**（2026-09 版不變，摘要）：寫在 CLAUDE.md 裡的安全規則是 write-only channel；能真正限制爆炸半徑的只有 harness 外面的確定性 enforcement—per-run identity、authorization broker、flow／origin policy、egress 與 audit。三部曲雛形：威脅模型篇 → 控制篇 → 供應鏈與應變篇。

**本圈新增的證據**（`arxiv.md` §2 D+K／§3 訊號 8、`conference_digest.md` §9.1、`book_ai_agent_book.md` §10.6、`notion_digest.md` §5.2）：

- **盛行率終於有了。** 2609.07360 掃 3,171 個 repo、用位元可判定的規則加三方驗證：**9.8% 裝 MCP server 完全不 pin 版本、3.1% 用看起來有範圍的授權預先核准任意執行、3.8% 帶一個替安裝者預先核准 shell 的 skill、16.0% 的設定帶安全缺陷—而原始掃描器的比率是 25.5%**。三分之一的天真掃描結果撐不過驗證，這同時是「別直接引掃描器數字」的自我紀律。
- **防禦也有了實測，而且不傷 utility。** 2609.08371（CapScope）把授權上限在讀任何 repo 內容之前就從可信輸入推導出來、把 capability 放在模型 context 之外：**注入的副作用在 baseline 是 75 次裡 33–47 次執行，在 CapScope 是 3 次**，修復成功率 68/75 對 68–72/75。這比 2026-09 引的 2609.00267「1.5 vs 8,100」更適合放進控制篇，因為它同時報了成本。
- **撤銷不等於關門，而且例子就是 GitHub。** 2609.02866：**GitHub 的工具無法把 merge 綁在被審過的那個 commit 上，受控實驗確認它可以 merge 另一個 commit**；NATS 回報沒有待處理訊息時，已派送的工作仍可能發布；Kafka 全部 broker 都套用了撤銷，而更早被授權的請求仍能寫入。對一個同時在跑這四個系統的讀者，這是本窗口最具體的爆炸半徑結果，而且講的是 provider 介面，不是模型。
- **「圍堵」與「結果」是兩個量測。** 2607.23999（ContainmentBench）：600 組配對，**兩種防禦都沒有發生實際違規，卻有 441 組（73.5%）在 12 個欄位的 trace 摘要上不同**；authorized proposal-commit 0.164（純汙染追蹤）vs 0.857（intent-ledger）vs 0.923（tool-boundary）。這句「結果一樣不代表圍堵一樣」也是 10 月四篇的收尾材料（`arxiv.md` §5 第 5 項），三部曲要避免重講。
- **人工核准的失效，換到一個乾淨的數字。** 2609.02035：光靠塑形過的 metadata 就把 skill 選擇從 **15.2% 拉到 63.5%**，而人類審查者只在 **2.9%** 的判斷裡擋下它，對照明示的引導是 91.4%。這正好取代 2026-09「動筆前必修 (2)」裡那個必須揭露受測者身分的 2608.27443—新的講法是「人只擋得住看得見的引導」，證據直接、不需要免責段。
- **東京：同一句話，三個獨立的舞台。**「Model output is input, not authorization」（`2QlDF` slide 3）、「Let agents reason; keep authorization outside the model」（slide 13 註）、「The Model Can Recommend. It Cannot Authorize.」（`2QlD9` slide 21）。其中一家把可執行的 policy 檔直接上台（`safe-gh` / `safe-push` / `safe-webfetch`，JSONC + YAML，`2QlDX` slides 34、38–55、62），並用 OWASP **ASI01–ASI09** 當攻擊路徑索引—這是控制篇那張對照表現成的骨架。日立的 workshop 把 Keycloak + agentgateway + Inspector + Tempo/Grafana 做成一份 Docker Compose 實驗室（`2RpxA` slide 12，`github.com/Hitachi/oss-assets`），是整場最可重用的工件，也是控制篇可以自己跑一遍的對象。
- **書給了機制。** ch.1 §1.2 把 harness 的 Verify 定義成「安全检查只看结构化数据…而不看模型自由生成的文本，因为后者可能已被提示注入操纵」；§4.6 的 **Sidecar** 是具體做法—一個平行的輕量 LLM 呼叫只看到 `{tool: "bash", command: "rm -rf /tmp/data"}`，看不到主模型的散文，在「数百毫秒」內放行或擋下，配一個**拒绝熔断器**在連續拒絕後交還使用者。這條是控制篇第二節現成的實作段。
- **台灣仍然沒有事故。** `community_digest.md` §1.8 最接近的是「讓 AI 火力全開的底氣，來自規範好的安全邊界」、把 agent 做進 Wayland compositor 的發行版（「信任邊界都圍著 gateway 設計…煞車也長在系統裡」，第一則留言是「目前的技術安全性很低!」）、以及一個多 agent runtime 安全治理 gateway（1 分享）。另外 LinkedIn 上一個給 `mcpproxy-go` 的第一支 PR 值得抄進威脅模型篇：外洩的全域狀態讓「a security regression test pass without actually exercising the guard」—**護欄的測試自己是綠的**。
- **Notion：控制篇的第一手地盤補齊了。** PSS、Kyverno、Gatekeeper、LimitRange/ResourceQuota、Linkerd/Istio authorization、Tetragon 都已有動手頁（`notion_digest.md` §5.2）。擋在這批材料與草稿之間的，只剩「找一位資安協作者」這一條。

**動筆前必修**（2026-09 五條保留，兩條改寫）：(1) 總論第一節切分兩層 harness（論文的 harness＝vendor runtime，系列的 harness layer＝你蓋的）；**(2) 改寫**—第二支柱的證據換成 2609.02035（塑形 metadata 91.4% vs 2.9%）與 2609.15887（純確定性的接受規則**一個假陽性都沒擋掉**），不再用 2608.27443；(3) 台灣案例改寫成「台灣還沒有公開的 agent 事故，但…」；(4) 每篇壓到 8–10 個 anchor；(5) 找一位資安協作者掛名審稿。**新增 (6)**：與第 10 條切乾淨—本條是**一個 agent 的爆炸半徑**，第 10 條是**半徑要圍著哪個 principal 畫**；identity 的材料一律讓給第 10 條。

**升級證據**（不變，加兩項）：台灣出現第一起公開的 coding-agent 事故，且 Backend 台灣的事故解剖貼文 ≥ 100 反應或 ≥ 15 分享；資安協作者確認；2608.28502 或 2608.27299 的後續研究在新一代 model 重測仍成立；Kubernetes pod certificates 或 IdP-managed MCP auth 在企業有採用案例。**新增**：2609.07360 的盛行率在第二個資料集重現，或有人把它套到台灣的公開 repo；`github.com/Hitachi/oss-assets` 的 workshop 實驗室被第二家公司拿去改造並公開心得。

**最早月份**：2027-01。若協作者找不到，與第 2 條互換，本條延到 2027-02。

---

## 4. Skills、Memory 與 Compaction：context 的第二層治理

**title_zh**：AGENTS.md 之後：Skills、Memory 與 Compaction 的實證報告

**pitch**（2026-09 版不變，摘要）：三塊沒人碰—(a) skills 的經濟學與准入；(b) memory 治理；(c) compaction。交付物：platform team 的 skill 准入 gate 與 compaction-proof 的 typed retention policy。

**本圈新增的證據**（`arxiv.md` §2 B、`conference_digest.md` §9.1、`community_digest.md` §1.5／§1.6、`book_ai_agent_book.md` ch.3／ch.9）：

- **Skills 終於被當成一個系統而不是一堆檔案來研究。** 2609.13321（SkillSeam）是 2026-09 缺的方法論：擾動一個封閉的 skill 系統，再從每個失效機制預期的通道去量—**壓平 persistence hierarchy 讓載入的 skill token +60%；一個懸空 anchor +64% token、−3.1pp 正確率；一個同義別名把非正規路徑從 0/32 推到 15/32；重疊的 lane 把歸屬衝突從 0/16 推到 14/16；平淡的 trigger 把路由衝突從 3/32 推到 30/32 並讓 token 膨脹 3.7 倍；最差的粒度組合 −12.5pp**。這六條就是 skill 准入 gate 的六個檢查項，而且每一條都有量測方式。
- **最誠實的 null 出現了，而且它同時是 11 月的材料。** 2609.12742 拿 SKILL.md 對三個 Kotlin repo 的 reverted merged PR 評分：**GEPA +4.9pp、SkillOpt +0.1pp，而 GEPA 的增益無法與 agent 的 run-to-run 變異分離**。要把它寫成「skill 優化的效果小到被變異吃掉」，不是「skill 沒用」。2609.11682 從成本側回答（比 SkillOpt 便宜 55–58%，每個 benchmark 50 個範例，跨 harness 穩健）。
- **供給的成長遠快過評估。** 2609.05571 從 19,769 個 repo 蒸餾出 **1,006,822 筆被接受的 skill 紀錄**；2609.02749 用 5,000+ 蒸餾 skill 在 MLE-bench 拿 **+134.3%**。對照 2026-09 的 2608.23067（注入「對的」公開 skill 反而掉 1.3–4.2%），矛盾沒有被裁決，但問題的形狀變了：**不是「skill 有沒有用」，是「這一百萬筆裡哪一筆對你這個 repo 有用」**—這就是「准入靠配對實測」的論證。
- **Memory 的研究問題換了。** 從「留住多少」變成「毀掉了什麼、有沒有結構」：2609.08279 用反事實還原被逐出的項目來稽核 eviction；2602.11243 發現 LLM 只有在被告知怎麼做時才會整理記憶；2609.03467 找到「silent grounding」—檢索很強但沒有變成回答品質；2606.14571 發現 memory 系統無法重用它在當下已吸收的回饋；2609.12436 把 durable 與 transient 分開，讓暫時性的 context 不能覆蓋長期知識。Context 組裝側持續有工程收益（2609.00749 −31% token；2607.01916 **−51.5% token、−36.4% 成本**）。
- **Compaction 仍然是最薄的一塊。** `compaction AND "coding agent"` 本窗口只有 1 筆；`x_digest.md` §7 明確記錄「No compaction change was announced」。2026-09 的升級條件「作者自己重跑 Compaction Cliff」，因此**仍然是唯一可行的路**。
- **東京：Skills over MCP 快定案，但 progressive disclosure 沒解。** Skills over MCP 已被接受為 SEP、「so close to final」，progressive disclosure 明講**未解**，並將成立 file-systems WG（`2QlLo` [00:37:00–00:44:22]）。反面材料來自一場影子 AI 的談話：「The risk is intent encoded in static text」（`2QlED` p.4）—這句話幾乎就是本條的標題。
- **Memory 的寫入路徑，會場上直接對立。** 一個專案預設「no LLM call by default」、用詞彙去重，並在自己的講者備註寫「This is not a calibrated probability or a semantic deduplication guarantee」（`2QlDp` slides 15、24–25）；另一個把 LLM 放進寫入路徑去「Reconcile — Decide to integrate, overwrite, or delete existing facts」（`2QlEe`）。**書採第三個、也是最嚴的立場**：§3.3.3「生产环境不应让任何一个模型绕过审核，直接改主分支或线上向量库」，改成一套 PR 流程，紀錄必須回答「从哪条证据而来、谁在什么时候批准」；§9.3.2 再加「LLM 总结只是…转换，并不是把输入变得无害的净化过程」。三方對立是一節現成的骨架。
- **AAIF 的 Gilbert 在 Friday keynote 自己點名沒有 memory WG**（`2QsV2` [00:07:15]），而基金會的 sandbox 貼文說這些專案「sitting today, unfunded and ungoverned」。**這件事不另開條目**：memory 的「治理」歸本條，memory 的「基礎設施／儲存產品」歸第 3 條，界線寫在第 3 條裡。
- **台灣第一次有可引用的第一手實作。** Claude Taiwan 一串 55 則留言的多 agent 協作實驗，最高票回覆是「compact 前要求先寫 handoff」；另一串的共識是「手動，差不多 70～75% 請 claude 先記錄目前專案進度與待辦事項，然後再壓縮 context」；還有一套 dotfiles 把原生記憶「全部砍除，只保留自己的線上 DB 記憶系統」（`community_digest.md` §1.5）。
- **准入閘不用自己發明，vendor 出了一個。** Claude Code v2.1.269 的官方 `plugin eval`：同一個 prompt 跑有／無 plugin 兩臂、預設三次、「assert 混合 LLM as a judge…三票中至少兩票通過才算過」（§1.6，25 反應／4 分享，「好像沒什麼人在討論」）。**配對、重複、多數決**—這就是本條交付物的縮小版，也是 11 月 pass^k 的一個微型範例。

**為什麼還沒進提案池**：2026-09 的反方意見（原 thesis 講過頭、第三部是三個弱關聯題的拼盤、Compaction Cliff 會過時、台灣直接訊號只有兩則）有三條被本圈削弱—方法論有了（2609.13321）、台灣第一手實作有了（§1.5／§1.6）、skills 這塊的份量明顯撐得起一個月。剩下兩條沒動：compaction 仍然綁在特定版本，而 2608.23067 vs 2608.20614 的矛盾仍未裁決。

**升級證據**（更新）：作者在自己的 repo，用當時的 Claude Code 版本重跑 Compaction Cliff 的幾個 config（**仍是第一順位，且本圈沒有任何 vendor 變更會使它失效**）；skill marketplace 出現第一起公開的供應鏈事故，或 `gh skill install`／agentskills.io 加上簽章與 provenance；2608.23067 vs 2608.20614 的矛盾有第三篇研究裁決（2609.13321 是機制解釋，**不算裁決**）；**新增**：Skills over MCP 正式定案並公布 progressive disclosure 的解法；作者拿 `plugin eval` 跑過自己的 skill 並有配對數據；memory-as-database 的產品有台灣使用者心得（§1.5 的 dotfiles 與 obsidian 決策紀錄已經很接近，但還不是「產品心得」）。

**最早月份**：2027-03（2026-11 吸收的 context 檔半部要先發布，避免自我重複）。

---

## 3. Agent runtime 是平台產品：sandbox fleet、state、memory 與 agent config as IaC

**title_zh**：Agent runtime 是平台產品：sandbox fleet、state 與 agent config as IaC

**pitch**（2026-09 版不變，摘要）：agent 的工作單位正在離開筆電。三部曲雛形：Sandbox fleet 篇 → State 與 Memory 篇 → Agent config as IaC 篇。作者是這題最過度合格的人（CNPA／CNPE／CBA／Crossplane／Argo／Kyverno 一整年的證照，Notion 承諾的 IDP 講題）。

**本圈新增的證據**（`conference_digest.md` §2／§9.1、`arxiv.md` §2 A／H+S、`x_digest.md` §8 gap 2、gap 7）：

- **東京補上了 2026-09 缺的那條脊椎：agent 的工作區是儲存產品。** 兩場把它講成 storage 而不是 compute—durability 當成有 commit point / RPO / RTO / retention 的政策（`2QlE7` pp. 4、7、13），以及 TTL、路徑範圍化的 agent credential 與**平行 agent 之間的樂觀鎖衝突**（`2QlEe`）。這比 2026-09 提的「CI runner → warm pool」更好用：RPO／RTO 是十五年的維運詞彙，套到一個新的工作單位上，正是作者慣用的歷史脊椎寫法。
- **流量層有了一個可以寫的故事，而且公開資訊自相矛盾。** **Agent Router** 成為基金會第六個專案—「Used to be called Envoy AI gateway… contributed by Tetrate and Bloomberg」（`2RaW6` [00:06:49–00:07:16]）；基金會自報：2024 年 10 月起公開開發、11 家公開採用者、9 個 maintainer 席次橫跨 5 家公司且無單一公司過半、132 位貢獻者來自 21 個組織、15 個穩定版、v1.0 在 2026-06。問題是**它和 agentgateway 的關係公開場合沒人講**（同一段話裡連續兩句提到，然後沒有下文），而日立的技術堆疊圖把兩者並列在 gateway 底下（`2QlEG` p.10）。**可用的區分要自己講**：Agent Router 是 Envoy 之上的 *model* 流量控制面，agentgateway 是懂 MCP 與 A2A 呼叫的 *agent 邊界* proxy。這是 platform team 2027 build list 上第一個選型題。
- **基金會自己承認底層是空的。** Sandbox 的門檻已從「used successfully in production at a wide scale」降到「a working implementation plus either early external interest or a credible thesis…A named, active maintainer」，回報是「standard infrastructure only. No funding, no marketing, no scanning」，時鐘是「六個月檢查點 + 十二個月申請 Growth 的窗口」。基金會的原話：agent-SRE 實務會依賴的 memory、context 壓縮與 sandbox 專案，「sitting today, unfunded and ungoverned」。**這是本條最有力的一句引言**，因為它出自要推廣這些專案的人。
- **arXiv 第一次出現 agent 工作負載的服務等級文獻。** 2609.06128（Amazon Rufus）報告 real-time／async／batch「each have distinct service-level objectives」且通常分開的 runtime，並把一張 typed dataflow graph 編到三種 binding 而**輸出品質沒有可偵測的差異**；2609.10964 把 P95 workflow flow time 壓到最多 3.50 倍快，做法是把 readiness 從釋出時機拉開；2609.03598 在 Slurm 上讓 agentic job 的 makespan −39%；2607.08565 只在「那台機器還能在 SLO 內服務」時才把後續 turn 黏到快取命中的實例上；2609.08020 從 agent 文獻之外提供 SRE 側的詞彙。**負面同樣重要**：17 筆 `"error budget" OR SLO` 命中**全部**是 LLM serving 的延遲，沒有一篇是 agent run 的 error budget—12 月那篇仍然是首發。
- **2026-09 的升級條件之一其實是壞查詢。** `(sandbox OR "agent runtime" OR "internal developer platform") AND Kubernetes AND agent` 本窗口 **0 筆**，`sandbox AND agent AND (Kubernetes OR container)` 也是 0。修法在 `conference_digest.md` §9.5：改用 `abs:"durable" AND abs:"sandbox" AND abs:"agent"` 與 `abs:"agent workspace" AND abs:"persistence"`。**在查詢修好之前，不能把 0 筆讀成「沒有研究」。**
- **build vs rent 變成一個決策工件。** `x_digest.md` §8 gap 2：Agents API、Managed Agents、Cursor cloud、Omnigent—技術篇假設你自己蓋，feed 上現在是用租的。「harness 是別人的一個 endpoint 時，你 pin 什麼？」是 12 月可靠篇 change management 那節接不住、只能留給本條的問題。gap 7 補上 2026-09 缺的 agent config as IaC 證據：AWS Agent Registry、Google plugins、Hermes CRD—把 agent、tool、skill 編目成同一個單位。
- **CNPE 仍未過關。** `notion_digest.md` §1：第二次考試已預約、截至 09-14 沒有 PASS 紀錄，mock 02 還是 16 個空標題。總論開場的資格與插曲的排期都卡在這裡。

**為什麼還沒進提案池**：2026-12 已把它壓成一節並明講「留給未來的 agent runtime as platform product」；SLO 要先定義（2026-12）才有東西給 fleet 用；仍然是 build list 而非決策敘事—但**脊椎問題本圈解決了一半**（儲存產品 + RPO/RTO），剩下的是書錨。

**升級證據**（更新）：CNPE 過關、Golden Kubestronaut 到手；KubeCon NA 2026-11 出現 ≥ 3 場以 agent sandbox／AI factory／inference on K8s 為題的講題；宣告式 agent 資源進 GA；台灣有公司在 DevOps Taiwan、CNTUG 或 Grafana & Friends Taipei 分享「自家 K8s 跑 agent fleet」；Kubernetes v1.38（預計 2026-12）有 agent 相關 KEP；**改寫**：用修好的查詢字串（`durable AND sandbox AND agent`）再出 2 篇以上，舊的字串作廢；**新增**：Agent Router 與 agentgateway 的關係有任何一方的正式說明（部落格、KEP、maintainer 會議紀錄）；AAIF Sandbox 的第一次年度回顧公布 acceptances／graduations／archivals 三個數字。

**最早月份**：2027-02；建議 2027-03，讓 2026-12 SRE 的 SLO 詞彙先沉澱。

---

## 2. 知識流失與維護債：吞吐量免費之後，組織付的帳

**title_zh**：知識流失與維護債：吞吐量免費之後，組織付的帳

**pitch**（2026-09 版不變，摘要）：團隊層的組織篇續集，只用硬數據（2607.09902、2606.13298、2607.05677、2608.25241）。三部曲雛形：維護債篇 → 決策記憶篇 → 團隊篇。書錨候選：Beck 或 Meadows；骨架用 CLD 或 TOC 的瓶頸遷移。

**本圈新增的證據**（`arxiv.md` §2 J、`community_digest.md` §1.4／§1.9、`conference_digest.md` §9.1）：

- **縱向研究側掛零。** 兩條監看字串本窗口都是 0：`("technical debt" OR maintenance OR "code quality") AND "coding agent" AND (longitudinal OR "post-merge")`、`"architectural decision" AND agent AND memory`。擴展查詢也只有 `"technical debt" AND "coding agent"` 1 筆、`"code quality" AND "coding agent"` 2 筆。**2026-09 的升級條件「再出 1–2 篇縱向研究」未達成。**
- **但組織側出現了本窗口最好的一句框架。** 2609.04630：**執行可以彈性擴張，驗收權威不行**—一個 Human-Agent Cell 產得出證據，卻拿不到驗收權威。這句話比 2026-09 的任何一則台灣貼文更適合當維護債篇的第一節標題。
- **開源的版本叫「stewardship community」。** 2609.12236：一小群核心保留實作權威，因為審查成本已經不值得為外部 patch 付；於是 AI 取代的是**實作勞動**，而被削弱的是**開源自我更新的方式**。這正好是「吞吐量免費之後付什麼帳」的另一種帳本。
- **開發者真正在吵的是什麼，有了 25,227 筆的答案。** 2609.04680 在 VS Code 社群從 43,806 筆候選 issue 篩到 25,227 筆，發現討論被 **agent 管理、設定、可靠度、認證與帳務**主導，而 hallucination 與授權條款（licensing）「rarely surface」。這是對「調查法問卷」的糾正，也順便替第 6 條的重切背書。
- **台灣這邊，軼事變強了。** Backend 台灣一位常貼作者的「夢境」貼文（217 反應／12 留言／15 分享，本圈該社團最高）講 AI 寫的 code 進了共用 library，留言區補上一個具體反例：沒訂閱走到 `answerFree` 時它又 call 回 `answer`、把 `subscribed=True`—「測試會過，但迭代上去時…應該很災難」。另一則留言：「接力修到的 code 多的是這種 if 大堆疊…27 吋螢幕還要 page down 個六次七次八九次」。**這不是事故報告，但它是本條需要的那個開場軼事**，而且 `community_digest.md` §5 機會 6 已經給了格式：把「不可讀的 agent code 被合併」當成一次事故來寫 timeline、contributing factors 與 action items，而不是當成風格抱怨。
- **情緒暫存器也到位了。** §1.4：一位 DevOps Taiwan 管理員轉貼的「套殼…被打碎」（32 反應）、Agile 內湖 Sprint 45《與我的 AI 焦慮共處》（12/3/7）、「工程師的能力正在流失」（53/6/9）、Backend 台灣的兩串 127/12 與 103/12、Claude Taiwan 的「AI 真的跟鬼一樣」（109/10/22）。digest 的判讀很直接：**本圈這批讀者在讀焦慮，不在讀 harness**。
- **東京替它命名。** 「intent debt」是從舞台上講出來的（`2QlDU` 摘要），機制是：agent 起草規格時會用一個有自信的猜測把空缺填掉。另一場給了反例—「The docs were complete. Agents still got it wrong.」（`2Qn4a` slide 42）—文件齊全不等於決策被保存，這正是決策記憶篇的論點。
- **`Fb temp` 仍未貼粉絲團。** `notion_digest.md` §6 顯示該頁 09-08 只增加了 AGNTCon 行程段落。升級條件之一未動。

**為什麼還沒進提案池**：原題駁倒後重建的軸（知識流失與維護債）證據結構沒變—硬數據全在 2026-09 引的四篇上，本圈只加了組織側的三篇與一批軼事。人篇仍不寫（headcount、中階主管）。

**升級證據**（更新）：2026-11 變異篇發布後，讀者對「ADR／決策記憶一節」的回應超過其他節；`Fb temp` 貼到粉絲團的反應 ≥ 20 或分享 ≥ 5；2607.09902／2606.13298 類型的縱向研究再出 1–2 篇（**本圈 0**）；DDDesign Taiwan 或 DevOps Taiwan 再出現「想不起來為什麼長這樣」類貼文；**新增**：2609.04630 的「驗收權威不隨執行擴張」在第二篇研究出現，或有台灣團隊公開講他們的 review 容量政策；有人把 §1.9 那個 `answerFree` 反例寫成公開的事後檢討。

**最早月份**：2027-01（若第 1 條缺協作者則本條先上）；建議 2027-02。不論排哪個月，不寫 headcount 決策敘事。

---

## 10. Agent identity 與委派授權：一千個員工，沒有一個有名字（新）

**title_zh**：Agent identity 與委派授權：爆炸半徑要圍著哪個 principal 畫

**pitch**：這是整場東京唯一的主題，同時具備工作組、有主席的資安 WG、一個 workshop、一個已合併（實驗性）的 Keycloak PR，以及一個沒人回答的問題。那個問題是從台上直接丟出來的：「do you know which agent did what? Can you revoke access to just one of them? Can you prove to an auditor that your agents only touched what they were supposed to?」（`2QlEM` 摘要，該場**沒有 deck**，唯一的其他紀錄是一位與會者的 LinkedIn 摘要）。配套材料：關聯式授權的「revoking staging access automatically suspends production too, something role-based systems can't express cleanly」（`2SrLI` 摘要）；日立 workshop 的漸進式授權—「the scope grew, the tool did not change」（`2RpxA` slide 20）；**Keycloak PR #46048 已在 26.7 合併為實驗性功能、PR #49998 審查中，而 Keycloak 自己建議不要用在生產**（AAIF，2026-09-09）；MCP 共同作者在 keynote 說授權／身分「maybe not the most technically interesting piece, but… conceptually one of the most important parts of agentic systems」（`2QrbB` [00:22:29–00:22:38]）。arXiv 側的收斂設計是同一件事：**授權是 context window 之外的一個 typed object，不是裡面的一個字串**—2609.14631（單調收窄）、2609.14744（**32 個單元裡沒有任何單一單元能提供完整的啟用剖面**，五來源稽核、1,248 組 field pair）、2609.05920（授權綁在傳遞閉包的根上）、2609.02690（attested lease）、2609.08371（CapScope）。阿姆斯特丹再加一場「What IS an Agent's Identity」（`community_digest.md` §1.8）。

**為什麼是新條目而不是第 1 條的一節**：第 1 條問的是**一個 agent 能炸多大**，本條問的是**半徑要圍著哪個 principal 畫**—誰簽的名、誰能被單獨撤銷、稽核員看到的是哪一個主體。兩條的證據有一半重疊（CapScope、agentgateway、per-run identity），所以**只能上一條**，或者第 1 條刻意把 identity 整節讓出來。切分規則寫在第 1 條的「動筆前必修 (6)」。

**為什麼不是現在**：台灣目前只有「安全邊界」「信任邊界」層級的討論（§1.8），沒有人在談 agent 的身分；Keycloak 自己說別上生產，寫成決策敘事會變成「等標準」；作者的地盤（SPIFFE 式身分、least privilege、network policy 在 CKS／KCSA 裡）能轉移，但這是 K8s 的詞彙，不是 IdP 的詞彙。

**升級證據**：AAIF authorization WG 或 Identity & Trust WG 產出第一份公開規格草案；Keycloak 的 agent 授權功能脫離實驗性，或 EMA／ID-JAG 有第二家 IdP 實作；台灣有公司在社團或 meetup 公開他們怎麼發 agent 身分（即使只是 per-run service account）；2609.14744 的「32 個單元裡沒有任何單一單元能提供完整的啟用剖面（五來源稽核、1,248 組 field pair）」在一年後重測仍成立；`abs:"agent identity" AND (abs:"delegation" OR abs:"authorization")` 這條新查詢在兩個月內累積 ≥ 3 篇。

**最早月份**：2027-02。與第 1 條互斥，同一季只上一條。

---

## 8. 艦隊不是免費的：multi-agent 拓樸的實證

**title_zh**：多一個 agent 不等於多一份證據：multi-agent 的實證帳

**pitch**（軸改寫）：2026-09 的軸是「拓樸選型表」，證據是實驗室 benchmark、與 model 版本強耦合。本圈換軸：**多 agent 的問題不是拓樸，是證據根數**。2609.01873 把一個證據根固定住、讓報告數從 1 增加到 32，**天真的後驗覆蓋率從 0.940 崩到 0.263**；把證據根從 1 提到 16 才把落差補回來。2609.05587 補上機制：**被汙染的工具，採用率每一個都超過三分之一，網頁搜尋到 68.0%**，而 agent 在內部認得出衝突，對外只呈現被汙染的那個答案。接上 2026-09 的 2609.02925（共用上游 telemetry 的 agent quorum，故障域是 1），三篇合起來是一個**完整的、反對「再加一個 reviewer agent」反射動作的論證**，而且不依賴任何 model 版本。

**本圈新增的證據**：

- **拓樸那條舊論點被換成一個有條件、有標價的版本。** 2609.13890：階層式在最簡單的三分之一贏 **2.4 個 pass@1**、在最難的三分之一贏 **21.1**，代價是 **~10 倍 token**；而且**用預算對齊之後排行榜會重排**—六個成本感知方法橫跨 21.6pp，兩個原本領先的 baseline 校準後落後。2609.02264 發現經獎勵篩選的拓樸**收斂到大約六種不同的圖**，且邊數與 token 消耗呈**負**相關。
- **故障域的論證有了數字。** 2608.28553：單一 process 的 plugin harness 在一次注入故障下**輸掉每一個 session，得分 1.5%**。
- **產業反例也要寫進去。** 2609.15877：Ericsson 的多 agent reviewer 提出 >200 個問題，**由該公司自己的開發者判定 96% 正確**，其中約 69% 重要、約 33% 嚴重。本條不能寫成「多 agent 沒用」。
- **東京的治理框架。**「governance in a multi-agent system isn't a policy document. It's the full data path」（`2QlDL` 描述）；reviewer 艦隊的凍結版本規則—「Independent reviewers challenge the same revision — Frozen artifact, one exact revision」（`2QlEJ` slides 26–27）。後者已被指派為 10 月 Review 篇的插入句（`conference_digest.md` §4），所以**本條不能再把它當主證據**，只能當前情提要。
- **書的不變量。** ch.10 §10.4.3：「审核者不能修改测试、证据采集器或发布门槛；否则「独立验证」会退化成自我批准」；ch.10 §10.5 的多 agent 拜占庭故障。§10.5 已排進 12 月總論 §五（`selection.md` §1），本條引用時要改角度或換段落。

**為什麼升級**：2026-09 判它「證據多為實驗室 benchmark、與 model 版本強耦合，半年後可能翻轉」。2609.01873 的機制—**證據根數決定後驗覆蓋率**—是統計性質，不是模型性質；2609.02264 的「收斂到六種圖」也不隨版本翻轉。決策工件也跟著換：不是拓樸選型表，是**一張「這個艦隊有幾個獨立的證據根」的檢查表**，加上 token 帳。

**還缺什麼**：台灣訊號仍然只有 2026-09 那一則 21 讚的「艦隊模式」留言；作者仍然沒有營運多 agent 拓樸的第一手數據。

**升級證據**：作者 2026-11 變異實驗的三組延伸出「單 agent vs manager-worker」的第四組並有數據；台灣團隊在社團公開艦隊模式的**成效**（不只是「怎麼設」）；2609.01873 的證據根論證在軟體工程情境（不是一般推理任務）重現；`abs:"multi-agent" AND (topology OR coordination) AND "software engineering"` 這條字串的命中數從 1 回到兩位數。

**最早月份**：2027-04（提前一個月，因為軸換成統計性質之後不再需要等 model 版本沉澱）。狀態：**候選**。

---

## 5. Agent 的探索式測試：testing 不能自動化，所以 tester 要去「用」它

**title_zh**：Agent 的探索式測試：checking 之外，tester 拿 computer-use agent 去用它做出來的東西

**pitch**（2026-09 版不變，摘要）：checking 之外，tester 對 agent 產出與 harness 本身的 exploratory testing 長什麼樣。書錨：Hendrickson《Explore It!》。

**本圈新增的證據**：

- **第一個「agent 去用另一個 agent 的產品」的完整實例。** 一家日本公司讓 **AI 打真的電話**去測自己的語音 agent，而 harness 刻意選 reasoning model 而不是即時語音 model，理由是「better at following instructions and staying on script」（`2QlDg` p-14）；六個工具的表面、「Same tools every time. Only the prompt we hand the AI changes」（p-21）、收尾是「AI products, tested and monitored by AI」（p-27）。另一場給了斷言形式：trajectory assertion 加 mocked tool（`2UjnC` 摘要）。**注意**：p-14 與 p-21 這兩筆已被指派為 10 月測試篇 §八的插入句（`conference_digest.md` §4），本條要用的是**整個 harness 選型的故事**，不是那一句。deck 是 OCR（`p-N` 標記），引述要保守。
- **台灣的開場軼事到位了。** Claude Taiwan 一個做台灣電商的設計工作室：「Vibe Coding 最容易漏掉的 Bug，可能根本不在 Code 裡…程式碼沒有 error。API 串接正常。Webhook 也有收到…但整間商店跑起來，就是會出事」，回覆是「每個 function 都沒錯，不代表 system 沒錯」（27/2/2，`community_digest.md` §1.2）。這一句就是本條的第一段。
- **arXiv 仍然是空的。** `("exploratory testing" OR "computer-use agent" OR "GUI agent") AND (testing OR QA)` **0 筆**；擴展查詢 `"exploratory testing"` 1、`"computer-use agent" AND testing` 3、`"GUI agent" AND testing` 4。這題的證據來源會是實務與書，不是論文—寫的時候要誠實說。
- **JSTQB 秋季大會 2026-10-16 還沒到**，議程仍是升級條件之一。

**為什麼還沒進提案池**：2026-10 已佔掉測試主題的席位，半年內不宜再有測試題；computer-use agent 當 E2E substrate 的成熟度與成本還在變；作者的探索式測試待讀清單還沒讀完（`notion_digest.md` §2：`Asking Testing Seriously` 仍停在 2026-03 的節錄狀態）。

**升級證據**（不變，加一項）：2026-10 發布後讀者對「探索式測試一段」的回應；作者在工作上用 computer-use agent 跑過至少一輪 exploratory session 並有數據；JSTQB 10/16 或 STARWEST 出現「exploratory testing with agents」講題；Whittaker／Hendrickson 讀完；computer-use 定價下降到可日常使用；**新增**：語音 agent 那場的 server 真的開源（描述說「We are open-sourcing the server」但 **deck 裡沒有任何 repo URL**—要去問講者），有 repo 才有可重現的範例。

**最早月份**：2027-04（與 2026-10 隔半年）。

---

## 11. 免費的 tool call 有人在付：MCP 生態的可用性（新）

**title_zh**：免費的 tool call 有人在付：把 MCP 生態當成會消失的上游依賴

**pitch**：兩場講付款，方法完全不同，前提一樣—今天的工具生態之所以免費，是因為有一個維護者在付錢：「Every free tool call has a payer. Right now, it's the maintainer」、「402 was not invented for this. It was waiting for it」（`2QlDO` slides 6–7，背後的生態研究是投影片引用的 arXiv:2608.00150—**21,000+ servers / over 60% unpaid / 41.6% gone 3 days later / 232% growth over 6 months**，用前要回原論文核對）。對面是同一場會議的另一種答案：執行前的證明加上對抗性驗收測試—「forged evidence => reject; changed payment => no signature; replayed request => no second payment; concurrent spend => no budget overrun」（`2VRYC`）。

**但本條最強的框架是可用性，不是經濟學**：一個「三天後就不見了」的依賴，先是 uptime 問題。本窗口的 arXiv 把這件事量到了族群規模—2609.14119 收割**整個公開 registry（21,643 servers、72,606 個版本紀錄）**，發現 **51.1% 的多版本 server 改掉了它宣告的內容、40.6% 是無聲改的、4.2% 換了 endpoint host 卻保留 registry 身分**，無聲漂移帶著高嚴重度發現的 OR = 2.96，而星數幾乎沒有保護力（每 log star OR = 0.78）；2609.10962 從 24,135 個 server 的普查裡抽 400 個未修復的機率樣本，**只有 48.8% 完成得了 initialize 握手**（策展過的 66.7%），最大宗的失效是根本啟動不了（37.5%）；2609.15397 量 98,291 個工具的註記詞彙，發現欄位普遍有填，卻沒有一個能表達 workflow 需要據以推理的外部效果；2609.14721 直說研究缺口：**33,319 個 MCP repo 有 93.7% 把它當成使能技術用，而不是分析或加固它**。

**決策工件**：MCP 依賴的 SLO 表—pin 版本、握手健康檢查、endpoint host 變更告警、宣告內容 diff、以及「這個 server 消失時 harness 退化成什麼」的降級路徑。

**為什麼不是現在**：付款協定（x402、AP2、UCP）都還在宣布階段，寫成決策敘事會過季；台灣完全沒有訊號；而且它和第 3 條的 MCP gateway、第 1 條的供應鏈資安三方切面重疊，要先確定它不是那兩條的一節。**分界建議**：第 1 條問「這個 server 會不會害我」，第 3 條問「我怎麼把它擺進平台」，本條問「它明天還在不在」。

**升級證據**：2609.14119 或 2609.10962 有第二次普查可以做時間序列（消失率是不是穩定的）；有人公開一份 MCP 依賴的事故報告（server 消失或換 host 造成的生產影響）；x402 或 AP2 有第一個非示範性質的生產採用；台灣有團隊在社團問「我們自架還是用公開 MCP server」；`abs:"MCP server" AND (abs:"ecosystem" OR abs:"availability")` 累積 ≥ 3 篇。

**最早月份**：2027-03。

---

## 6. Model 供應是上游依賴：席位、額度、斷線與本地混合

**title_zh**（重切後）：harness 的模型可攜性：同一份規格，四個 model，幾輪修補

**pitch**（2026-09 的三篇結構保留：韌性篇／本地與混合篇／Token 流向篇），但本圈出現**一條繞開讀者錯位的重切**：

- **台灣自己做出了第一張 pass@1-by-model 表。** 搞笑談軟工的版主讓四個 model「在同一套 specification、同一套 harness 下，依據 10 個 Problem Frames 規格，從頭產生 Product Aggregate 的完整後端程式」（DDD + Clean Architecture + CQRS + Event Sourcing + Design by Contract），一輪通過 Gate 的結果是 **Fable 9/10、Opus 8/10、Sonnet 5/10、Haiku 1/10**；最弱的那個第一次生成花 148 分鐘、總共 **40 個修補輪**（236 反應／32 留言／41 分享，本圈全社團最大的一串）。他自己的說法是「故意找能力比較弱的 Haiku 來驗證我的 AI Coding 方法論的邊界」，另一串是讀者問「地端 LLM 可否跑我的 AI Coding 專案？」（107/9/12）。
- **這把本條從抱怨換成一個工程指標**：**一套 harness 的好壞，等於它在 model 變便宜、變小、變本地時退化得多優雅；量法是每個 gate 的修補輪數 × model**。它同時接上 Claude Taiwan 那八串額度貼文裡真正有形狀的兩個詞—「分層派工」與「混用模型」（§1.7）—以及 Red Hat 那則的提問：「下一個模型發布時，你需要重建嗎？」（§1.3）。
- **東京給了企業版的同一句話。** 兩份印上日期的 model 名單，以及那句操作性的框架：「Budget pressure makes self-hosting an operational decision rather than a research one」，而且名單是「by the hardware they need, not by how good they are」分組的（`2So56` slides 3、9；`2QlEY` p.6 標「Verified September 11, 2026」）。反面則是一個 29 turn 之後被放棄的 open-weight session（`2QsV2` [00:03:24–00:03:42]）。
- **成本側的反直覺持續累積。** 2609.13890（階層式 ~10 倍 token，且預算對齊會重排排行榜）；2607.02436（測試工具讓成本 **+42–68% 而功能與可靠度都沒有增益**，但 xHigh reasoning 用多 9–29% 的成本換到 first-try-perfect **28% → 89%**）；2609.11076（specify-and-verify 在五個 Rust/Verus 元件上成本全部更貴）；2609.01600（一個有限參考語意就能精確決定的東西，花掉約 3,000 個 reasoning token）。`x_digest.md` §8 gap 4 補上 feed 版本：會更貴的 routing、harness 層快取、「$38 的瑣碎問題」、「Inference FinOps」變成職稱。
- **開發者真正在吵什麼，也支持重切。** 2609.04680 的 25,227 筆 VS Code issue 由 **agent 管理、設定、可靠度、認證與帳務**主導—帳務是其中之一，但不是主角。

**為什麼仍是觀察中**：2026-09 的升級條件第一項「3–5 家台灣公司的企業層採購型態觀察」**缺一不可**，本圈沒有任何進展；Claude Taiwan 的八串仍然全是個人席位（630 元台幣變 630 美元那串 154/46/3 是最典型的）。重切解決的是**角度**，不是**讀者**。

**升級證據**（第一項仍缺一不可，新增一條平行路線）：3–5 家台灣公司的企業層採購型態觀察；Grok Memphis 等級的 vendor outage 再發生且有台灣團隊公開影響；主權模型政策有具體法規動作；vLLM 台北 meetup 第二場以上；Claude Taiwan 以外的實務社團出現席位／額度討論。**新增（可取代第一項，走可攜性路線）**：作者或社群產出一張 harness portability 表—同一份規格、同一套 harness、≥ 3 個 model，報一輪通過率與修補輪數—並且至少包含一個地端 model；那位版主的地端 LLM 重試有結果。

**最早月份**：2027-03。狀態：觀察中。

---

## 7. 棕地的設計維度：用 DDD 與 Event Storming 讓 legacy 對 agent 可讀

**title_zh**：棕地的設計維度：用 DDD 與 Event Storming 讓 legacy 對 agent 可讀

**pitch**：2026-09 版不變（邊界篇／現代化篇／設計記憶篇；DDDesign Taiwan 是資料集裡貼文數最多的實務社團）。

**本圈新增的證據—幾乎沒有，記第一次空手**：

- **arXiv 完全空。** `("domain-driven design" OR "bounded context" OR "event storming") AND LLM` **0 筆**；擴展 `"domain-driven design" AND LLM` 0、`"event storming"` 0、`"bounded context" AND LLM` 3 筆**且三筆全部無關**（一個 TTS codec、一個電網 QA 渲染器、一個長時程軌跡模型）。
- **社群也空。** DDDesign Taiwan 本圈只有管理公告：官網重啟加知識庫（24/1/4）、Line 與 Telegram 十月關閉全面轉 Discord（25/1）、一則 Impact Mapping 訪談（16/1）、一位新成員的 `handoff-semantics` .NET 8 參考實作（3）。**沒有任何 agent 相關討論。**
- **唯一的新材料來自東京，而且只有一句。** context graph 被當成「承載決策而非程式碼」的工件，而且是直接對著棕地講的：「your agent inherits code, not decisions」（`2QlDU`；`2WZJf` slides 17、29）。同一份 deck 預告了一本可能的書錨：《GraphRAG: The Definitive Guide》（O'Reilly，2026-12，`2WZJf` slide 37）—但那是 GraphRAG 不是 DDD，別混用。

**狀態處置**：維持 `候選`，但**記第一次空手**。依使用規則，若 2026-11、2026-12 兩圈仍無新證據，降為 `觀察中`。另一個現成的動作在 digest 裡：DDD Taiwan 十月轉進 Discord 而且明說「bot-friendly」，那是 10 月系列上線後投放的地方（`community_digest.md` §1.10）。

**升級證據**（不變）：DDD Taiwan 年會出現 agent + DDD 的正式講題並被分享 ≥ 10；作者讀完 Evans 或 Brandolini 並有讀書筆記可當書錨；2026-11 變異篇的段落引來 DDDesign Taiwan 的討論；2608.28972 類型的 legacy 現代化案例再出 1–2 篇。

**最早月份**：2027-05。

---

## 12. MCP task lifecycle 與長時間工作（新）

**title_zh**：一個會等三小時的 tool：MCP task lifecycle 怎麼觀測、怎麼驗收

**pitch**：這是規格改了、而會場上沒人討論、卻打破 request/response 心智模型的那一條。Tasks 被移到擴充，改成 `tasks/get` / `tasks/update` / `tasks/cancel`，`tasks/list` **整個移除**（`2RcMn`）；MCP 共同作者在 keynote 講用途：「MCP task allow things that can take minutes, hours, weeks or even months and then return the result back」（`2QrbB` [00:21:06–00:21:13]）。具體版本在語音那場：一個會**阻塞整通電話長度**的 stateless MCP server—「The server does the waiting. The model just calls and waits」，而且作者自己把它一般化了—「A tool that waits is not specific to phones. The same idea applies to deployments, human approvals, and long-running jobs」（`2QlDg` p-19、p-27）。書的 ch.6 §6.2 事件觸發材料是同一件事的另一半。

**為什麼是 backlog 而不是 12 月的一節**：12 月的 SLI 全部假設 run 有一個結束；一個跑幾週的 task 會把 run availability、error budget 視窗與 `min_events` 全部打壞。但目前只有**一份生產說法**，而且來自同一個 deck。

**升級證據**：第二個生產帳（不同公司、不同領域）出現；Tasks 擴充在 MCP 規格裡定案並有 ≥ 2 個實作；OTel GenAI semantic conventions 開始討論長時程 span；`abs:"Model Context Protocol" AND abs:"task"` 有第一篇論文；12 月系列發布後讀者問「跑三天的 run 怎麼算 availability」。

**最早月份**：2027-02。狀態：觀察中（第二個生產帳出現前不主動提案）。

---

## 13. 碳與成本感知的 agent 工程：先是可靠度，才是綠色（新）

**title_zh**：有界重試與 right-sizing：把碳與成本當成可靠度控制

**pitch**：整場東京唯一一場**自己公布範圍限制**的量測：「The result supports a Workflow claim — not an Energy claim」（`2QlEh` slide 36）、「The controls changed together; the observed reduction cannot be attributed to one control alone」（slide 34），以及會場唯一一份完全可重現的量測—「Repeated runs produced identical experiment outputs. The implementation uses Python 3.10.12, the standard library, and zero external API calls」（slide 35）。它的工程內容**先是可靠度控制、才是綠色控制**：有界重試加上宣告好的停止條件、right-sizing、以及「Context is every input sent to a model; keep only what each step needs」（slide 13）。書的 §7.6.3 三層成本模型是同一件事的另一種寫法，而且明確把「日志与追踪存储（用于可观测性）」算成一層成本、要求**每任務成本上限自動終止迴圈**。

**為什麼是觀察中**：一場、一家公司、且作者自己說不能歸因到單一控制；台灣沒有碳議題的工程訊號；ESG 敘事對本系列的讀者（Engineering VP／Staff）不是決策語言。

**不論它會不會變成主題，slides 34–36 都值得引**：它是「誠實界定範圍」的範本，任何一個月談量測時都可以當對照—而且和 `2So56` slide 17 的方法學警告（「Five other conditions differed besides the model」）互相呼應。

**升級證據**：第二家公司公布 agent 工作負載的能耗或成本量測且標明範圍；歐盟或日本出現與 AI 工作負載能耗相關的申報要求；`lean-agentic-ai` 類專案有非作者的採用；12 月的成本 SLI 上線後，作者自己量得出「有界重試省了多少」。

**最早月份**：2027-Q2。狀態：觀察中。

---

## 14. 日本作為需求訊號（新）

**title_zh**：（未定；可能不是文章，而是讀者假說）

**pitch**：`x_digest.md` §8 gap 8 把三件事擺在一起—一場給業務使用者的 Claude Code 講座**約 2,000 人報名**（2026-09-17）、一本 Codex 的書在排行榜第一、一本講「控制 AI 波動」的書（《確率論から決定論へ》）—結論是，作者的 zh-TW／ja 跨海與 11 月的主題**有一群會付錢的讀者**。東京現場補上同一件事的另一面：整場 85 則 X 貼文裡**沒有一則繁體中文**（作者自己那兩則是英文寫的），主流日本科技媒體只有一篇報導，寫的是 keynote；AAIF 有「over 140 ambassadors from 60 plus countries」卻**只有兩位來自日本**，而日本申請者會被排程外審查（`2QsUJ` [00:04:21]、[00:04:57–00:05:24]）。

**這條的形狀還不確定**：它可能是一個主題（「日本企業怎麼導入 agent，台灣可以抄什麼」），也可能只是一個**發行策略假說**（英文版該不該加日文版、該不該投日本的社群）。`community_digest.md` §4 已經給了一半答案：英文版十天 +16 views 追平中文四篇的 +14，Medium 的推薦流在分發英文。所以本條先當**假說**記著，不當主題提案。

**升級證據**：作者的英文版在日本的 referrer 或讀者來源有可見比例；AAIF Japan 的 ambassador 名額開放且作者考慮申請；東京或大阪的 agent 社群（Agentic Tokyo）出現可投稿的 CFP；11 月變異篇發布後有日本讀者回應；台灣社群第一次出現東京／阿姆斯特丹／聖荷西任一場的討論（本圈是 0）。

**最早月份**：2027-Q2。狀態：觀察中。**不要**在證據還只有三則書與活動數字時寫成「日本市場分析」—作者沒有那個地盤。

---

## 9. 去技能化：當 agent 代替思考，工程師如何保住知識主權（單篇）

**title_zh**：去技能化：當 agent 代替思考，工程師如何保住知識主權

**pitch**（2026-09 版不變，摘要）：文化長文而非三部曲，是《與不確定性共舞》（619 views／98 reads，2025 年中文最高 views）的續集；hook 會傳播但完讀率低（16%），所以要在前三分之一就給決策工件。

**本圈新增的證據**：

- **第一次有行為面的量測，而且它說語言是落後指標。** 2609.06213：**11,429 份審查、400 位重複審查者、207 天，核准率從 30.5% 升到 36.6%**（p = 8.6e-8，d = 0.25），同時四個人工設計的語言特徵**沒有單調下降**，用它們訓練的分類器落在多數決基線之下；embedding 抓得到訊號（MLP F1 = 0.74），而 Granger 分析說**核准率的改變先於語言的改變**。翻譯成本條的話：**習慣化是行為先發生，說法後跟上**—靠讀 review 文字判斷「審查者還在不在狀況內」，量到的是落後指標。
- **東京把同一篇論文從治理投影片引出來**（`2QlDX` slide 16 引 arXiv:2606.22721，標 OWASP ASI09），並在另一場給了配重—「The last 10% is mine.」（`2Qn4a` slides 10、14）。**注意**：slide 16 那一筆已被指派為 10 月 Review 篇 §三的插入句，本條要用的是 2609.06213 的完整設計，不是那句引用。
- **arXiv 側仍然只有三篇，而且散落。** `(deskilling OR "skill atrophy") AND developers AND AI` **0 筆**；擴展 `deskilling AND AI` 2、`"skill atrophy"` 1。cluster J 的明確結論：「Backlog item 9 has three papers across both branches and that is all」—2608.23642（現行 agent 設計既阻礙監督，也侵蝕監督所需的能力）、2606.12432（把 capability displacement 列為退役系統留下的六種「AI debris」之一）、2609.03456（已引）。
- **情緒暫存器在 §1.4**（同第 2 條）。Agile 內湖 Sprint 45《與我的 AI 焦慮共處》2026-09-23 是最近的一個現場。

**升級證據**（不變，加一項）：2026-11 發布後社群對去技能化一段的回應；「去技能化 2.0」podcast 或那篇 18k 字論文正式發表；2608.30572 類的教育研究再出；粉絲團貼 Kent Beck 類貼文分享數再破 20；**新增**：2609.06213 的習慣化曲線在第二個資料集重現，或有人在 agent PR（而非人寫的 PR）上量到同一條曲線。

**最早月份**：2027-Q1 任一月當插曲（不佔主題席位；可作為粉絲團導流的長文）。

---

## 插曲（不佔主題席位）

- **東京現場筆記：AGNTCon + MCPCon Japan 給台灣讀者**（新，**時效性最強**）。條件全部成立：台灣 14 個社團**零貼文**、85 則 X 貼文裡沒有一則繁體中文、日本主流媒體只有一篇談 keynote；作者是在場的人，有兩則現場貼文（Day 1 的 15 反應，Day 2 的 demo 影片 234 觀看、12 反應）與一份逐場筆記。格式上有數據支持：作者**歷來 views 最高的一篇是 5 分鐘的課程筆記**（3,000 views／307 reads），會議筆記型短文正是他跑得動的格式。**風險是它會過期**—阿姆斯特丹（09-17/18）與聖荷西（10-22/23）一落地，「日本首場」就不是新聞了。建議：10 月上旬，與 10 月四篇的排程錯開，只寫五到七個機制加一句台灣可以抄什麼，不寫綜述。素材與引用紀律見 `conference_digest.md` §8（24 句可引語）與 §1（紀錄的限制：20 場沒有 deck、五場只有作者自己的現場筆記）。
- **PSTN、語音與物理世界的動作空間**（新）。兩天裡最完整的一條 end-to-end harness 故事，而且落在三個主題都不碰的領域：一個為電話長度而阻塞的 stateless MCP server（「Making MCP stateless does not make the call stateless」，`2QlDg` p-17）、六個工具的表面、用「照腳本走」而不是「自然」來選模型（p-14）、「Same tools every time. Only the prompt we hand the AI changes」（p-21）、收尾「AI products, tested and monitored by AI」（p-27）。**未決事項**：描述說要開源，deck 裡沒有 repo URL—先問到 repo 再寫。deck 是 OCR，引述保守。最早 2027-Q2。
- **我的 Golden Kubestronaut 之路 ＋ agentic platform engineer 的認證地圖**。條件不變：CNPE 第二次過關。**本圈狀態：仍未過關**—考試已預約，`Golden Kubestronaut Learning Plan` 自 2026-09-01 未動、`CNPE Mock Exam 02` 自 09-07 建立後仍是 16 個空標題（`notion_digest.md` §1、§6）。排期：過關後的下一個月；**不要跟 2026-12 撞**。
- **`Fb temp` 軟體腐化貼文**（2026-09-02 草稿）：**仍未貼**。該頁 09-08 的唯一變動是加了 AGNTCon 行程段落。它的反應數仍然是第 2 條的升級證據之一。
- **（沿用，未動）** 2026-09 列的其他插曲候選不變。

## 已被 10–12 月吸收、下圈不要再提的訊號

2026-09 的表格全部保留（Review 容量與 reviewer 艦隊 → 2026-10 Review 篇；審 agent 寫的測試與 mutation gate → 2026-10 測試篇＋總論；evals from traces 與 judge 盲點 → 2026-10 可靠度篇與 2026-12 觀測篇；搞笑談軟工版主的可重現性、DDDesign Taiwan 那串「多 agent 抽 bounded context 每次數量不同」、spec 當輸入契約 → 2026-11；AGENTS.md 對 pass rate 不敏感 → 2026-11 總論 §五；OTel GenAI semconv、AIOps bot、flight recorder → 2026-12；harness pin／diff → 2026-12 可靠篇；K8s v1.37 sandbox fleet → 2026-12 一節，完整版在第 3 條；vendor outage／額度 → 2026-12 一句，完整版在第 6 條；skills 供應鏈資安 → 第 1 條；agentic commerce／WebMCP → 不列）。**本圈新增下面這些**，來源是 `selection.md` §1 的 12 月錨點表與 `conference_digest.md` §4 的十五個插入點：

| 訊號 | 去了哪裡 |
|---|---|
| MCP proxy 的單一結構化事件 schema，含 `fault_domain` 與 `exclude_from_error_rate`（`2QlDa` slide 35、19） | 2026-12 觀測篇主 schema；本條在 backlog 裡只剩「錯誤分類學」的一般論 |
| 日立參考實作的 who-vs-why 缺口、「orders were sometimes placed despite unmet terms or approvals」（`2QlEG` p.24） | 2026-12 總論 §三與應變篇；**同一頁的另一句已進 10 月可靠度篇 §一** |
| 103 個 session 的 23.5 turns、6/6 成品對 vs 5/6 session 成功、`rm -f events.jsonl -> blocked` 卻在道歉、semconv 連 denied vs failed 都表達不了（`2So56` slides 2/9/10/13/18） | 2026-12 總論 §五、觀測篇 §3；**slide 10 與 slide 13 另已進 10 月總論 §三與測試篇 §七** |
| harness 的定義、「we don't talk about agentic AI evaluations」、AAIF 269 家會員／14 sectors、新設 agents accountability WG（`2QsV2`、`2RaW6`、`2QsUJ`） | 2026-12 總論 §二 |
| Uber 每月約 9,000 份 RCA；heavy approval flows get skipped under stress（`2QlDI` slide 14、`2QlDv` slide 17） | 2026-12 總論 §三、§十；**`2QlDI` slide 14 另已進 10 月 Review 篇 §二** |
| 「A writable log can be altered or deleted」與五條對抗性驗收測試（`2VRYC`） | 2026-12 總論 §六、應變篇 §3；**剩下的付款那一半在第 11 條** |
| 書 ch.1 §1.2 Agent = Model + Harness 與 Verify 規則；ch.7 Exp 7-6 的 52 筆失敗裡 24 筆自稱完成被 verifier 否決；ch.10 §10.5 拜占庭故障 | 2026-12 總論 §五（全系列唯一帶書數字處）；**第 8 條引 ch.10 要換段落** |
| 書 ch.7 §7.2 Pass@k vs Pass^k（p=0.6、k=5 → 99.0% vs 7.8%）、§7.7 的 SE ≈ √(p(1−p)/n)；三次重試 1st 86%／2nd 99%（`2TjiE` slide 18） | 2026-11 的驗收指標與方法學警告 |
| 「same prompt, same model, same harness，兩次結果完全不同」（`2VPr7` slide 2）、五位講者各自的「縮小 decision surface」 | 2026-11；**全場沒有一位講者報過同一份規格的 run-to-run 分布，那是 11 月的第一手空位** |
| 十五個插入點裡的另外十筆（Quartic.ai 四態閘門與五題健康檢查、AAAI/ICLR 送審量、tool-call verifier、Frozen artifact、337/0 的 regex director、issue 裡的 `skip_tests=true`、Red Line Rate、Gen-AX 的模型選型） | 2026-10 四篇（已寫好，只加句不改行文）；**第 5、8 條引用時要換角度，不能重講同一句** |
| 「equal terminal outcomes do not imply equal containment」（2607.23999） | 2026-10 三部曲的收尾；第 1 條只能當前情提要 |
| 核准率 30.5% → 36.6% 的習慣化曲線（2609.06213 / 投影片引的 2606.22721） | 2026-10 Review 篇 §三一句；**完整設計留給第 9 條** |

## 訊號監看清單

每月 1 日 `collect.sh` 與 `prompts/arxiv.md` 的輸入。格式：看什麼 → 出現什麼算訊號 → 影響哪一條。1–15 沿用 2026-09；16–22 是本圈新增。

**X 帳號**

1. @unclebobmartin、@martinfowler（含轉發）— 測試／review／harness 的立場文 → 第 5 條、2026-10 的回響。
2. @trq212、@ClaudeDevs、@claudeai — Function Hooks（09-03 預覽、尚未出貨，回饋在 GitHub）、`plugin eval`、`/skill-doctor`、permission 與 compaction 的變更；**本窗口沒有任何 compaction 變更** → 第 1、4 條要重測數字。
3. @perplexity_ai、@Docker、@allenown（DEVCORE）— agent detection & response、agent identity；台灣資安圈第一篇 agent 事故分析 → 第 1、10 條。
4. @charlieholtz／@conductor_build、@mattyp、@K8sArchitect、@kubernetesio、@CloudNativeFdn — sandbox fleet、AI factory、v1.38 → 第 3 條。
5. @dexhorthy、@hwchase17／@Vtrivedy10、@ArtificialAnlys — SlopCodeBench、tuned evaluators → 2026-10 回響與第 8 條。
6. @minorun365、@TestingGolem、@jassttokyo／@JSTQB_PR — 日本企業導入與 QA 重心移動；JSTQB 秋季大會（2026-10-16）議程 → 第 5、14 條。
7. @OracleDevs、@himanshutwtxs（mem0）、@akshay_pachaar — memory as database、agent-native git → 第 3、4 條。

**LinkedIn**

8. Alolita S.（OTel GC）與 OTel GenAI SIG — semantic conventions 從 development 進 stable 的時點 → 2026-12 引用要更新；killer.sh 的 CNPE 課程與 Golden 路線圖 → 插曲排期。

**arXiv 查詢字串**（2026-09 的 9–13 全部保留，並修正兩條）

9. `"privilege escalation" AND (harness OR "coding agent")`（本窗口 0，改用擴展式 `"privilege escalation" AND harness`）、`skill AND ("supply chain" OR poisoning) AND agent`、`"reference monitor" AND agent` → 第 1 條。
10. `("technical debt" OR maintenance OR "code quality") AND "coding agent" AND (longitudinal OR "post-merge")`（本窗口 0）、`"architectural decision" AND agent AND memory`（本窗口 0）→ 第 2 條。**兩條都太窄，下圈改用擴展式並記錄命中數。**
11. ~~`(sandbox OR "agent runtime" OR "internal developer platform") AND Kubernetes AND agent`~~（連續 0，**作廢**）→ 改用 16 的新字串 → 第 3 條。
12. `(compaction OR "context window" OR "working memory") AND "coding agent"`（本窗口 0 / 擴展 1）、`"agent skills" AND (evaluation OR staleness OR provenance)`（13）→ 第 4 條。
13. `("exploratory testing" OR "computer-use agent" OR "GUI agent") AND (testing OR QA)`（0；擴展 1/3/4）→ 第 5 條；`"multi-agent" AND (topology OR coordination) AND "software engineering"`（1）→ 第 8 條；`("domain-driven design" OR "bounded context" OR "event storming") AND LLM`（0）→ 第 7 條；`(deskilling OR "skill atrophy") AND developers AND AI`（0）→ 第 9 條。

**arXiv 新字串**（`conference_digest.md` §9.5；每一條都附了動機的場次與它延伸的舊查詢）

16. `abs:"OpenTelemetry" AND abs:"GenAI" AND abs:"semantic conventions"`（`2So56` slide 18）→ 2026-12 與第 12 條。
17. `abs:"agent identity" AND (abs:"delegation" OR abs:"authorization")`、`abs:"delegated authorization" AND abs:"agent"`（`2QlEM`、`2SrLI`、`2RpxA`）→ **第 10 條**。
18. `abs:"transparency log" AND abs:"AI agent"`、`abs:"tamper-evident" AND abs:"agent"`（`2VRYC` 與阿姆斯特丹的 Agent Action Capsule）→ 2026-12 應變篇與第 1 條。
19. `abs:"agent payment" OR abs:"x402"`、`abs:"MCP server" AND (abs:"ecosystem" OR abs:"availability")`（`2QlDO` slides 6–7；**用前先把 arXiv:2608.00150 對回投影片數字**）→ **第 11 條**。
20. `abs:"coding agent" AND abs:"human review"`（習慣化那條線，`2QlDX` slide 16 引的 2606.22721）→ 第 9 條與 2026-10 回響。
21. `abs:"durable" AND abs:"sandbox" AND abs:"agent"`、`abs:"agent workspace" AND abs:"persistence"`（`2QlE7`、`2QlEe`）→ **第 3 條；這是 11 的修復，不是重複**。
22. `abs:"Model Context Protocol" AND abs:"task"`（`2RcMn` 的 Tasks 擴充）→ **第 12 條**；`abs:"agent" AND abs:"cost variance"`、`abs:"agent" AND abs:"token cost" AND abs:"same task"` → 第 6 條與 2026-11；`abs:"LLM-as-a-judge" AND (abs:"reproducibility" OR abs:"variance")` → 第 8 條與 2026-10 回響。

**Facebook 社團**（保留在 `FB_GROUPS`；括號內是該社團的有效指標）

14. Backend 台灣：分享數 ≥ 15 的事故／資安解剖 → 第 1、2 條（本圈最接近的是 217/12/15 的共用 library 那串）。搞笑談軟工：一輪通過 Gate 的模型表、地端 LLM 重試、去技能化、論文發表 → 第 6、9 條與 2026-11 回響。DDDesign Taiwan：**十月轉進 Discord**，Line／Telegram 關閉—監看要跟著搬，否則第 7 條會永遠空手。DevOps Taiwan：驗證閉環、SDD 是不是瀑布、棕地 meetup 後續 → 第 2、3 條。Scrum Community 與 Agile 內湖：測試專欄（3–17 反應）與 Sprint 45《與我的 AI 焦慮共處》（09-23）→ 2026-10 回響、第 9 條。Claude Taiwan：handoff／compact 門檻、plugin eval、分層派工與混用模型 → 第 4、6 條；**席位抱怨只當第 6 條的症狀計數器，不當主證據**。Twinkle AI：MCP Hub、vLLM 台北 meetup、主權模型 → 第 3、6 條。六個 vendor 社團（MCP、OpenClaw ×2、GCP & K8s、Cowork、Antigravity）本圈**再次全是詐騙與外語廣告**，只有三則與 agent 有關且已抽出—下圈若仍如此，從 `FB_GROUPS` 拿掉。

**會議與日期**（2026-09 的 15 保留；本圈把東京帶回來的日期全部併進來）

15. JSTQB 秋季大會 2026-10-16（→ 第 5 條）；STARWEST（→ 第 5 條）；KubeCon + CloudNativeCon NA 2026-11（→ 第 3 條、2026-12 引用）；Kubernetes v1.38 預計 2026-12（→ 第 3 條）；DDD Taiwan 年會（→ 第 7 條）；DevOpsDays Taipei 與 KCD Taipei（→ 第 3 條）；Twinkle AI／vLLM 台北 meetup 第二場（→ 第 6 條）；作者自己的 CNPE 第二次考試（→ 插曲排期與第 3 條）。

| 日期 | 是什麼 | 影響哪一條 |
|---|---|---|
| **2026-09-17/18** | **AGNTCon + MCPCon Europe，阿姆斯特丹**—帶著東京沒有的 EU AI Act／防篡改軌：Agent Action Capsule 與獨立 transparency log、「Governance You Can Run, Checkable Properties for Production Agents」、EU 法律下部署 agent 的責任 | 2026-12 應變篇（**動筆前要先收**）、第 1、10 條 |
| 2026-09-23 | Agile 內湖 Sprint 45《與我的 AI 焦慮共處》 | 第 9、2 條 |
| 2026-09-24 | 一位 KDDI 講者的新書（書名未印在投影片上） | 第 14 條 |
| 2026-10-15 | 投件 Open Source AI Week（10/16–25）的截止日 | 第 14 條、插曲排期 |
| **2026-10-22** | **Dex Horthy「There Is No Software Factory Without Better Verifiers」，聖荷西**—SlopCodeBench 的數字，連同受訪者自己的誤差棒但書 | 2026-10 回響、第 8 條 |
| 2026-10-22/23 | AGNTCon + MCPCon North America，聖荷西（推廣貼文的講者名單是折扣碼貼文，**不是議程**，用前要對官方議程） | 第 3、10、11 條 |
| **2026-11-17** | **WebMCP 的 Chrome origin trial（149–156）到期**，而「Mozilla: Neutral — No ETA」「WebKit: Opposed — No ETA」 | 自主瀏覽器那條小候選的**硬到期日**；沒有續期就刪掉 |
| 2026-12（初） | A2UI 可用性，「Hoping for early Dec」 | generative UI 當未測輸出類別的小候選 |
| 2026-12 | 《GraphRAG: The Definitive Guide》（O'Reilly） | 第 7 條的書錨候選（**是 GraphRAG 不是 DDD，別混用**） |
| 每年 6 月／1 月 | AAIF ambassador 招募窗口，日本申請者排程外審查 | 第 14 條 |
| 滾動 | AAIF Sandbox 的六個月檢查點與十二個月 Growth 窗口，每年公布 acceptances／graduations／archivals | 第 3 條 |

**標準與專案**（新增一組，全部是第 1、3、10、11、12 條的前提）

- OTel GenAI semantic conventions：trace 能不能記錄「執行前被拒絕」與「執行了但失敗」的差別（`2So56` slide 18 標「under discussion」，footer 註明 verified 2026-08-31）—**這是整份清單裡對 12 月最關鍵的一條**。
- MCP：SEP-1442／SEP-2322／SEP-2243、Tasks 擴充、`tools/list` 的 `"ttlMs": 300000` / `"cacheScope"`、Skills over MCP 與即將成立的 file-systems WG。
- 授權：Keycloak PR #46048（26.7 實驗性）／#49998，底下的 EMA 與 ID-JAG。
- 付款：HTTP 402 / x402 / USDC on Base、AP2。
- 瀏覽器：WebMCP 的 `document.modelContext.registerTool`、`readOnlyHint`、`toolautosubmit`。
- AAIF 工作組：authorization、agent payment、agent discovery、security（Security & Privacy 另有主席）、interoperability、observability、**agents accountability**（新設）、Governance Risk & Regulatory Alignment；Gilbert 自己點名的兩個缺口是 **memory 與 hardware**。
- 專案：Agent Router（repo 遷往 `github.com/theagentrouter/agent-router`）、agentgateway、`github.com/Hitachi/oss-assets` 的 workshop 實驗室、`agentcanvas`、`lean-agentic-ai`、`trust402`、`mem9`／`drive9`、`agentmemory`。**未經查證、不得引用**：某 deck 上列為 review 基礎設施的三個 vendor agent 名稱（`2WCMf` pp. 7、21）—引用前要先確認它們實際是什麼。

**值得追蹤的講者**（公開紀錄；本圈新增）：NTT DOCOMO BUSINESS 的 Kota Tsuyuzaki（@bloodeagle40234，OTel + MLflow trace 評估）、Anthropic MCP Connectivity 的 Camila Rondinini（flight-recorder schema）、日立的 Tatsuya Sato 與 Yoshiyuki Tabata／Michito Okai（MCP 授權／Keycloak）、KDDI 的 Minoru Onda（@minorun365）、Runlayer 的 Alexander Frazer（AAIF Security & Privacy WG 主席）、FRAME00 的 Aggre Hiroyuki（proofs vs logs）、Woven by Toyota 的 Juan Corena（唯一公布重試分布的人）、Red Hat 的 Marco Gonzalez（AAIF ambassador，keynote 段落最可靠的公開摘要者）。基金會帳號：@AgenticAIFdn、@Linux_Fdtn_JP、@mcpsummit、@LF_Europe。

**follow graph 的修補**（`x_digest.md` §8 結論）：目前追蹤清單裡**沒有任何標準組織的 maintainer、沒有 MCP／A2A／Envoy／OTel 的貢獻者、也沒有日本的會議記者**—Agent Router 改名、MCP keynote、以及東京這場本身（含兩個被追蹤帳號從會場發文）都只出現在另外抓的 `x_conf_search.json`，不在四個 feed 檔裡。下一圈前要補追：MCP 與 A2A 的規格編輯、Envoy AI Gateway 與 OTel GenAI SIG 的負責人、兩三位 JaSST／AGNTCon Japan 講者。

## 成效權重（每月底回填）

已知基準（`style_brief.md` reception 段）：2025 年中文長文完讀 27%、英文 8%；書評型 46–51%、方法清單型 9–24%、文化型 hook 會傳播但完讀 16%；views 超過 presentations 的週都是粉絲團分享的週。對 backlog 的含意：有書錨的條目（第 2 條 Beck／Meadows、第 5 條 Hendrickson、第 9 條）在 format 分項加分；純 build list 的條目（第 3、4 條）要找到歷史脊椎或書錨才提案—**第 3 條本圈拿到半條脊椎（agent 工作區＝儲存產品，RPO／RTO 的老詞彙套新工作單位），第 4 條仍缺**。

| 月份 | 主題 | 中文 views／reads／完讀 | 英文 views／reads | 粉絲團分享 | 對 backlog 的調整 |
|---|---|---|---|---|---|
| 2026-09 | Agentic Engineering 三部曲 | 43／15／35%（發布 11–14 天；09-08 潤稿重刊，篇幅 +2–4 分鐘） | 26／6（23%） | 否（粉絲團未貼；個人頁一則公開貼文 28 心情／3 分享，疑為系列宣傳，內文未抓到） | 組織篇在中英文都最多人點（zh 11 views；en 9 views／4 reads），技術篇最少（zh 3；en 6／1）；英文 3 篇十天 +16 views 追平中文 4 篇 +14，但完讀 23% vs 35%；總論仍佔中文 views 58%。方法型條目要帶「誰來做」的組織鉤子；純 build-list 條目（3、4）維持先找書錨 |
| 2026-10 | 綠燈不是驗收 | | | | |
| 2026-11 | 同一份規格，跑十次 | | | | |
| 2026-12 | Agent 的 SRE | | | | |

**2026-09 這一列與 09-05 的差距**（`community_digest.md` §4）：中文四篇從 **29／11（38%）** 到 **43／15（35%）**，十天 **+14 views／+4 reads**；英文從三篇 **7／2（29%）** 到四篇 **26／6（23%）**，可比的那三篇十天 **+30 presentations／+16 views／+4 reads**。月度區塊從 **171／39／13／+1 follower／0 subscriber** 到 **267／82／21／+2／+2**—presentations 漲約 56%，Medium 還在把英文版丟進推薦流。

三件對 backlog 有直接影響的事：

1. **中文會讀完，英文會被點開。** 分發靠 Medium 的是英文，靠作者人脈的是中文；完讀仍然是中文贏（35% vs 23%），比 2025 年的 27% vs 8% 收斂了但沒有翻轉。兩種都要寫，reads 從中文來。
2. **「誰來做」的標題比「藍圖」的標題跑得遠。** 組織篇在兩個語言都是最多人點，技術篇在兩個語言都最少—即使技術篇才是帶 build list 的那一篇。**這直接壓住第 3、4 條**：它們正是 build list 型，提案時必須帶組織鉤子或書錨。
3. **粉絲團仍然沒貼，而且看得出來。** 除了中文總論以外，九月每一篇的 views 都低於 presentations（系列合計 69 vs 226），正好是 2025 年被分享那幾週的反面（《與不確定性共舞》142 presentations／619 views）。粉絲團有 727 位追蹤者、2025 年那幾篇各被分享 18–22 次，而他們**還不知道這個系列存在**。digest 給的順序是：先把九月系列貼上粉絲團，再趁熱寫東京插曲。
