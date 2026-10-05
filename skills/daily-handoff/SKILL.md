---
name: daily-handoff
description: "Use when working with a project's daily issue: opening it for the day, recording work into it as the day goes, handing the session over when the context runs out, closing the day, or restoring context in a fresh session from the last handoff. Match on intent in any language, not on these words: start the daily, today's daily, plan for the day, update the daily, log this into the daily, hand over, pass the session, running out of context, close the day, wrap the day up, fixate everything, resume, pick up where we left off, what happened yesterday. Same intents in Russian: заведи дейлик, обнови дейлик, передай сессию, сдай смену, подними контекст."
---

# Daily: open, keep, pass, close, resume

The daily is not a report. It is a **handoff point**, and its main reader is the
next session: it opens the issue and reconstructs the day — what was done, where
it lives, what to continue from. Management skims it rarely.

**The daily is alive.** It can be opened any time — morning with a plan, midday,
evening — and is edited all day: statuses change, comments accumulate, sections
appear for whatever happened. One closing act at day's end does not describe it.

Hence five actions:

| | When | What it does |
|---|---|---|
| **open** | start of day | creates the issue: plan, carry-over from yesterday |
| **update** | during the day | edits the body, appends comments |
| **pass** | session runs out | fixates and writes a handoff; the day continues |
| **close** | end of day | the same plus brings the daily to its final form |
| **resume** | new session | reads the last handoff, walks the addresses |

Boundaries: *update* fixates nothing and writes no handoff — it is just a record
of what is happening. *Pass* and *close* differ in scope, not in kind: after the
first the day continues, after the second the day need not be remembered.

## Language: the package is English, the output is the user's

These instructions are English to keep the context cheap. **What a human reads is
written in that human's language.**

- the daily body and comments — the language of the daily repository, matching
  the surrounding issues and that repo's own template;
- what you say in the terminal — the user's language;
- markers, attribute names and status keywords — always as written here.

Do not translate an existing daily, and do not switch the language of a day
already in progress.

## Step 0 — read the live state before writing anything

**Every action starts by reading the daily as it is now.** Not from memory, not
from what an earlier step in this same conversation reported. Sessions run in
parallel and the issue changes under you.

```bash
# 1. the daily for today, in this contour, for this project
gh issue list -R "$REPO" --label "<Project>" \
  --search "<YYYY-MM-DD> in:title" --state all --json number,title,state

# 2. its body and comments
gh issue view <N> -R "$REPO" --json body,comments
```

From that single read, establish:

| | Why it matters |
|---|---|
| does a daily for today exist | *open* must not create a second one |
| **is there more than one** | duplicates happen — see below |
| which sessions already wrote | decides your own session name |
| is the day already closed (`kind="day"`) | decides what *close* does |
| what the shared sections say now | your edit must not revert someone else's |

Re-read immediately before a write that depends on what you just checked. The
gap between reading and writing is where a lost update lives.

## Duplicate dailies

Two issues for the same (date, project) do happen — two sessions open one in the
same minute, or a create is retried.

**Keep the one with the work in it**: comments, a filled body, a later edit. The
other is an empty twin.

Report both, say which you would keep, and act after confirmation:

```bash
gh issue close <dup> -R "$REPO" --reason "not planned" \
  --comment "Duplicate of #<survivor>; the day is recorded there."
```

If both have content, do not merge them yourself — say so and ask.

## Session names

The unit of markup is the **session**: not the project, not the agent, not the
model. Two terminals on one project in one day are two sessions even when one
person runs both.

### Default name

```
main-<agent>        main-claude · main-codex · main-gemini
```

`<agent>` is the kind of assistant you are. Take `main-*` when, by step 0, **no
other session has written in today's daily**.

### When you are not alone

Someone else already wrote → `main-*` is not yours to take. Use a **scope** name:

```
<scope>-<agent>     panel-claude · orders-codex · launch-audit-claude
```

The scope is the area this session works in, not a single task: a session that
fixes one bug and then reviews around it is still one scope. Pick it from what
you are actually doing; if that is not clear, ask the user once and reuse the
answer for the rest of the day.

**Names, never ordinals.** "The second session" counts from whoever is speaking;
for the other session the second one is somebody else. Such records cannot be
matched and `resume` cannot filter them.

## Markers

The body — one block per session, for that session's write-ups:

