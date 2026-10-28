# Codex 校稿 — 2026-11-aaif-after-tokyo/article.md（第 2 輪）

> model: gpt-6.1-sol, reasoning: xhigh, 2026-10-29 00:17. 原話照錄，未經摘要。

我會先讀口吻規範與上一輪處置紀錄，再逐段核對中英文、圖說、表格和文末註記；只列本輪仍存在的問題，全程限於倉庫內唯讀檢查。
<!-- codex ran: /bin/zsh -lc pwd -->
<!-- codex ran: /bin/zsh -lc 'cat STYLE.md research/2026-09/voice_brief.md' -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-after-tokyo-zh-r1.md .context/research/aaif-2026-10-28-polish/2026-11-aaif-after-tokyo -->
<!-- codex ran: /bin/zsh -lc "wc -l 2026-11-aaif-after-tokyo/article.md 2026-11-aaif-after-tokyo/article.en.md; rg --files -g AGENTS.md -g '"'!agents/**'"' -g '"'!.claude/**'"' -->
<!-- codex ran: /bin/zsh -lc "sed -n '55,180p' research/2026-09/voice_brief.md" -->
<!-- codex ran: /bin/zsh -lc 'cat research/2026-10/aaif-agntcon/codex-polish-2026-11-aaif-after-tokyo-zh-r1.md' -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,110p' .context/research/aaif-2026-10-28-polish/2026-11-aaif-after-tokyo-zh-r1-disposition.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '1,47p' .context/research/aaif-2026-10-28-polish/2026-11-aaif-after-tokyo-zh-r1-disposition.md" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.en.md | sed -n '1,185p'" -->
上一輪採用的中文修正已核對，先前待同步的英文也有更新。我會接著檢查其餘中英差異；作者已說明不採用的「暫緩 rollout」分母建議，本輪不重提。
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.en.md | sed -n '94,114p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.en.md | sed -n '187,313p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.md | sed -n '94,211p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.en.md | sed -n '315,411p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.en.md | sed -n '412,533p'" -->
<!-- codex ran: /bin/zsh -lc "rg --files -g '"'!agents/**'"' -g '"'!.claude/**'"' -g '"'!.agents/**'"' -g '*article.md' -g '*article.en.md' 2026-10* 2026-11* 2026-12*" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.md | sed -n '212,312p'" -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.md | sed -n '314,410p'" -->
<!-- codex ran: /bin/zsh -lc "rg --files -g 'article.md' -g '"'!**/agents/**'"' -g '"'!**/.agents/**'"' -g '"'!**/.claude/**'"'" -->
已讀完兩版正文、圖說、表格與文末註記。目前剩下的疑點主要是少數句子的搭配、問句標點，以及中英對同一動作的表述；我會再核對跨篇節次，刪除純屬語感偏好的修改。
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.md | sed -n '411,532p'" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |規格修改卡|名額|接手.*成本|成本.*接手|G2|G3|frozen holdout|constraint tests|red-then-green|golden tasks|Org|champion|白名單|legibility'"' 2026-11-same -->
<!-- codex ran: /bin/zsh -lc "sed -n '299,367p' 2026-11-same-spec-variance/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## [一二三四五六七八九十]+、|Org|Repo|Dir|三級|legibility|golden tasks|白名單'"' 2026-10-agentic-harness-blueprint/article.md" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## [一二三四五六七八九十]+、|G2|G3|judge|委派|completion|人工投入|品質|champion'"' 2026-11-agentic-eval-economics/article.md 2026-09-agentic-org-design/art -->
<!-- codex ran: /bin/zsh -lc "nl -ba 2026-11-aaif-after-tokyo/article.md | sed -n '1,196p'" -->
<!-- codex ran: /bin/zsh -lc "rg -n '"'^## |G2|G3'"' 2026-11-agentic-eval-economics/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '508,532p' 2026-11-aaif-after-tokyo/article.md" -->
<!-- codex ran: /bin/zsh -lc "sed -n '57,120p' 2026-10-agentic-harness-blueprint/article.md" -->
<!-- codex ran: /bin/zsh -lc "python3 -B -c 'from pathlib import Path
import re
s=Path('\\''2026-11-aaif-after-tokyo/article.md'\\'').read_text()
print('\\''雙破折號：'\\'',s.count( -->
跨篇節次與主要數字已核對，未找到新的錯引；也未發現「——」、引號巢狀或全形括號的問題。最後清單會保留可直接替換的局部修正，並把僅涉及標點選擇的項目列為可選。
已核對上一輪 33 項處置、兩版全文及相關跨篇節次。以下只列本輪仍存在的 12 項問題；未修改檔案。

1. **［建議］§一〈一張邀請，和兩週內排好的東京行〉＋段首「這次 AAIF 陸續公開錄影」**  
   原文：「哪些是現場聽到、哪些是回台北補看，文末〈影片與資料的核對方法〉逐一交代。」  
   問題：文末交代了場次來源與核對方法，但「五場東京演講」並未逐一標明是否現場聽過，與此處承諾的資訊不完全相符。  
   建議改法：「八場材料的來源與核對方式，文末〈影片與資料的核對方法〉逐一交代。」英文對應句也宜同步調整。

2. **［建議］§四〈程式有編譯器，其他工作靠什麼回應錯誤？〉＋節標題（下接「Anthropic 的 David Soria Parra」）**  
   原文：「其他工作靠什麼回應錯誤？」  
   問題：「回應錯誤」容易理解成出錯後如何處置；本節實際問的是，其他工作如何取得指出錯誤的回饋。英文標題也是後者。  
   建議改法：「其他工作靠什麼指出錯誤？」

3. **［可選］§六〈請求失敗後，哪些事情可以安全重試？〉＋段首「Anthropic 的 Camila Rondinini」**  
   原文：「請求失敗之後，我們憑什麼知道外面有沒有改變。」  
   問題：冒號後已直接提出問題，改用問號可與本節標題及英文版一致。  
   建議改法：「請求失敗之後，我們憑什麼知道外面有沒有改變？」

4. **［建議］§七〈私有部署需要重新分配營運責任〉＋段首「共用同一套程式呼叫介面」**  
   原文：「同樣可靠地選工具、保留限制或產生可編譯的修改」  
   問題：「保留限制」較像保存限制文字，未清楚表達模型是否遵守限制；英文用的是 *honoring constraints*。  
   建議改法：「同樣可靠地選工具、遵守限制或產生可編譯的修改」

5. **［可選］§八〈哪些調查步驟應該固定，哪些需要模型判斷？〉＋段首「Uber 的 Kriti Dangi」**  
   原文：「一條線索要經過什麼，才變成值得交給工程師的工作。」  
   問題：冒號後直接提出本節問題，問號較能呈現提問語氣，也與英文版一致。  
   建議改法：「一條線索要經過什麼，才變成值得交給工程師的工作？」

6. **［建議］§八〈從線索走到修補，先建立有辨識力的重現〉＋段首「要往修補前進，就得」**  
   原文：「真的無法用程式重現，才動用模擬器。」  
   問題：「程式」與「模擬器」不是清楚的對立，模擬器裡也能執行程式；此處承接的是前面的單元、元件與整合測試。  
   建議改法：「真的無法用前述測試重現，才動用模擬器。」

7. **［可選］§九〈從生產錯誤找到真正該改的地方〉＋段首「Pydantic 的 Marcelo Trylesinski」**  
   原文：「上線之後發現沒做對，該改哪裡，又怎麼知道改對了。」  
   問題：冒號後連續提出兩個問題，句末用問號較清楚，亦與英文版一致。  
   建議改法：「上線之後發現沒做對，該改哪裡，又怎麼知道改對了？」

8. **［建議］§九〈把生產錯誤變成有明確預期的測試〉＋段首「事前準備的 eval 與生產」**  
   原文：「這兩個問題不同，卻都需要一個獨立的判準來源」  
   問題：「這兩個問題」分別指較前面的 judge 共享盲點，以及後面的 optimizer 改動判準；中間隔了數句分析，指涉需要回讀。  
   建議改法：「共享盲點與由 optimizer 改動判準是兩個不同的問題，卻都需要一個獨立的判準來源」

9. **［可選］§十〈一次次任務之外，長期要觀察什麼？〉＋段首「PagerDuty 的 Inês Bolaños」**  
   原文：「一次次任務累積之後，使用者與 agent 之間的摩擦出現在哪裡。」  
   問題：冒號後提出觀察問題，問號較能與前面的提問方式及英文版一致。  
   建議改法：「一次次任務累積之後，使用者與 agent 之間的摩擦出現在哪裡？」

10. **［建議］§十一〈我會帶回團隊的：三個決定，和一張會議用的表〉＋段首「第三個時刻，是維護者」**  
    原文：「比較的名額買不到人工接手的成本」  
    問題：「買不到成本」動賓搭配不成立；「名額」也沿用了被引用文章的比喻，本篇沒有先建立其意思。對照英文與變異篇，這裡要說的是比較次數不能代替人工成本的記錄。  
    建議改法：「執行比較的次數再多，也不能代替人工接手成本的記錄」

11. **［建議］§十二〈離開澀谷之後〉＋段首「所以我會從一個經常」**  
    原文：「一個經常發生、範圍明確的調查」  
    問題：「調查」是需要執行的工作，搭配「經常發生」略顯翻譯腔。  
    建議改法：「一項經常需要做、範圍明確的調查」

12. **［可選］§文末〈References〉＋引註 10「MCP — Skills overview」**  
    原文：「完整 manifest 與 dynamic 情況分開」  
    問題：正文一直使用「完整的檔案清單」，到引註才首次出現 manifest；補上對應名稱，可避免讀者以為是另一種材料。  
    建議改法：「完整檔案清單（manifest）與 dynamic 情況分開」

各類問題統計如下，每項依主要問題計一次；第 2、4 項雖參照英文判讀，列入用語可讀性，不另計中英差異。

| 類別 | 項數 |
|---|---:|
| 錯字、同音誤字、漏字、重複字 | 0 |
| 標點 | 4 |
| 斷句與可讀性 | 5 |
| 指涉與承接 | 1 |
| 用詞、術語一致 | 1 |
| 前後一致 | 1 |
| 中英實質意思差異 | 0 |
| **合計** | **12** |

嚴重程度：**必改 0 項、建議 7 項、可選 5 項**。未發現「——」、引號巢狀錯誤或全形括號不成對。

上一輪修正已落實，未發現新增的必改級錯誤或實質中英落差。餘項集中在局部搭配、指涉與問句標點，作者口吻及全文主軸已相當穩定。

<!-- tokens: in 1932956 out 15928 -->
