<!--
Medium 發布指南（此註解區塊不要貼進 Medium）

自動化：`./tools/medium_draft.sh <article-dir> en` 會建好草稿並比對內容，停在發布前一步。
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

# The Same Spec, Ten Runs, Part 1 — Specification: Decide What You Need Before Deciding How to Describe It

> **TL;DR** — "Make the input handling more robust" points in a direction, but it has not yet answered: should no message, whitespace-only text and a wrong type produce different results? This piece is written for document authors and Tech Leads, and it deals with the choices that come before writing one more paragraph. First recover the requirements that already exist; hand what is genuinely undecided to whoever has the authority to decide; then separate the normative requirements that must be followed from the rationale and examples that explain them, the pre-submission self-check, and the optional implementation suggestions. Along the way I take apart the four briefs of the formal study: A0 already contains the complete goal, A expands the explanation, B adds rationale and a self-check, and C adds one optional pattern. Some of their differences only change how things are explained; others change what is allowed. All forty programs passed the checks, and that still cannot rank the documents. By the end, you can use a concrete input to check whether a rewrite changed a requirement, write the self-check you want to add as a reviewable change card, and then decide which text serves only this one task and which needs long-term maintenance. The next round of comparison has not been run; the change card is a proposal, not proof that the effect holds.

> Series: [Overview](https://medium.com/p/3700b5d771fd) → **Part 1, Specification (this piece)** → Part 2, Contract (coming soon) → Part 3, Variance (coming soon). Chinese edition: [同一份規格，跑十次（一）：規格篇—先決定要什麼，再決定怎麼交代](https://medium.com/p/fc5ed5fce443).

## 1. What "make the input handling more robust" has not yet answered

The research task behind this series comes from my `medium-articles` repo. `research/scripts/codex_jsonl.py` reads the work records that Codex sends back. Those records use JSONL: each line is one JSON value; some lines carry review text, and some say the work is complete. The tool recognizes and handles each line as it arrives, which is why it is called a streaming parser.

It hands its result to the next program, the caller, through three channels: stdout carries the ordinary review content, stderr carries diagnostics, and the exit code at the end reports the outcome as a single number. Exit 0 means the tool believes this run produced a valid review; any other number sends the caller down a different failure path.

The study reproduced two problems in a fixed starting version of the parser, the seed commit. First, when the program received the valid JSON `[]` or `null`, it treated the value as an object and called `.get()` on it, so it crashed. Second, if a message's `text` was the number `123` and a valid completion event followed, the program printed `123` as review content and finished with exit 0. Before fixing either, someone has to say which inputs were always meant to be accepted and which ones are actually errors.

Suppose the task description were a single sentence: "Fix the type crashes and make the parser more robust." It sounds clear. Nobody objects to fixing a crash, and nobody wants a number treated as a review result. But the moment the implementer opens the program, they run into choices that this sentence has not made for anyone. The `text` field of an agent message alone has at least four values that need an answer first.

Let me fix the comparison scenario first: for each row, the input contains one agent message with the listed `text` value, followed by exactly one valid completion event; there are no other messages or malformed events, and no explicit failure. From here on I call a format error malformed, and I use contract for a chosen set of behaviors the program is required to follow. In the table, R05 stands for requirement 5 of the contract, so the spec and the checks can be compared side by side.

The exit code depends on the whole input, not on one field, so that trailing completion event is a necessary premise. Read the table across: first what the implementer has to answer, then what the caller would see under the other answer. The last row mentions strip, which means removing the whitespace at both ends of a string; in this case, that is not harmless tidying.

📌【在此插入表 table-01.png】

All four rows are choices; none of them can be derived from "more robust". The contract treats `false` as a format error so that a wrong type sent from upstream becomes visible; it keeps whitespace-only strings valid, and says in so many words that this is "for legacy compatibility", that is, to keep existing usage working. Another product might choose differently. In this repo, though, behavior that existing callers already depend on is a compatibility obligation, and a change of maintainer is no license to rewrite it.

There are choices beyond `text`. On a malformed line, stop or keep reading? Contract R03 chooses to keep reading. If one input contains both bad data and an explicit failure event, which should be reported at the end? R11 says that once EOF, the end-of-input signal, arrives, the checks run in order: an explicit failure reports 3; next comes 6 for a malformed event; then 4 when there is no valid completed turn; then 5 when the turn completed without an agent message; only when none of these applies is the result 0.

This is an order of precedence, unrelated to the size of the numbers. It works like a checklist consulted in order: once an earlier condition holds, the later ones no longer decide the final answer. Should duplicate messages be dropped? R13 says they are printed as before and each handled as a valid event. May the old end-of-stream summaries be made more readable while we are at it? R12 requires them to be kept word for word. These are all choices about externally visible behavior, not just about how the code is written.

These decisions affect the caller more directly than code style does. The expanded spec, A in section 3, says in R11 that "the nonzero exit tells the existing caller that it is not a valid completed review." So if a fix strips whitespace-only strings, or moves the malformed verdict behind "no agent message", the conclusion the caller receives changes, even if the program becomes tidier for it.

Kiro's bugfix spec documentation divides a fix into three parts: current behavior, expected behavior, and unchanged behavior ([Kiro Bugfix Specs](https://kiro.dev/docs/specs/bugfix-specs/)). For this parser, the third part is especially important: the existing diagnostics, the exit precedence and the handling of duplicate events are all behavior the fix has to preserve. The template itself guarantees no compatibility; acceptance still has to confirm it.

In his 2013 short essay "Why We Should Build Software Like We Build Houses", Leslie Lamport argues that programs, too, deserve a blueprint before construction. Writing a specification, he points out, forces you to say what the program should do before you change it; a specification also lets users of an interface know how to use it without reading the implementation ([Lamport, 2013](https://lamport.azurewebsites.net/pubs/wired.pdf), pp. 1–3). This is his engineering position, not a comparative trial; he also says that writing a specification does not guarantee a program is free of errors.

From those two points I distilled a question a document author can use directly (my inference, not his words): reading only this description and not the implementation, does the caller know which exit `text: false` will end with? If the answer is no, first check the existing normative requirements and compatibility obligations. The answer may have been decided long ago and simply left out of this description, in which case the traceable requirement should be restored; only if it genuinely has not been decided does it go to the requirements owner, who has the authority to decide and bears the consequences. Neither gap should be left to the implementer's guess, and the two must not be classified indiscriminately as undecided requirements.

In the previous series, [Green Is Not Done](https://medium.com/p/c4fc9f3d8581), I kept separating the artifact from the grounds that support accepting it. Back at this parser, there is one more thing to clarify before acceptance: which behaviors have been promised, and which are still only choices facing the implementer? [The Overview](https://medium.com/p/3700b5d771fd) of this series splits the judgment into three layers: whether the requirement has been decided, whether this program meets it, and whether this way of briefing is worth reusing. This piece calls a program awaiting acceptance a candidate; when we get to document changes, the recurring question will be "would a candidate permitted by the original wording still be permitted after the rewrite?"

The piece follows one document change from start to finish: first sort out what each sentence does, then compare four real documents, then write the problems found into a change card, and finally decide how the text is kept and maintained. All four documents in the formal study had their behavioral goals written out in advance, so the study did not measure the payoff of requirements exploration. What it can show us is what each brief added, and whether a rewrite smuggled in a change of scope that nobody intended.

## 2. Five kinds of sentence in one document: normative requirement, rationale, example, self-check and optional pattern

One passage of spec text can do several jobs at once, and the document author may not notice. Take the `text: false` case and lay it out as five sentences: "false must be reported as a format error" sets a requirement; "so that a wrong type from upstream becomes visible" explains the rationale; listing the `false` input with its required output is an example; "before handing in, confirm again that false is not skipped" is a self-check; "a small shared function could handle text" is an optional pattern. From here on I call such a small shared function a helper.

All five may be useful, but not all of them can be used to reject a submission. During review, first identify which job a sentence is doing; if it raises a behavioral choice that nobody has resolved, mark it separately as an undecided requirement. The point of classifying is to know who is affected when the sentence changes, and who confirms it.

One check makes the difference concrete: temporarily delete a sentence and see which programs move from qualified to disqualified, or the reverse. From here on, the legal set means all implementations the contract permits. If a sentence is the only basis for requiring duplicate messages to be kept, then after deleting it a program that drops duplicates may no longer be excluded; that sentence was carrying normative weight.

This is a clue in one direction only. No change after deletion does not mean the sentence had no normative role; the same requirement may be repeated elsewhere, so you still check its source and the status the document gives it. The same goes for examples: if the document designates an example as the sole acceptance answer, it carries normative weight too, and cannot be ignored because its heading says "example". In the table below, rationale, examples, self-checks and optional patterns refer only to text that explains or restates existing requirements without adding an obligation.

📌【在此插入表 table-02.png】

The table also works in reverse. If editing a passage of "rationale" turns a previously legal implementation illegal, that passage was already normative and should be handled as a requirement change: confirm the change with the affected callers and update the acceptance checks. The same holds for optional patterns. As soon as acceptance starts rejecting implementations that did not adopt a particular helper, that helper has been quietly promoted into a requirement.

The unit of classification is the sentence, not the whole document. Even A0, the most compact of the four briefs that section 3 introduces, keeps one sentence of rationale inside R05. A explains in R02 that text which cannot be decoded is still silently skipped, and adds that "this existing tolerance is intentionally retained"; in R07 it explains that an item error, the error of a single item, does not mark the whole run as failed, because "this preserves the old distinction between an item error and a failed turn". The sections that B and C append declare what they are in their opening lines: B says the section "adds no requirement and does not prescribe a class layout or helper names"; C says "any implementation meeting the same contract is acceptable".

Beyond the category, look at how strongly a sentence binds. Take "use a shared helper": "must use" excludes implementations without the helper; "may use" leaves the choice open; "should use, exceptions need a reason" is yet another requirement. Readers should not have to guess which of the three is meant.

RFC 2119 defines MUST, SHOULD and MAY for exactly this difference: MUST means required and MAY means optional; SHOULD may be set aside in particular circumstances for valid reasons, but only after the full implications are understood and weighed. Its §6 also warns against using these imperatives to impose practices unrelated to interoperability ([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html)). RFC 8174 adds that only the key words appearing in uppercase under this convention carry those definitions; a sentence that uses none of them can still be normative ([RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html), §2).

These documents belong to the context of IETF Internet standards, and not every repo document has to adopt them. What I borrow is the habit of writing the strength down: the absence of MUST does not mean something is optional, and "recommended" and "may" cannot be swapped at will.

The last decision is how precise the text needs to be. Lamport holds that descriptions can be written at different levels of precision: most simple things can be stated clearly in ordinary prose, and only the subtle or critical parts deserve a more rigorous method ([Lamport, 2013](https://lamport.azurewebsites.net/pubs/wired.pdf)). Applied to this parser, R05 has to separate types from empty values carefully, so it is worth enumerating value by value, even as a table. A requirement such as "keep the existing CLI entrypoint", the command-line interface that starts the program, can point at the existing interface in a short sentence without a formal description. More precision can also mean more maintenance, though: when a requirement changes, the rationale, examples, self-checks and optional patterns tied to it may all need checking together. That is what the classification is for: when something changes, you know which other sentences to check with it. Next, I apply the method to the four documents that were actually handed to the model, to see what "writing a bit more" added.

## 3. Four frozen briefs: A0 is not a blank control, and C is not a Skill

The formal study prepared four briefs. They share the same seed code and the same thirteen requirements, R01–R13, and their versions were fixed before generation; that is what this piece means by "frozen". Whoever cites the results later must be able to find the exact text used at the time; a document that has since been edited cannot be passed off as the version that was tested.

**The four English specs in full: [A0: compact](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A0.md), [A: expanded](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A.md), [B: A plus rationale and self-check](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/B.md), [C: B plus an optional implementation pattern](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/C.md).** These links point to the original text used in the experiment; the tables and excerpts below are only a reading guide.

To read and compare at the same time, open the [full-text and line-by-line diff guide](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/experiments/same-spec-ten-runs/SPECS.md). To find the differences, compare A0 with A requirement by requirement across R01–R13, then read the sections B and C each append; that is easier than rereading all four documents from the top. The guide also provides the three line-by-line diffs and the complete task input, seed code included. A0 and A also differ in one place over the scope of CLI options; section 5 explains it carefully, so do not start out treating them as two documents with the same meaning that differ only in length.

The table below sketches the shape of the four documents. The English word counts are whitespace-separated units and include headings and code blocks; they exclude the seed code, and they are not the token counts the model uses to process text. The fourth column maps what each adds onto the categories of the previous section; the pattern there is only text suggesting how to arrange the implementation, and an excerpt of the original follows shortly.

📌【在此插入表 table-03.png】

A0 is the easiest to misread. It has only 936 English words, but it is not a user story that merely sketches the job to be done, and it is not a blank control with no concrete requirements. Its opening says the task is to "fix valid-JSON wrong-type crashes and prevent non-text values from becoming a successful review"; it then states that "the requirements below are the complete contract", and that "this is a maintenance task; preserve the existing permissive stream behavior." R01–R13 are all there, and so are the fixed output strings; each requirement is simply compressed into one paragraph.

A opens with a paragraph of background: the repository uses this parser to turn Codex JSONL output into a review while keeping diagnostics separate. It also describes the two kinds of input that currently cause trouble, and adds that "evaluation adds no additional requirements." A then expands the requirements one by one: R04, R10 and R11 become tables, the fixed strings of R03 and R12 move into code blocks, and quite a few clauses gain a sentence or two of rationale. So A is not without rationale; its rationale is simply spread through the clauses. A also writes one more sentence of scope into R13; because of that sentence, A0 and A cannot be treated as semantically identical, which section 5 works through.

B begins with the full text of A, byte for byte, meaning every byte is preserved, and only then adds a section titled "Non-normative rationale and checklist": rationale and self-check that add no requirement. The consolidated rationale has two paragraphs. The first points out that successful JSON decoding only guarantees a JSON value; it does not guarantee that the value is the object you need, or that the fields inside it have the right types.

It also flags a Python trap, the old code's `if text:` check: it tests whether the value is judged true or false, not whether it meets the contract. That true-or-false judgment is called truthiness; `0`, `false`, an empty array and an empty object can all fall into the "false" branch, and that is no reason to treat them all as no message. The second paragraph of rationale reminds the reader to keep per-event validation separate from the final status of the run: one bad event should not erase what was already streamed out, nor keep a later explicit failure from being observed.

Then come the six self-check questions, which B says refer "only to the published contract". They are quoted below as B wrote them; as you read, first pick out what each one asks the implementer to go back and check. In question 3, bool is a boolean value, float a floating-point number, and the token values are the usage figures a completion event reports; even when a number looks plausible, its type still has to meet the requirement. In question 4, `str` means conversion to a string, and `turn.failed` is the event that explicitly declares the work has failed. The requirement numbers each question refers to are in parentheses:

1. (R01–R03) Does output arrive before EOF, and do malformed diagnostics use physical line numbers while ignored text remains silent?
2. (R04–R08) Are missing, null, empty and wrong-type values distinguished for each field according to its own rules?
3. (R08) Are bool, float and negative token values rejected before a token comment appears?
4. (R09–R10) Is top-level error's legacy str conversion retained, and can malformed turn.failed still produce exit 3?
5. (R11–R12) Does final precedence remain 3, then 6, then 4, then 5, then 0 with unchanged legacy summaries?
6. (R13) Do repeated messages/completions and unknown string types remain accepted without new sequence rules?

All six point back to the original clauses; none adds behavior. The sixth deserves a second look: it reminds the implementer not to add sequence checks or deduplication on their own initiative, which heads off a fix that grows stricter with every edit.

So B's change gathers the existing requirements into one place, so the implementer can check them one by one before submitting the candidate. C is the first to cross into something else: beyond reminding you what to check, it suggests how the program could be arranged.

C likewise begins with the full text of B, byte for byte, and then adds a "Non-normative implementation pattern", a suggestion for arranging the implementation that adds no requirement. It lives in the input text; it installs no capability in the model and runs nothing on its own, so the pattern here is not a native Claude Code Skill, plugin or hook that an agent can load and use. The formal study did not measure the effect of those execution mechanisms either.

C keeps R01–R13 and states that any implementation meeting the contract is acceptable. The pseudo-flow below is quoted from C's original plain text; it reads like a route sketch for the implementer, there to explain the order of processing, not a program that has to be copied verbatim:

```text
# Excerpt of C's optional pattern, quoted from the original plain text; not executable code
for physical_line_number, raw_line in stdin:
    strip and try JSON decoding
    validate root and the recognized event's relevant fields
    emit one malformed diagnostic if needed
    otherwise emit that event's legacy stdout/stderr
    retain explicit turn.failed even when its diagnostic fields are malformed
at EOF:
    choose 3 > 6 > 4 > 5 > 0 and the matching legacy summary
```

After the flow, C suggests "a helper for optional text" that "can distinguish absent/null/empty from wrong-type values"; it also warns specifically that "top-level error must retain its separate str conversion rather than sharing that stricter helper." C lists two equally acceptable arrangements as well: an event handler, the function that processes one event, "can return a small result describing stdout/stderr output" and the run's state, or the existing if-branches can be kept, "with local validation" in each branch.

The model generated ten candidates from each brief. Within each group, all ten runs received exactly the same frozen task packet, containing the brief, the shared task instructions and the seed code; generation used `claude-opus-5-5` at high effort, a fixed reasoning-effort setting; the model had no tools and could only deliver a single file in a single shot. Only after generation did a separate acceptance program, the grader, check the candidates. 102 cases compare the result after the full input has been sent, and 1 more streaming probe watches whether a message has already been emitted before EOF, 103 checks in all. All forty passed, and the operational conditions (no timeout, missing trace or tool violation) held as well.

That result still carries a great deal of uncertainty. Within each group, assuming the ten runs are independent, identically distributed and share one success probability, 10/10 gives an exact two-sided 95% Clopper–Pearson confidence interval of about 69.15% to 100%; that is the estimated range under the stated statistical method, not a guarantee that the next run succeeds. Ten out of ten is still not enough to rank the four documents (formal results in [RESULTS.md](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/experiments/same-spec-ten-runs/RESULTS.md); the derivation and its limits in section 6 of this series' [Overview](https://medium.com/p/3700b5d771fd)).

The design itself also limits which questions can be answered. Relative to A0, A adds expanded explanation, tables, rationale and one scope statement all at once; relative to A, B adds rationale and a self-check together. It is like changing two ingredients in a recipe at once: when the dish comes out different, the credit cannot go to just one of them. Comparing B with C could in principle estimate the effect of adding the pattern section as a whole, but it still cannot separate which suggestion inside it worked, let alone reveal the model's reasoning from the result. With all four groups passing, this round also provides insufficient evidence to establish a benefit from these additions.

So the sentence-by-sentence reading that follows answers only "what did each document change", and does not rank them. Keep the full-text links from the start of this section open, pick requirement R05 first, and see how the same thing is briefed in the four documents.

## 4. Comparing R05 sentence by sentence: the legal behavior is unchanged; what was added is reminders and a path

First, the R05 rule in full, since the next few sections keep coming back to it. For an agent message's `text`, a missing value, `null` and the empty string all "mean no message and produce nothing": nothing is printed and nothing counts as spoken. A nonempty string "is printed unchanged plus one newline, flushed", that is, the buffered output is pushed out immediately so the next program can read it now, and it "counts as a spoken agent message"; the message must not be stripped of its leading and trailing whitespace, and "whitespace-only strings remain valid". Every other provided non-string value is malformed, "including 0, false and empty arrays/objects".

Under R03, each malformed line emits one `[codex malformed event] line N: REASON` diagnostic, "where N is its physical line number and REASON is any nonempty single-line explanation", and reading then continues with the next line. That line produces no stdout, and counts as neither a spoken message nor a completion.

One input shows how the rules chain together. Line 1 is an agent message whose `text` is `false`; line 2 is a valid completion event. Line 1 is malformed, so one diagnostic is emitted and nothing counts as spoken; line 2 is valid, so the usage comment is printed and one completion is recorded. At EOF there is no explicit failure but there was a malformed event, so R11 gives exit 6; R12 says exit 6 carries no end-of-stream summary.

All four documents require the same of this input: B and C keep A's R05 word for word, and comparing A0's R05 with A's sentence by sentence, I found no difference that would make a candidate legal under one document and illegal under the other ([A, original text](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs/A.md)).

If the legal behavior is the same, where is the difference? The table below compares only the text that concerns R05. The second column quotes the original wording, condensed where needed; the third applies the categories of section 2. Look at the fourth column: none of the four rows changes the legal set; what changes is where, and in what form, the implementer is reminded. In the quotations, trim means removing whitespace, normalize means converting to some uniform representation, and CJK means Chinese, Japanese and Korean characters; those words are in the original to stop the implementer from tidying content that must be kept as is.

📌【在此插入表 table-04.png】

Reading from the top down, you can see the same trap handled three times. A points out inside the clause that Python's truth values can mislead; B expands that point into a paragraph of rationale, adds the history of the old code, and then uses self-check question 2 to make the implementer go back and distinguish the values; C offers a path that can encapsulate that distinction, and attaches the exception that the helper must not be applied to the top-level error. The three treatments belong to three kinds of content, and each has its own maintenance: the rationale has to be kept consistent with the implementation history, the self-check has to be updated when the clauses it points to change, and the helper suggestion must always carry its exception with it.

The table also makes a gap obvious: the four documents contain almost no examples that pair an input with its expected output. A's tables and fixed strings are still normative, and the `0` and `false` it lists are part of the rule itself. In other words, the four conditions do not differ in the "example" category at all. Whether adding input-output examples would help is a separate intervention that has not been tested.

This section has split one requirement into normative text, rationale, self-check and an optional path, but it has not answered which is more effective: all four groups scored 10/10, leaving insufficient evidence to attribute the success to any one passage. More importantly, R05 being aligned is no grounds for assuming the whole document is aligned. The seemingly small scope addition in the next section changes which candidates can be accepted.

## 5. Seemingly equivalent wording: how A0 and A differ on the scope of new CLI options

The R05 comparison showed that text can grow longer while the legal set stays the same. The other case exists too, and it is harder to notice: two sentences that seem to say the same thing, yet allow different things. There is one such place between A0 and A.

Start with a familiar command-line option: adding `--debug` when running a tool may ask for extra diagnostic output. A CLI option is a switch of that kind, passed in from the command line; the shell wrapper is the shell program outside the tool that launches it and reads its result. With those two roles clear, look at how the two documents bound the scope of the change.

A0's R01 says: "No new CLI arguments or external dependencies are required." A0's R13 says that "this task does not add a strict mode, reject duplicate terminals, or change the shell wrapper" (duplicate terminals are repeated terminal events, such as a second completion). A's R01 is almost the same as A0's: "No new arguments or dependencies are required, and the shell wrapper is outside this change." The difference comes in the last sentence of A's R13: "Rejecting duplicate terminals, suppressing duplicated text, enforcing terminal ordering, changing the shell wrapper **or adding CLI options** is outside this task" (emphasis mine).

Now work the difference through with a hypothetical candidate. Candidate X is an example for the derivation only, not any candidate from the formal study. It meets every other requirement of R01–R13 and additionally adds a `--debug` option that is off by default; when the option is not given, every output and exit code agrees with the contract. I deliberately do not use `--strict` as the example, because both documents already exclude a strict mode, and comparing on it would show no difference between them.

- Under A0: R01 only says new arguments are "not required", which is neutral on whether they may be added; and the out-of-scope items R13 lists do not include CLI options. No sentence in A0 directly excludes X. A reviewer who wants to reject it can only infer from "this is a maintenance task", a noticeably weaker textual basis.
- Under A: R13 explicitly lists adding CLI options as outside the task. X did something the task excludes, so the reviewer has explicit text for sending it back.

The same X is hard to reject on any clause under A0, yet there are grounds to reject it under A. So on the dimension "may a CLI option be added", the set A allows is narrower than A0's; that one sentence carries a scope decision. Neither sentence uses the uppercase key words of the RFC convention above. RFC 8174 explains that normative text need not use those words; so a reviewer can still send a candidate back on the strength of A's scope sentence, and the sentence does not lose its force for lack of a MUST NOT.

What effect this difference had is still unknown. The formal grader did not comprehensively check extra CLI options or the `main` interface, the interface that starts the program, so the existing pass results cannot say whether any candidate added an option. The archived candidates have not yet been comprehensively checked for this point in this round either; and even after such a check, what a candidate added could not by itself be attributed to this one sentence.

Three things are certain now. First, A0 and A cannot be claimed to be semantically identical in full; going from A0 to A, besides expanding the explanation and adding rationale, also changed a scope decision. Second, the frozen packets cannot be modified, so this difference has to stay in the record as it is. Third, removing the difference in the next round requires the owner to decide first: may an option that is off by default be added? After the owner decides, both texts and the acceptance checks are updated to reflect that decision, and only then are the candidates regenerated.

I would check other spec rewrites the same way: for every pair of sentences that look synonymous, try to find a candidate that is "legal under one side and illegal under the other". If one can be found, the two sentences are not equivalent, and the owner has to decide which side to adopt; if none can be found, that only means none was found this time, and does not prove equivalence. Semantic alignment can find differences; it cannot decide for the owner which side to take. The decision reached after alignment also needs an acceptance check, or the texts will agree while nobody checks the behavior.

## 6. Confirm the premises before diagnosing: a wrong exit code cannot tell you what the model was thinking

A hypothetical candidate just showed two specs allowing different scopes. Now a different question: the specs agree on the answer, but the program does not deliver it; can we say outright that the document was not clear enough? All forty formal candidates passed, so what follows is still a hypothetical faulty version, not a newly discovered formal failure. I use it to show how far the output lets you locate the problem, and where the guessing has to stop.

Suppose a candidate gets only the `text` branching wrong, while its handling of valid completion events and of EOF follows the contract. The branch below is of the same kind as the old code's truthiness test that B's rationale paragraph describes:

```python
# Hypothetical faulty version (teaching illustration; not one of the 40 formal candidates; not executed)
text = item.get("text")
if text:                    # the truthiness test is the only branch
    print(text, flush=True)
    spoke = True
# false, 0, [], {} are all silently skipped, just like null and ""
```

Feed it the two-line input from section 4:

```text
{"type":"item.completed","item":{"type":"agent_message","text":false}}
{"type":"turn.completed","usage":{"input_tokens":12,"output_tokens":3}}
```

The table compares what the contract requires with the observable results of this hypothetical candidate. Every result in it is derived from the contract; this hypothetical candidate was not executed. Compare row by row, and pay particular attention to the row where the two sides agree.

📌【在此插入表 table-05.png】

That stdout agrees on both sides is itself a warning: an acceptance check that inspects only stdout would pass this candidate. The real difference is in stderr and the exit code. To the caller, 5 and 6 are both nonzero and both mean "no valid review"; looking only at the success-or-failure branch, the behavior has not changed. But the diagnosis points the wrong way: upstream actually sent data of the wrong type, yet the candidate reports "completed, but the agent did not speak", and the location information for line 1 is gone. Whoever investigates may end up chasing a problem that does not exist. R05 lists `false` as malformed precisely to prevent this.

Next comes the easiest misstep: seeing exit 5 and inferring that the model "missed R05". That inference has no basis; there are at least three other possibilities. The generated code kept the old code's truthiness structure; the model wrote a helper that treats every false-like value as missing; or the model understood R05 and got something else wrong. Reading the code can locate the faulty path, but under tool-free, single-shot generation, no record exists that explains why the model wrote it that way. Even in a full session with tools, the execution trace can only show what actions the agent took; it still cannot show how it understood the requirement.

So if the document is to be changed because of this, the change can only be written as a hypothesis for now: "this reminder may reduce deliveries of this kind."

Generalizing the example, I put together the diagnosis table below. The table also covers another kind of error: the contract allows different explanatory wording, but the check insists on matching the reference program word for word. What needs fixing then is the basis for judgment, called the oracle; it can be an expected value, a reference behavior or a human judgment. Both the grader that runs the check and the oracle it uses can be wrong, so a red test alone does not make the candidate wrong.

The table is my design, not a research result. Confirm the premises in the second column before making the judgment in the third; the same "did not pass" may need completely different people to handle it. The positive and negative controls in the table are examples known to satisfy or to violate the contract; they first check whether the yardstick, the grader together with its oracle, can tell the two apart.

📌【在此插入表 table-06.png】

The table deliberately has no row for "the model is not smart enough". Every row points to work that can be done: ask the owner to decide, send the candidate back, fix the yardstick, align the sentences, or add the exception to the implementation suggestion. The REASON example in the third row comes from the actual contract: R03 requires only that REASON be nonempty and on a single line; an acceptance that compares it word for word with the reference implementation's wording would wrongly reject legal candidates.

As for operational problems such as timeouts, a missing trace or a violated tool restriction, those signals by themselves cannot tell whether a candidate meets the behavioral contract. If a checkable candidate exists, contract acceptance can be run separately, with the operational status kept in its own column; neither column may be used to cancel the other out, and the original slot, one scheduled generation attempt, is kept rather than replaced by a new run.

## 7. Exploration, text, executable feedback: three interventions, three actions

The value of the diagnosis table is that the next action has a reason. If nobody knows yet what to do with an empty value, find someone to decide; if the answer exists but is easy to misread, improve the explanation; if the agent can run checks itself, let it see its errors before delivering the candidate. In research, deliberately changing one condition and watching whether the result changes is called an intervention. Here, the three concrete actions above are the way to understand it; the table then shows which gap each one handles.

📌【在此插入表 table-07.png】

Spec exploration already has mature methods. When Matt Wynne introduced Example Mapping, he split the discussion into four kinds: the story, the work to be done; rules; concrete examples; and questions nobody in the room can answer. Examples are used to find out what a rule actually means; questions show whose knowledge or decision the team still lacks ([Wynne, 2015](https://cucumber.io/blog/bdd/example-mapping-introduction/)). The value table in section 1 is really a stack of question cards: is false no message or an error? Is whitespace kept? Only once those questions have answers can the requirements that follow exist.

Anthropic's official best practices for Claude Code also mention that, for a larger feature, you can let Claude interview you to surface edge cases and trade-offs, then keep the spec as a separate artifact ([Best practices for Claude Code](https://code.claude.com/docs/en/best-practices), Let Claude interview you). Both practices help a team lay out what has not been decided; the decision itself still belongs to the owner.

Whether a text intervention helps depends first on what it changes. One external study used 5 program-repair tasks from SWE-bench Verified, a single model, Kimi K3, with mini-swe-agent, a fixed sampling setting of temperature 1, and combined 12 spec styles with 3 effort levels, repeating each combination 15 times, for 2,700 records in the final data table. The analysis excludes the prompt that supplies the solution directly (the paper calls it the oracle prompt) and keeps 11 spec styles. That oracle prompt is a prompt condition that provides the answer; it is not the oracle of the previous section, the basis for judgment.

The bare user story, which gives only a rough task description, cost about 29.7% more than the full spec. That is a hierarchical model's estimate at a single price rate: the 90% Bayesian credible interval is +5.1% to +58.7%, and the 95% interval is −0.3% to +66.8%, which includes zero. The interval expresses the parameter uncertainty under that model and its prior assumptions; 29.7% cannot be lifted out as a fixed gap every team would get ([arXiv 2608.25399v1](https://arxiv.org/html/2608.25399v1), §4.1, Appendix C).

The study also records that the terser specs more often hit the original limit of 60 turns; after the limit was raised to 120, 112 records were rerun, and 108 of them completed successfully (Appendix A). So 2,700 is the final record count, not the total number of requests: the 112 reruns come on top of it. Nor should "completed successfully" be inflated into all of them passing the issue-resolution acceptance.

What that study varied was whether concrete information was provided, not simply whether the document was longer or shorter. In this round, A0 already contains the complete goal, so the bare-user-story result does not apply; and letting an agent work for more turns already changes the delivery conditions. Both limits demand that the change card state first exactly which one thing it intends to change.

The same text can also act differently in different environments. That environment is what harness means here: the working frame around the model, which tools it can use, when it stops, and which results come back to it. Imagine a self-check that says "run the tests before handing in"; a model without tools can only read that reminder, while a model with tools might actually run them and correct itself on the results. This is an example to explain the pathway, not an effect measured in this round.

"Prompt-Induced Waste in Coding Agents" offers a related study. It uses 24 coding tasks with definite acceptance conditions and 18 prompt variants; 9 main variants keep the goal, the acceptance conditions and the test command. The core analysis has 4,644 valid runs; for seven models whose provider-supplied reasoning text was available, 2,801 records were annotated with the condition labels masked, meaning the annotators did not know which prompt condition a record belonged to. The latter is a subset of the former, not extra runs, and it does not include the separately arranged study of harder tasks.

The researchers observed that content demanding specific reasoning or verification changes the reasoning and verification work actually invested; merely restating the original word for word did not reproduce the full effect (§3). The effect of adjusting effort also changes with harness policy (§6.1). The tasks are small, though, with a very high success ceiling, and they barely cover architecture-dependent tasks, so the findings cannot be carried straight to large changes ([arXiv 2608.01347v6](https://arxiv.org/html/2608.01347v6), §11–12). The hypothesis I draw from this stays limited: a self-check that demands a concrete verification action may change how the work is done; to observe that pathway, the text and the available tools have to enter the design together.

Text has a cost too. The official Claude Code guidance warns that when CLAUDE.md gets too long, important instructions can be drowned in noise, so you should watch whether a change actually changed behavior. The same document warns that a reviewer asked to find gaps will usually find some; fixing every comment as given leads easily to over-engineering. My practice is to treat only findings that violate correctness or a settled requirement as must-fix. A self-check written as an open-ended "find the problems" could produce a similar tendency (that is an inference); B's sixth question gives the opposite reminder: do not add sequence rules. All of the above is vendor practice guidance, with no effect size from a controlled experiment.

When Birgitta Böckeler tried several spec-driven development tools in September 2025, she recorded small fixes generating large amounts of documentation, readers having to review more Markdown, and the agent not fully following the spec ([Böckeler, 2025](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)). These are one author's small set of trial experiences, not an average causal effect.

This round also recorded generation cost: by the CLI's list-price estimate, the ten runs of A0, A, B and C came to about USD 1.25, 1.38, 1.51 and 1.55 per group. That is not an actual bill, and it excludes human cost; the reading, review and maintenance time that really needs measuring was not measured this round.

Executable feedback takes a different route. The official Claude Code guidance has a section called Give Claude a way to verify its work: with executable checks, the agent can see the results and correct itself. The model in the formal study had no tools and delivered in a single shot; the self-check could only be read during generation, and the model could not actually run any test. In a session with tools, the same self-check might prompt the agent to run the public checks a few more times. If that pathway appears, it should be recorded. Where before the agent could only read the text, now it can also run the checks and get their feedback; the pathway is different. A no-tools study therefore cannot vouch directly for a with-tools workflow.

Tools also offer different entry points, so a team need not treat every gap as full feature development. According to the GitHub Spec Kit README as accessed on 2026-09-28, spec-driven development (SDD) first handles what to build and why, then moves to how to implement it; bug fixes and idea assessment have optional extension entry points ([Spec Kit README](https://github.com/github/spec-kit), version not pinned). The Kiro documentation consulted in the same research pass likewise distinguishes requirements-first, design-first, bugfix and quick-spec paths ([Kiro Specs](https://kiro.dev/docs/specs/)).

For the document author this means: if all that is missing is an empty-value policy, hand that question to the owner first; there is no need to generate a whole set of documents for the sake of a complete process. Böckeler's small trial predates those documentation versions and cannot be used to judge the tools at those versions; and a tool offering a path does not mean the model necessarily follows it, or that the product decision has been made on the team's behalf. Choose the entry point from the gap; do not reason backward from the name of an entry point to work that has been done.

Taken together, my judgment is this: before writing one more paragraph, use the diagnosis table to confirm which kind of gap it is. If the behavior has not been decided, explore and find the owner. If compliance with a requirement can be checked mechanically, consider writing that check first; that may be more direct than another paragraph, but this is an inference, and this round did not compare the two. If you want to add optional text on the grounds of "improving delivery", do it after the requirement is settled, state a hypothesis about which observable action it might affect, and submit it for review with the change card of the next section. Recording the necessary behavior and compatibility requirements is the document's responsibility in any case, and need not wait for that comparison of benefits. The sources and limits of the methods involved are collected in [Spec and contract foundations research](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/spec-foundations-research.md).

## 8. The spec change card: turning "just add the six self-check questions" into a reviewable change

The spec change card is written for a Tech Lead to review. It turns "add one more paragraph" into a change, and states its scope, expected effect, counterexamples and withdrawal conditions. Below, I fill one in with the parser as the background. First, what this card is: R05 is a real, archived requirement; the faulty version on the card comes from the hypothetical candidate in section 6 and did not appear among the 40 formal candidates; and the comparison the card proposes has not been run. The full card and a blank template are in the attached [spec change card](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/spec-change-card.md).

The card in one sentence: P is the original expanded spec, Q is the same spec plus the six self-check questions, and the question is whether that addition is worth it. It is laid out in YAML so a reviewer can check the reason, the change, the acceptance and the responsibilities field by field; it is not a configuration file that can be run.

```yaml
# Spec change card (design example, comparison not yet run; the faulty version is hypothetical, not a result from the 40 formal candidates)
decision: Demonstrate on this parser first whether six self-check questions should follow the expanded spec; cross-task versions are built separately under a fixed rewrite policy
existing_requirements: R05 (wrong-type false-like values are malformed), R03 (one diagnostic per line, then continue), R11 (EOF precedence)
symptom: Hypothetically, a candidate uses `if text:` as its only branch and silently skips text=false
diagnosis: When the reproduction matches, a settled requirement was not implemented; why the model wrote it that way cannot be known
change:
  P: the expanded spec
  Q: P plus the original text of B's six self-check questions; without B's two paragraphs of consolidated rationale, and without C's pattern
held_constant: existing requirements, rationale, examples, optional patterns, seed, tool permissions, budget, stop conditions and acceptance version
expected_effect: fewer deliveries that fail the shared contract; the six questions as a whole are the unit of comparison, with no attribution to any single question
acceptance_signals:
  malformed_case: false followed by a valid completion → no message output, one malformed diagnostic, exit 6, no end summary
  legal_cases: null and "" produce no agent-message output; " " is printed unchanged and counts as an agent message
compat_risk: if the checklist is shortened to "text is always strict", it may wrongly change R09's str conversion of the top-level error
free_choices: function names, dict or class state, whether to extract a helper
owners: spec owner (confirms the checklist adds no requirement), QA owner (positive and negative controls), the reviewer taking over (records effort); no real people assigned yet
adoption_evidence: the difference in qualifying deliveries (submissions that meet the comparison's acceptance conditions set in advance) within the scope set in advance, failures per requirement, and the cost and human effort of every attempt
disposition: keep / withdraw / modify / still undecided, with evidence version, reasons, owner and re-review conditions
```

The first point of review is whether "symptom" and "diagnosis" are kept apart. The symptom is a reproducible observation: a minimal input, a candidate version, and the actual stdout, stderr and exit code. The diagnosis goes only as far as "a settled requirement was not implemented". The card deliberately does not say "the model missed R05", for the reasons given in section 6. Only when the two fields are written separately will later changes state hypotheses about visible behavior, instead of pretending to fix what the model thinks.

The second point of review is that only one thing changes this time. B in the original study added consolidated rationale and the self-check together, so even if B had done better, there would be no way to know which part did the work. This card adds only the six self-check questions, exactly as B wrote them, to P, without B's two paragraphs of rationale and without C's pattern; R01–R13 remain the complete contract. Apart from the six questions, every other condition of P and Q has to be the same, including the existing rationale, examples and optional patterns, and the seed, tool permissions, budget and stop conditions. The two complete packets still have to be built and archived. Anyone who wants to know whether "adding only one paragraph of rationale explaining truthiness" helps has to write another card and build another pair of P and Q. Both interventions may help, both cost reading and maintenance, and each should be judged on its own evidence.

Crossing to other tasks also requires freezing the [self-check rewrite policy](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/self-check-transfer-policy.md) first. The parser's six questions include EOF, token and error-event requirements, and cannot be pasted onto CSV or any other tool. For instance, when a CSV tool is only required to hand over a complete file, the parser question "must a message be readable before EOF" cannot be carried over. Each self-check question may only point back to a requirement that task's P already contains; the six checklist positions are rewritten under rules fixed in advance, a position with no corresponding obligation is marked not applicable, and no question is added just to fill six. Undecided policies go to the owner first, and Q is built only after they have been added to the shared P. The rewriter may use only P and the seed-repo information visible under both conditions, not the hidden grader, the reference fix, or the results of the formal tasks to tune Q; otherwise, even without adding a requirement, Q might merely be handed clues to the answer.

Each task's P and Q are diffed and archived, and repeats of the same task under the same condition use identical text. What is then compared is the overall effect of the rewrite policy, and the work of mapping the self-check to each task's requirements, with its review and maintenance, counts as cost. The mapping across all tasks and the input documents are not finished yet, so this card cannot be taken straight as an executable cross-task plan.

The third point of review is whether the expected effect can be observed. The hypothesis is that the six self-check questions will reduce deliveries that fail the shared contract, and the comparison evaluates the checklist as a whole. `false` being skipped is only the example used to show the reasoning; it is not the checklist's sole target of observation. Take question 2 to see how a self-check connects back to the clause.

Question 2 asks: are missing, null, empty and wrong-type values distinguished for each field according to its own rules? On reading it, the implementer should go back to R05 and separate the values that are easily confused: `null` and the empty string mean no message; `false`, although also false-like, is malformed; a whitespace-only string is a valid message. This step only rechecks behavior already decided; it adds no rule.

Then check the code: if `if text:` is the only branch, `false` is skipped along with `null`, and the question has found something to fix. Then confirm three results with the `acceptance_signals` input: stdout has no output representing `false`, stderr has one malformed diagnostic pointing to line 1, and the exit is 6. A fix can also overshoot, so the positive controls are checked at the same time: if after the fix `null` is rejected too, or whitespace-only strings are stripped, the requirement question 2 points to is violated just the same.

This check has one boundary: the model answering "compliant" after its self-check is not evidence of compliance. The self-check is only a reminder; the evidence has to come from external acceptance. The checklist also covers more than R05; even if errors of the `false` kind decrease, that does not establish that question 2 changed where the model paid attention. The comparison records the overall qualifying deliveries, and separately records the failures per requirement, to confirm that the other requirements did not get worse.

The fourth point of review is compatibility risk. The checklist's fourth question explicitly asks that R09's str conversion of the top-level error be retained; that is an exception the contract keeps on purpose. Whether the top-level error's message is a number, a bool or a container, it is converted to a string as before and does not count as malformed. The risk appears when the checklist is retold: if someone shortens it to "check all text strictly", the implementer may apply the strict helper to R09. That is a hypothetical wording risk, and this round did not observe that failure; but it shows why a self-check list cannot be summarized casually, and why the exception has to be kept with the list.

The fifth point of review is legitimate implementation freedom. Function names, whether state lives in a dict or a class, whether a helper is extracted: none of these becomes a requirement because a self-check was added. External acceptance must accept the different arrangements the contract allows; otherwise the P/Q result may only reflect which group looks more like some template, not which group better meets the contract.

The sixth point of review is owners and adoption evidence. The spec owner confirms the checklist adds no requirement in disguise; the QA owner confirms acceptance can tell the known faulty versions apart and also lets legitimate exceptions through; the reviewer who takes over records the time spent understanding, fixing and reviewing each candidate. This example card has no real people assigned yet. The evidence needed for adoption is a comparison of qualifying deliveries within the target task scope chosen in advance, a separate list of failures per requirement, and a record of the model cost, human handling and document maintenance of every attempt. The practical threshold, sample size and stop conditions should be decided by the actual owners before they see the results.

A filled-in card is not yet a green light to start comparing. Before building P and Q, confirm that acceptance rejects the faulty version under study while accepting legal implementations; after building the packets, check that this parser's two packets differ only by the original six self-check questions; for other tasks, check their self-check sections against the approved policy, keep the complete inputs, and compute version fingerprints (hashes), so that text edited later cannot be mixed with the original results. If a pilot, a trial run of the process on a few tasks, finds a problem in the requirements or expected values themselves, fix it first and create a new version. Once the formal comparison starts, every slot is kept under the rules set in advance; the checklist is not edited, no runs are added and no samples are picked after seeing a disappointing result.

The next round's design also differs from the formal study: it plans a bounded session in which tools can be used. The agent may run the public checks within the session and correct itself; external acceptance happens only after the session ends, and no replacement session is opened. How a task, each scheduled run and a session are counted, and how human observation is arranged, is left to Part 3, Variance; the full proposal and comparison plan are in the attached [document change evaluation proposal](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/document-change-proposal.md) and [comparison plan example](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/comparison-plan-example.md).

The change card writes down the commitment of the comparison first; only once the real results are in does the final disposition field get its turn. Even if Q's pass rate is higher, look at the uncertainty of the gap, whether it is enough to support clearing the practical threshold set in advance, and whether the added human effort and cost are acceptable. If both groups still pass everything, one sentence from Anthropic's article on eval practice is worth keeping in mind: "An eval at 100% tracks regressions but provides no signal for improvement." ([Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), Step 7).

An all-pass result can be kept as a regression asset, to recheck with when something changes later, but it cannot say whether the six self-check questions worked or not; at that point, go back and judge what is missing: the yardstick's discriminating power, the representativeness of the tasks, or the precision the sample size allows. So the card's disposition has four options: keep, withdraw, modify, or still undecided. Each records the evidence version, the reasons, the owner, and the conditions under which it must be reviewed again.

If the team cannot run a comparison yet, it can still, under the rewrite policy, attach a self-check matching each task's requirements to a small number of jobs as a limited trial that keeps the existing human approval in place, writing down the scope, owner, stop conditions and review date. That yields observations from real work, but it cannot be used to claim the effect has been established.

## 9. Switching to a CSV export: how the same card is used

The change card has now said why to change, exactly where, and what to judge by; the next thing to confirm is whether it stays useful away from the parser. Here I switch to CSV, a text table whose fields are separated by commas; one record, for instance, holds a name, a date and a note in that order. This is a hypothetical requirement, not an existing feature of the repo, and no new model generation was done. The series did actually replay three ways of judging on fixed data, but it did not verify a complete date-conversion feature; this section first looks at how a document author handles an undecided policy. The teaching program and its results are in the [CSV replay record](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/workbench/csv-transfer.md).

Suppose a CSV export tool is to gain date-column formatting, and the callers have already required that the input row order and duplicate rows be preserved. Of the three records, the first has the name `王,小明`, a name that itself contains a comma, a null date, and a note containing a line break; the next two are both `李`, dated 2026-09-28, with an empty note, and are identical in content. Under the existing requirements, `王,小明` must come first, and both `李` rows must be kept. What the team has not decided is the empty-date policy, and it also has to confirm whether null, the empty string and a missing field should be distinguished.

The document author first separates the settled requirements from the open questions. The draft below covers only what that distinction needs; it is not a complete date-conversion spec:

```markdown
<!-- One-off spec draft for a hypothetical task; never handed to a model; not a complete implementation spec for the feature -->
## Requirements
- On export, preserve the relative order of input rows and keep duplicate rows; do not sort, do not deduplicate.

## Examples
- 王,小明 first, then the two identical 李 rows → still three rows out, in the original order.

## Open questions
- Should a null date produce an empty field or be rejected? Does the same policy apply to the empty string and to a missing field?
  - Who answers: the requirements owner of the export feature
  - Impact: acceptance expected values that depend on this policy stay unsettled
  - If a provisional assumption is needed, limit it to prototype exploration, record it separately, and keep it out of formal acceptance

## Rationale
- To be supplied. If downstream really does match rows to the source in original order and treats duplicate rows as distinct records, write that down.
- Do not write an unconfirmed use as fact.

## Optional pattern
- A helper for the date representation may be extracted; it must not sort, deduplicate, or decide the open policy on its own.
```

The most important part of this draft is the "Open questions" section. It hands the unanswered question to someone who can answer it; an agent can raise questions from it too. Without that record, some implementation might pick one representation on its own, and a test would then freeze it as the only answer. The rationale section is left blank deliberately for the same reason: an invented use would lead the next person to believe it had been verified.

One format premise first, so the third case below reads easily. In CSV, one complete row of data is a record and the column titles are the header; the end of a record can be marked by different line-break characters, the two common ones being LF and CRLF. If the requirement allows both, rejecting a file only because its characters differ may mean the check is too strict. Now use the diagnosis table from section 6 to handle three cases separately:

- **The candidate sorted the data rows.** The spec has an explicit answer, so the candidate is sent back. The sorted output shows that it broke the contract; it does not show why the model did it. To reduce deliveries of this kind with a self-check, the intervention "does the output preserve each row's relative order and number of occurrences?" can be proposed; its benefit still has to be measured separately.
- **The candidate filled a null date with a fixed string, or rejected the input.** First check the existing interface and compatibility requirements. If there really is no answer, this is an undecided requirement and goes back to the owner; it cannot be ruled a violation merely because it does not match the reviewer's preference, and the candidate's choice cannot be written straight in as the only expected value.
- **Acceptance wrongly rejected LF output.** If the owner has confirmed that each record may end with LF or CRLF, QA should fix the oracle that accepts only the CRLF template, record its version, and re-score the affected candidates consistently. The settled requirement does not need to change with it, and there is no need to compare the documents' length first.

Continuing the hypothetical scenario from the Overview, the owner decides that a null date produces an empty field, and confirms the fixed header `name,date,note`, unchanged row order and number of occurrences, and commas and line breaks inside fields kept as they are. The document author then records the null-date decision as a requirement and derives the example for the first record from it. If the empty string and the missing field are still undecided, those questions stay recorded separately; they cannot be generalized automatically from this one null example. If a prototype assumption or a test depends on the old choice, check the impact and update it; the downstream reason the owner supplies is recorded together with the decision.

At this point the document can support the next step: QA updates the oracle to match the approved output obligations and re-scores the candidates; the owner resolves the remaining date-policy questions. The CSV fixed-data replay demonstrates the former piece of work; it does not mean the complete date feature has been accepted, nor that the self-check has proven effective.

Finally, the parser's R01 requires that output be readable before stdin ends; that is the parser's streaming obligation. A CSV tool that only promises to hand over a complete file cannot copy that requirement. In the cross-task self-check template, the corresponding checklist position is marked not applicable under the rules set in advance. What carries over is the method of checking requirements; the concrete obligations still come back to each tool's own callers.

## 10. How document authors and Tech Leads divide the work: standing guidance, one-off specs and continuously maintained specs

The previous section handed the null question to the owner and wrote the answer back into the requirements once it was settled. The next question: how long does that decision stay, and who will still see it when something changes later? A reminder that serves only this fix and a behavior that must hold on every call cannot rely on the same maintenance arrangement.

Böckeler uses three names to distinguish a spec's lifecycle. **spec-first** means writing the spec before the code for this piece of work; for example, listing the behaviors this CSV fix will change. **spec-anchored** means the spec is maintained along with later changes; for example, the empty-date policy keeps one current description across versions. **spec-as-source** goes further and treats the spec as the primary source of editing, with the code derived from it; having written a spec first is no grounds for claiming to use this mode. She also separates the spec for a single task from the background documents that span tasks ([Böckeler, 2025](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)).

Tool documentation shows a similar separation of scope. The Claude Code documentation describes several things separately: keeping standing guidance in CLAUDE.md, writing a separate spec to record the decisions from an interview, and pairing them with executable checks and an adversarial review ([Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)). Spec Kit separates the project-wide constitution from a single feature's requirements, plan and task steps ([Spec Kit README](https://github.com/github/spec-kit)). On that basis I maintain the following three kinds of text separately; this is my arrangement, not a classification these sources jointly prescribe.

The table sets out what each of the three documents mainly keeps, which mix-ups to avoid, and who is responsible for reviewing it. The third column lists placements that easily confuse scope and responsibility; it does not forbid every cross-category reference. This is a suggested division of maintenance, not a rule that a kind of content may exist only in one file.

📌【在此插入表 table-08.png】

Take the parser. "Whitespace-only strings remain valid as before" belongs in the continuously maintained spec, because it is compatibility behavior that callers depend on and it must hold for the next fix as well. "No CLI options are added this time" belongs in the one-off spec; it only describes the scope of this change. As for a cross-task self-check, if the comparison supports adopting it, the rewrite policy can go into the standing guidance or a task template, and the self-check is then built from each task's P; that is exactly the question the card in section 8 is meant to answer. If the choice made for one fix is written straight into the standing guidance, it quietly constrains every later piece of work, which is the situation I most want to avoid (my inference, not Böckeler's claim). Whether spec-as-source suits an existing repo is a separate question; spec-first being useful on a single task does not mean the whole repo should switch to deriving code from specs.

When a document is handed over, the open questions and the exceptions go with it. Here is how I suggest handling them, not yet tried out in a team:

- **Mark open questions separately from the approved contract.** A one-off spec can keep its questions, and a continuously maintained spec can have a pending section or link to an issue. Each question records its impact, owner, provisional assumption and review date; exploratory assumptions and their tests are marked separately, and do not pose as accepted promises. The boundary depends on approval status and scope, not on the file name.
- **Write a requirement's exception next to that requirement.** Right after R03 says a malformed event has no other semantic effect, it states that `turn.failed` still records explicit failure; R05 says in the same paragraph that whitespace-only strings remain valid. Once an exception is separated from its rule, it is easily lost in retelling. An exception that is easy to miss can also go into the self-check, which is what B's fourth question does.
- **An optional pattern's exception travels with the pattern.** When C suggests the text helper, it warns in the same paragraph that the top-level error must not share it. When the pattern is copied elsewhere, the exception goes along.
- **A team-level exception keeps its reason and its approver.** Under RFC 2119's definition of SHOULD, a recommendation may be set aside for valid reasons, but only after the implications are understood and weighed. I would require the reason, the approver and the scope to be recorded, with a time set for re-review.
- **When standing guidance conflicts with a one-off spec, stop and ask the owner to confirm.** For example, the standing guidance says "strictly type-check every text field", while the one-off spec requires R09 to keep its str conversion. Within the scope the settled compatibility requirement covers, the compatibility requirement prevails. The conflict also means the standing guidance needs a narrower scope, and its owner should make that change; the implementer must not pick a side on their own.

When a passage enters the standing guidance, record who is responsible for reviewing whether it should remain. In "[Agentic Engineering, Part 2 — The Harness Blueprint: Making Your System Legible to Agents](https://medium.com/p/3facc281f633)" I made two suggestions: before changing an agent's background information and instructions, name the concrete outcome you want to improve; after the change, rerun a representative fixed set of tasks (golden tasks).

Applied here, every passage of standing text should record four things: which requirement it serves, which observable error it aims to reduce, who its owner is, and the date of its next review. A revision of the requirements, acceptance starting to cover a certain faulty version, a change of model or harness, or a conflict with a task's requirements all trigger a review.

Triggering a review is not the same as withdrawing, though. When acceptance starts to cover a faulty version, it can catch the error, but the candidate may still have to be redone, and a self-check might reduce exactly that rework. The owner confirms whether the passage is merely a duplicate, whether it still has an effect, and whether removing it would leave an acceptable number of failures and an acceptable workload for whoever takes over. Only when it conflicts with a requirement, the comparison has ruled out an improvement worth the investment, or the human effort exceeds the limit set in advance is it withdrawn or narrowed, for the corresponding reason.

With that, the division of work is clear. The document author classifies sentences, finds an owner for each open question, and keeps exceptions next to their rules. The Tech Lead reviews the change card, decides which kind of document a passage belongs in, and what expiry condition to attach. The requirements owner makes the decisions; the QA owner brings acceptance into line with them; the repo or platform owner manages the total volume of standing guidance and its conflicts. No role has to do all the work at once, but every passage of text must lead to someone responsible.

## 11. Closing: record why a sentence should stay, and when it should be withdrawn

Back to the opening sentence, "make the parser more robust". It points in a direction, but it is not yet a complete answer about behavior; some answers have to be restored from the existing contract, and only some need a fresh decision from the owner. How should the parser handle `text` when it is null, false, or whitespace only? After a malformed line, keep reading or not? In what order is the exit code decided? Someone always answers these questions in the end. The difference is whether the requirements and interface owners answer them and write the answers down, or some implementation quietly makes the choice in code and a test then freezes it as the baseline.

When you next ask "should I write one more paragraph?", my advice is to confirm first what that paragraph does. If it is filling in a decision, hand it to the owner; if it explains a decision already made, confirm that it does not change the legal set in disguise; if it is a self-check or an optional pattern, use a change card to write down which error it aims to reduce, what the unit of comparison is, who is responsible, and under what conditions it is withdrawn.

The frozen documents let us see, sentence by sentence, how a brief accumulates around a shared goal; the CLI-scope sentence between A0 and A also reminds us that a rewrite that looks like mere polish can change the scope. All 40 formal candidates passed, but that result cannot rank the documents; the P-versus-Q comparison has not been run; CSV is a hypothetical requirement paired with a fixed-data replay, with no new model comparison and no acceptance of a complete date feature. Those limits decide the next step: fix the explicit gaps first, then design a comparison for the optional text intervention, and do not infer an effect from the current all-pass result.

What I most want document authors to leave behind is a checkable reason attached to every passage of text. The sentence in R05, "whitespace-only strings remain valid for legacy compatibility", is a good example: it explains why the rule is kept, and it implies the condition for withdrawing it. The day the callers that depend on whitespace-only messages retire, the interface owner knows to go back and review this requirement, treat the change as a requirement change, and handle it together with acceptance, so it will not be deleted in passing during some refactor. The six self-check questions should carry an equally clear reason: they exist to reduce deliveries that fail the shared contract. If the comparison planned in advance supports them and the human effort required is acceptable, keep them; if they conflict with a requirement, the comparison has ruled out an improvement worth the investment, or the human cost exceeds the limit, withdraw them.

By this point, the document author can hand over two things: a spec that states the required behavior and the legitimate freedom clearly, and a change card that explains what the added text is for. The next person to take over still has to answer: "given a program, how do I know it meets the requirements?" Part 2, Contract, starts there: it turns requirements into observable results, and then checks whether the basis for judgment would let a faulty version through or wrongly reject a legitimate one.

> **Before writing one more paragraph, confirm which choice it settles and for whom; and as you write it, write down when it should be withdrawn.**

### Series

This series, The Same Spec, Ten Runs:

- [The Same Spec, Ten Runs: What Justifies Making an Instruction a Team Default?](https://medium.com/p/3700b5d771fd)
- **Part 1, Specification (this piece)**: The Same Spec, Ten Runs, Part 1 — Specification: Decide What You Need Before Deciding How to Describe It
- The Same Spec, Ten Runs, Part 2 — Contract: The Judgments Still Missing Between a Requirement and an Acceptance Check (coming soon)
- The Same Spec, Ten Runs, Part 3 — Variance: All Ten Passed, So Where Does the Next Piece of Evidence Come From? (coming soon)

The previous series, Green Is Not Done: [Overview](https://medium.com/p/c4fc9f3d8581), [Testing](https://medium.com/p/51d001a6dcd5), [Review](https://medium.com/p/4d36d0f2f9c1), [Reliability](https://medium.com/p/4b6d147bff0d), [Payment Walkthrough](https://medium.com/p/20452944263b).

Agentic Engineering, Part 2 (published): [The Harness Blueprint: Making Your System Legible to Agents](https://medium.com/p/3facc281f633).

### References

1. Leslie Lamport — [Why We Should Build Software Like We Build Houses](https://lamport.azurewebsites.net/pubs/wired.pdf), author's archived version, dated 2013-01-24, PDF pp. 1–3. The publisher's version was not checked for this piece; version notes in the [author's bibliography](https://lamport.azurewebsites.net/pubs/pubs.html#wired). [§1, §2]
2. Kiro — [Bugfix Specs](https://kiro.dev/docs/specs/bugfix-specs/), page marked as updated 2026-08-04, accessed 2026-09-28; see the three parts current / expected / unchanged behavior. [§1]
3. Scott Bradner — [RFC 2119: Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119.html), 1997-03; see §§1–6, especially the definition of SHOULD and §6. [§2, §10]
4. Barry Leiba — [RFC 8174: Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://www.rfc-editor.org/rfc/rfc8174.html), 2017-05; see §2. [§2, §5]
5. Matt Wynne, Cucumber — [Introducing Example Mapping](https://cucumber.io/blog/bdd/example-mapping-introduction/), 2015-12-08; see How it works and Known unknowns. [§7]
6. Anthropic — [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices), living official documentation, captured 2026-09-28; see Give Claude a way to verify its work, Let Claude interview you, Write an effective CLAUDE.md and Add an adversarial review step. [§7, §10]
7. arXiv 2608.25399v1 — [Can your AI agent be cheaper?](https://arxiv.org/html/2608.25399v1); see §4.1, Appendix A and Appendix C. [§7]
8. arXiv 2608.01347v6 — [Prompt-Induced Waste in Coding Agents](https://arxiv.org/html/2608.01347v6); see §3, §6.1 and §11–12. [§7]
9. Birgitta Böckeler, martinfowler.com — [Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html), 2025-10-15; see spec-first / spec-anchored / spec-as-source, the distinction between task specs and standing background, and the author's trial observations from September 2025. [§7, §10]
10. GitHub — [Spec Kit README](https://github.com/github/spec-kit), living document, accessed 2026-09-28, commit not pinned; see the SDD, bugfix and idea assessment entry points, and the constitution and feature-spec steps. [§7, §10]
11. Kiro — [Specs overview](https://kiro.dev/docs/specs/), page marked as updated 2026-08-27, accessed 2026-09-28; see the requirements-first, design-first, bugfix and quick spec paths. [§7]
12. Anthropic — [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), 2026-01-09; see Capability vs. regression evals and Step 7. [§8]
13. Kochi Chuang — [The Harness Blueprint: Making Your System Legible to Agents](https://medium.com/p/3facc281f633), Agentic Engineering, Part 2. [§10]
14. Research attachments for this series (all links point to a pinned version of the public repo): [the four frozen specs](https://github.com/fantasybz/medium-articles/tree/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source/specs) [§§3–5]; [formal results](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/experiments/same-spec-ten-runs/RESULTS.md) [§3]; [spec change card](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/spec-change-card.md) [§8, §9]; [document change evaluation proposal](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/document-change-proposal.md) and [comparison plan example](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/comparison-plan-example.md) [§8]; [spec and contract foundations research](https://github.com/fantasybz/medium-articles/blob/774759192ab0e0b2da3d8b163eb3f07f3d12f4c3/research/2026-10/same-spec-ten-runs/rebuild-2026-09-28/spec-foundations-research.md) [§7].

### AI collaboration note

- The 40 candidates of the formal study were generated by `claude-opus-5-5` at high effort, CLI 2.1.282, with no tools, in single-shot generation. The study was designed and run in collaboration with AI agents; I set the direction and read the design and the reports. AI collaboration does not mean that an outside party has independently reproduced the results.
- The Chinese manuscript was written by Claude Code (Opus 5.5, max effort) and then polished paragraph by paragraph and fact-checked by a Codex lead agent. Writing the manuscript at max effort is a different process from the formal study's high-effort generation.
- The spec change card, the hypothetical faulty version and its derivation in section 6, the hypothetical CSV case, and the meta-level teaching work of writing, reviewing and re-scoring after the fact are not counted in the formal study's 40 generation slots and 103 checks, nor in the four groups' combined generation cost estimate of about USD 5.69. The P/Q comparison planned in this piece has not been run.
- The record of the manuscript's main writing, agent review, paragraph-by-paragraph polish and language checks is in [STATUS.md](https://github.com/fantasybz/medium-articles/blob/main/research/2026-10/same-spec-ten-runs/manuscripts/STATUS.md).
- This English edition was written by Claude Code (max effort) from the final Chinese text, then polished paragraph by paragraph and fact-checked by a Claude lead agent, and reviewed by a separate Claude reader agent and in three Codex review rounds against the Chinese and the frozen study; the English-edition section of the same STATUS.md records the writer settings, each review round and the final checks.

*Kochi Chuang (莊軻齊) | Medium @fantasybz. Chinese edition: [中文版](https://medium.com/p/fc5ed5fce443).*
