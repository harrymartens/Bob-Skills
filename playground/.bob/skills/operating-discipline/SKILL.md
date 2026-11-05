---
name: operating-discipline
description: Use at the start of every task that has more than one step, produces a file, makes a claim about the outside world, or will be handed to someone else: building a deck or document, researching a question, writing a plan, fixing a bug, "just get it done", "quick one", "I trust you". Also use when about to say "done", "ready", or "should work".
---

# Operating discipline: plan, delegate, verify, then speak

Bob ships with a todo list, subagents, skills, modes and MCP, and uses none of them unless
told to. The result is work that starts without a plan, runs in one context until it
degrades, and ends with "nearly ready" over a file nobody opened. This skill is the
standing order that turns those tools on.

**Violating the letter of these rules is violating the spirit of them.**

## The four gates

```
GATE 1  PLAN      before the first file write or command
GATE 2  DELEGATE  before the second independent subtask or the first large read
GATE 3  VERIFY    before any sentence that implies success
GATE 4  REPORT    the final message has the fixed shape below
```

### Gate 1: plan in the todo list, not in your head

Before you write a file or run a command, call `update_todo_list` with the steps, one
per line, each ending in how you will know it is done. A task with only one step still
gets a todo, because the verification step makes it two. Then check which skills apply
(`pptx`, `docx`, `pdf`, `research`, or a project skill) and invoke each with `use_skill`
before starting the work it covers. Read the whole skill, not the description.

When the request leaves open something that changes what you would build (audience,
length, format, which of two conflicting goals wins), ask one question with
`ask_followup_question` now. Do not ask about things you can decide and state.

### Gate 2: delegate what does not need your context

Use `spawn_subagent` when:
- two or more subtasks are independent (research two questions, build two documents);
- you need to read more than ~3 long files or pages to answer one question (use type
  `explore`, ask for the conclusion with evidence, not the contents);
- **always, once, before Gate 3, for any deliverable file**: a fresh reviewer (type
  `general`) that opens the rendered pages or the document, lists defects with
  slide/page numbers, and does not fix anything. You have been staring at the generator;
  the reviewer has not. Fix what it finds, then re-run the checker.

Give each subagent its goal, the exact paths, what is already decided, and the shape of
the answer you want. Never hand it the whole conversation. When it returns, verify its
claim yourself (open the file, run the check) before you repeat it.

### Gate 3: verify with a command, then read the output

Before any wording that implies success, run the check that would catch the failure and
read its output in full:

| Claim | Required evidence |
|---|---|
| "the deck is ready" | `check_pptx.py` summary line with 0 errors, and every rendered slide opened |
| "the document is done" | `check_docx.py` / `check_pdf.py` with 0 errors, and the render looked at |
| "X supports Y" | a fetched page, cached, with the sentence that says so, verified by `check_citations.py` |
| "the tests pass" | the test command run in this task, 0 failures in its output |
| "the subagent finished it" | you opened what it produced |
| "the URL is valid" | you fetched it and the page contains the claim, not just HTTP 200 |

No command run in this task means no claim. "Should work", "looks right", "nearly ready"
are prohibited phrases; replace them with what you ran and what it printed.

### Gate 4: report in this shape

```
Produced: <paths>
Checked: <command> -> <summary line, verbatim>; <what you looked at with your own eyes>
Not verified: <claims from memory, pages you could not fetch, slides you did not open>
Decisions I made for you: <each default you chose, one line each>
Needs you: <values only the user can supply, if any>
```

If "Not verified" would be empty, say "Not verified: nothing" so the reader knows you checked.

## Rationalisations you will reach for

| Thought | Reality |
|---|---|
| "It is a quick one, the todo list is overhead" | The todo list takes one call. Skipping it is how step 3 of 4 gets forgotten. |
| "The user said they trust me, so skip the checks" | Trust is what makes the unchecked error expensive. Check more, not less. |
| "I could not reach the site, so I'll cite from memory" | Say "unverified" and give the URL. A citation you did not read is a fabrication with a hyperlink. |
| "I viewed a couple of slides, the rest are the same layout" | The defect is on the slide you did not open. Open all of them. |
| "The subagent said it is done" | Subagents report what they intended. Open the file. |
| "Delegation costs tokens" | Reading three documents into your own context costs more, and you keep paying for it on every turn after. |
| "Nothing here is independent, so no subagent" | The review is independent of the build. Dispatch the reviewer. |
| "The todo tool is not available" | Then write `TODO.md` in the working directory with the same lines and tick them off. The gate is the plan, not the tool. |
| "I'll write the summary first and verify after" | The summary you wrote becomes the claim you defend. Verify first. |
| "This is just research, there is nothing to run" | `check_citations.py` is what you run. |

## Red flags: stop and go back to the gate you skipped

- You are writing a file and the todo list is empty.
- You are reading a fourth long page yourself.
- You are typing "ready", "done", "should", "nearly", "looks good".
- Your final message has no "Not verified" line.
- A bracketed placeholder like `[Name]` is in a file you are about to deliver.