```markdown
<!-- ephemeris:begin session="panel-claude" -->
## 🛠 panel-claude — what this session worked through
<!-- ephemeris:end session="panel-claude" -->
```

**You edit your own block only.** Not when updating, not when closing the day —
even if you see an error in another block; you write about the error in yours.
No block yet — create it at the end of the body, before the shared trailing
sections.

Comments — marker on the first line:

```
<!-- ephemeris:devlog session="panel-claude" -->
<!-- ephemeris:handoff session="panel-claude" -->
<!-- ephemeris:handoff session="panel-claude" kind="day" -->
```

`resume` looks for `ephemeris:handoff` and finds both handoff kinds. `kind="day"`
exists only to answer "is the day already closed?". Comments with no session
name still resolve — those are days that had a single session.

## Shared sections are not wrapped in markers

Stage, done, phase goals and blockers stay common to the day. Ownership is
written **into the status line itself**:

```
B14.1  P0: re-booking releases the hold   🔒 race, panel-claude's area
B14.3  P1: price skips the check          📋 orders-codex's area
B1     Bug 1: invisible characters        🔄 led by panel-claude
B1.3   Line in retry.py                   ✅ dropped — panel-claude did it better
```

**The owner is always named.** "Mine", "ours", "the second one", "she" do not
appear in shared sections: everyone reads them, and those words mean different
things depending on who is reading. Your own item carries your own name.

In the blockers section a session stands as a counterparty, like a person:

```
- **panel-claude** — fixes for the two review blockers. Running review when done
```

In shared sections edit only your own lines and those you are closing by your own
work. You do not rewrite another session's line.

## Contours

Dailies live in **separate repositories per contour**. Work and personal do not
mix: different owners, different readers, different sensitivity. Separation by
address, not by a label inside one repo — otherwise a work detail lands in the
personal feed one day, or the other way round.

The addresses live **outside this package**:

```
~/.config/ephemeris/daily.conf

default = work

[work]
repo     = <owner>/<repo>
assignee = <login>

[personal]
repo     = <owner>/<repo>
```

File or contour missing — ask and offer to create it. Default nothing.

**`assignee` goes to `gh` as a bare login, without `@`.** In `gh --assignee` the
`@` is reserved for special values (`@me`, `@copilot`), and `@login` is rejected
as unknown. A config holding `@login` — strip the `@` and carry on without
asking. The special values themselves pass through unchanged.

### Choosing the contour

**Named explicitly** ("personal daily", "work", a command argument) — take what
was named.

**Not named** — derive from the project: which contour has a label for it. Label
sets do not overlap between contours, so the answer is usually unambiguous.

```bash
gh label list -R "$REPO" --limit 100 --json name --jq '[.[].name]|join(", ")'
```

Exactly one contour matches — work there. Both or neither — **ask**. Do not
guess: the wrong contour means a work detail in the personal repo or a personal
one in the organisation's, and you will not notice soon.

### Contour conventions differ

`assignee` may be absent, labels may use a different case, the required sections
may differ. Carry nothing across — read the template of the repo you write into.

## The body template lives in the daily repo, not here

The canonical template is the `README.md` of that contour's repository. **Read it
before writing a body** — it changes as the reporting changes, and a copy kept
here would fall behind in silence.

```bash
gh api "repos/$REPO/readme" --jq .content | base64 -d
```

From there: required and optional sections, the icons, the formatting rules, the
register the text is written in.

**The template is a frame, not a form.** Required sections are required; but the
day also dictates its own — a breakdown of a failure, of a piece of work — under
its own icon and heading. That is better than an even list of identical items.

## Open the daily

**1. Step 0.** Exists for today → do not create a second one; move to *update*.
More than one → handle the duplicate first.

**2. Take the project's previous daily** and carry over what outlives a day:

- `🎯 phase goals` — in full, with statuses. **Numbering runs through and is never
  reused**: a closed `E1.11` keeps its number forever, otherwise "see E1.11" leads
  somewhere else a month later;
- blockers and waits — with who holds them and since when;
- do not erase yesterday's closed items, mark them closed: they show where you
  nearly built something unnecessary.

Mark new items as new — the list visibly grew by five, it was not "always like
that".

**3. Build the body:** stage, the day's plan in order, carried-over goals and
waits. `✅ Done` is empty in the morning, as it should be.

