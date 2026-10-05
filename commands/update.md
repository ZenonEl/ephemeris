---
description: Update today's daily — body and comments
argument-hint: What to record; session name and contour if not obvious
---

Use the **ephemeris:daily-handoff** skill.

**Read the live state first:** contour, today's daily for this project, its body
and comments, and which sessions have already written. No daily — open one with
`/ephemeris:init`, do not append to yesterday's. Take your session name from what
that read shows.

Record what actually happened:

- **body** — surgically: statuses in `🎯`, stage, waits, new tasks under new
  numbers. Do not rebuild existing write-ups, extend them; your own go in your
  session's block between markers, other blocks stay untouched;
- **comments** — devlog: detail, commands, output, `file:line`, diffs, technical
  register. First line is `<!-- ephemeris:devlog session="<name>" -->`.

This is not closing the day: fixate nothing and write no handoff. Do not record
as done what has no commit or check behind it.

Write in the language of the daily. Show me what you are about to record before
sending it.

Record: $ARGUMENTS
