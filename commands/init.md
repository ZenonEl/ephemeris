---
description: Open today's daily — the day's plan and yesterday's carry-over
argument-hint: Project; session name and contour (work | personal) if not obvious
---

Use the **ephemeris:daily-handoff** skill.

1. **Read the live state first.** Determine the contour, then find today's daily
   for this project and read its body and comments. One exists — do not create a
   second, go to `/ephemeris:update`. More than one — handle the duplicate before
   anything else.
2. **Take your session name.** Nobody has written yet → `main-<agent>`. Someone
   has → a scope name `<scope>-<agent>`; unclear → ask once.
3. **Read the template** from the daily repo's `README.md` — it may have changed.
4. **Carry over from the project's previous daily**: `🎯 phase goals` with their
   statuses and running numbering, blockers and waits with who holds them and
   since when. Closed items are marked, not erased. New ones are marked new.
5. **Build the body:** stage, the day's plan in order, the carry-over. `✅ Done`
   is empty in the morning.

Show me the title, the contour and the body **before** creating the issue. Create
after confirmation, with the project label; assignee only if this contour has one,
as a bare login without `@`.

Write the daily in the language of the daily repository.

Project: $ARGUMENTS
