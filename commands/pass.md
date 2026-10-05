---
description: Pass the session — the context runs out, the day continues
argument-hint: Session name; project and contour (work | personal) if not obvious
---

Use the **ephemeris:daily-handoff** skill.

**Read the live state first:** contour, today's daily, its comments, and which
sessions are present. Confirm your own session name from that read.

1. **Fixate what is unsaved:** commit, push, worktrees out of `/tmp`, writes to
   memory, archive and local docs. The report is written after, not instead.
2. **Add the handoff comment** with
   `<!-- ephemeris:handoff session="<name>" -->` on the first line and a session
   handoff heading. Then re-read the comments and confirm it posted once.

**Do not bring the body to its final form** — the day is still running. Statuses
in `🎯` only where they changed, and only yours. Write-ups go in your session's
block; other blocks stay untouched.

**The handoff is a map, not a retelling.** Keep it short — it travels back into a
small context window. Do not copy write-ups, address them: a comment is addressed
by `#issuecomment-<id>`, never by "above". Did not manage something — `Not closed`.

Write the comment in the language of the daily. Show me the text before sending.

Session: $ARGUMENTS