**4. Show the title and body before creating.** Create after confirmation:

```bash
gh issue create -R "$REPO" --title "<YYYY-MM-DD> — <Project>" \
  --label "<Project>" --assignee "<login>" --body-file <file>
```

## Update the daily

During the day, any number of times. Fixates nothing, writes no handoff.

- **body** — surgically: statuses in `🎯`, stage, waits. Do not rebuild existing
  write-ups, extend them: the live wording there is easy to lose in a rewrite.
  Your own write-ups go in your session's block; other blocks stay untouched;
- **comments** — devlog: detail, commands, output, `file:line`, diffs, in the
  technical register. First line is the `ephemeris:devlog` marker;
- a new task gets a new number, never a reused one.

Do not record as done what has no commit and no check behind it. That is a plan,
and it belongs in the plan.

## Pass the session

When the context runs out and the day continues.

**1. Fixate what is unsaved** — commit, push, worktrees out of `/tmp`, writes to
memory, archive and local docs. The report is written after, not instead.

**2. Write the handoff comment.** Same form as below, with two differences:

- heading says it is a session handoff, not the day's;
- **keep it short.** It travels back into a small context window — the very thing
  it exists to save. Write-ups are not copied, they get an address.

**The body is not brought to its final form.** Statuses in `🎯` change only where
they changed; the stage stays the day's; no summaries. The day is still running.

## Close the day

**Closing works like opening: the first one does it, the rest add to it.** No one
is appointed, exactly as no one is appointed to open the daily.

From step 0 you already know whether a `kind="day"` comment exists for today.
**Re-read the comments immediately before writing** — in the interval another
session may have closed the day.

**It does not exist — you are closing the day.** The order below is mandatory.

**It exists — the day is already closed by another session.** Do not rebuild the
shared sections, do not re-apply the label, do not run the weekly sweep: that is
done. Add **your own** handoff as a separate comment below, in the ordinary pass
form, and say in its first line who closed the day and in which comment. Do not
edit their comment.

### The order

**1. Fixate first.** Commit the uncommitted, push the branches, move worktrees
out of `/tmp`, either finish what was started or name it unfinished. Everything
going to memory, archive or local docs is written **now**, before the report.

**2. Bring the daily to its final form.** The same as *update*, but for the whole
day: stage, `✅ Done`, goal statuses, waits, the day's write-ups in your block.
Detail goes into a dump comment. Other sessions' blocks are not rewritten.

**3. Now the handoff comment**, carrying `kind="day"`. A separate comment, not
inside the dump.

If the day had session handoffs, **collect them as addresses, not as a retelling**:
list them with their addresses and say what is in each. Rewriting their content
would create a second version of the day that drifts from the first.

```markdown
**Sessions today.** three handoffs:
- morning, importer skeleton — #issuecomment-5175291319
- midday, the front-page failure — #issuecomment-5177450597
- evening, panel translations — #issuecomment-5179364121
```

**4. Verify the write landed once.** Re-read the comments and confirm there is
exactly **one** `kind="day"` for today. More than one — say so plainly; a double
post is the failure mode this step exists to catch.

**5. Apply `ready-to-close`.** The label means one thing: the day is handed over
and the daily may be closed at the next sweep.

```bash
gh issue edit <N> -R "$REPO" --add-label ready-to-close
```

Label missing in this contour — create it with the same meaning rather than
inventing your own name:

```bash
gh label create ready-to-close -R "$REPO" \
  --description "Daily handed over, ready to close at the weekly sweep"
```

*Pass* does **not** apply the label — the session ended, the day did not.

## The weekly sweep

Dailies pile up open because closing them mid-week serves nothing — they may
still be needed. The sensible moment is when the week changes.

**When to check.** On closing the day, compare the ISO week of today with the
weeks of this project's open dailies:

```bash
date +%G-W%V                      # current week
date -d <YYYY-MM-DD> +%G-W%V      # the daily's week
```

Same week — nothing to sweep, say nothing. Different — offer to close.

**What qualifies.** Only the intersection of three conditions:

```bash
gh issue list -R "$REPO" --state open \
  --label "<Project>" --label ready-to-close \
  --limit 100 --json number,title,createdAt
```

