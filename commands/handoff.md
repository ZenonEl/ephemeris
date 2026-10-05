---
description: Close the day — fixate everything and write the day's handoff
argument-hint: Session name; project and contour (work | personal) if not obvious
---

Use the **ephemeris:daily-handoff** skill.

**Read the live state first:** contour, today's daily, its body and comments, the
sessions present, and whether a `<!-- ephemeris:handoff … kind="day" -->` comment
already exists. **Re-read the comments immediately before writing** — another
session may have closed the day in the meantime.

**It exists — the day is already closed by another session.** Do not rebuild the
shared sections, do not re-apply `ready-to-close`, do not run the weekly sweep.
Fixate your own work and add your handoff as a separate comment below in the
ordinary pass form, naming in its first line who closed the day and where. Do not
edit their comment.

**It does not exist — you are closing the day**, in this order:

1. **Fixate.** Uncommitted into a commit, branches pushed, worktrees out of
   `/tmp`. Whatever goes to memory, archive or local docs is written now.
2. **Bring the daily to its final form** — as `/ephemeris:update`, but for the
   whole day. Detail goes into a dump comment. No daily at all — open one first.
   Other sessions' blocks are not rewritten.
3. **Add the handoff comment** with `kind="day"`. Session handoffs from today are
   collected **as addresses**, not retold.
4. **Verify it landed once:** re-read the comments and confirm exactly one
   `kind="day"` for today. More — say so plainly.
5. **Apply `ready-to-close`**; create the label in this contour if it is missing.
6. **Check the week.** The ISO week changed — offer to close this project's
   dailies from **previous** weeks that carry `ready-to-close`, with reason
   `completed`. Show the list and wait: the batch is visible to everyone. Without
   the label do not close — such a daily was never handed over.

Nothing goes into the handoff that you did not do. Did not manage it — `Not
closed`. Archive material is referenced only as `ctx:<slug>#<id>`.

Write in the language of the daily. Show me the text before sending.

Session: $ARGUMENTS
