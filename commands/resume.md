---
description: Resume the shift — restore context from the last handoff in the daily
argument-hint: Session name if several ran today; project and contour
---

Use the **ephemeris:daily-handoff** skill.

**Read the live state first:** contour, today's daily for this project — or the
project's most recent one if there is none for today — and its comments.

Find the last comment carrying `<!-- ephemeris:handoff -->`. A session is named —
take that session's last handoff. Not named — take the most recent one and list
which sessions appeared today.

Walk every address and **check that it resolves**: `ctx:` in the archive,
`<owner>/<repo>#NN` through `gh`, a sha through `git show`, memory and paths by
reading them. Do not take the comment's word for it.

Report three things: what came back, what did not resolve, what to continue from.
Say the unresolved ones out loud — do not restore half a context in silence.

No handoff — read the body and comments in full and say there was none.

Report to me in my language.

Session: $ARGUMENTS