- **this project** — other projects' dailies are not touched;
- **`ready-to-close`** — the day was handed over. A daily without the label stayed
  open for a reason: it was never handed over, and closing it silently is wrong;
- **a previous week or earlier** — never the current one, not even Monday's.

**How to close.** Reason `completed` — the work was done, not abandoned:

```bash
gh issue close <N> -R "$REPO" --reason completed
```

**Show the list and wait for confirmation.** Closing is visible to the whole
organisation and happens in a batch; a mistake there is noticed late and undone
by hand.

## The shape of a handoff comment

```markdown
<!-- ephemeris:handoff session="panel-claude" kind="day" -->
## 🔄 Shift handoff — HH:MM

**State.** `feat/x` = `abc1234`, merged into main · tree clean · no worktrees in
tmp · staging is up and opens

**Where things are.**
- the front-page failure write-up — `#issuecomment-5175291319`
- customer answers about warehouses — `ctx:priyomka#i004`
- payment split question — `ctx:priyomka#q007`
- importer fixes — `<repo>#110`, PR `<repo>#112`
- rule "English on screen ≠ a translation" — assistant memory

**Continue from.** E1.39 — 337 untranslated strings left, all of them deliberate;
the reasons are recorded in the dictionary file.

**Not closed.** The mail sender — a launch blocker, not solvable in code.
```

The marker on the first line is mandatory: it is how the handoff is found among
the other comments. `State`, `Where things are`, `Continue from` are always
present; `Not closed` when there is something.

Write the content itself in the language of the daily.

## The handoff is a map, not a retelling

**A handoff does not load the next session with content — it says where things
are.** Retelling the day inside a comment makes a second copy of what is written
next to it: the copy drifts from the original and spends context doing it.

So a handoff is made of addresses. The next session reads it, sees the map and
**decides for itself** what to open. Not needed — not read. Needed later — it
comes back and reads, the address has not moved.

This is not economy for its own sake: even in a large window the choice belongs
to whoever is working, not to whoever wrote the handoff yesterday.

### Address rules

**A reference to archive material is written only as `ctx:<slug>#<id>`.** Not "in
the project archive", not "we discussed it" — the exact identifier, otherwise the
next session cannot resolve it.

**A comment is addressed by its identifier, not by its position.** "The comment
above" stops being true at the next comment; `#issuecomment-<id>` never moves:

```bash
gh api "repos/$REPO/issues/<N>/comments" --jq '.[] | "\(.id)  \(.html_url)"'
```

**Cross-repo links are `<owner>/<repo>#110`, not a bare `#110`.** GitHub resolves
a bare number against the daily repo and the link lands elsewhere.

Everything else is written plainly. "Staging opens, checked by hand" has no
address and does not need an invented one — but it does not get to look verifiable
either: such lines belong under `State`, not under `Where things are`.

**What was not done is not written into the handoff.** "Saved to memory" with no
memory file is a promise, not a report, and the next session discovers the
substitution an hour into the wrong direction. Did not manage it — `Not closed`.

## Resume the shift

**1. Find the handoff.** The last comment carrying `<!-- ephemeris:handoff -->`
in today's daily; no daily for today — in the project's most recent one.

A session is named — take that session's last handoff. Not named — take the most
recent one and list which sessions appeared today.

**2. Walk the addresses and check that they resolve.** Do not take the comment's
word for it:

| Address | Resolved by |
|---|---|
| `ctx:<slug>#<id>` | `mnemo_audit.py --export <dir> --json`, or the material in `raw/` |
| `<owner>/<repo>#NN` | `gh issue view` / `gh pr view` |
| a commit sha | `git show --stat` |
| assistant memory | the file in the project's memory directory |
| a path | read the file |

**3. Report three things:** what came back, what did **not** resolve, and what to
continue from. An address that did not open is said out loud — not half a context
restored in silence.

No handoff at all — read the body and comments in full and say there was none.

## Boundaries

- **A handoff does not replace the devlog dump.** The dump is "what happened", the
  handoff is "where it is now". Neither substitutes for the other: the dump will
  not restore you, the handoff will not explain anything.
- **Written text is not rebuilt.** Statuses, stage and waits are edited; the day's
  write-ups are only extended.
- **No second daily per day and project.** One exists — update it.
- **The list of what belongs in closing a day is deliberately not fixed here.** It
  grows out of the days when something went missing.
