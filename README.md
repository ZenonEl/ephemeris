# Ephemeris

[![Version](https://img.shields.io/badge/version-0.9.1-6f42c1.svg)](#status)
[![Instructions](https://img.shields.io/badge/package-agent%20instructions-0969da.svg)](skills/daily-handoff/SKILL.md)
[![License](https://img.shields.io/badge/code-AGPL--3.0--or--later-blue.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE-docs)

**English** · [Русский](README.ru.md)

Ephemeris is a Claude Code plugin and Codex skill for issue-based daily
handoffs. One daily issue keeps the state of a project day. When an agent
session ends, it leaves source addresses for the next session instead of
rewriting the same context into another summary.

The package contains agent instructions, not an application or background
service. GitHub issues remain the visible record, while project evidence can
stay in its original repository or archive.

## Daily cycle

| Command | Purpose |
|---|---|
| `/ephemeris:init` | Open the daily issue and carry over unfinished work. |
| `/ephemeris:update` | Update state and append technical notes during the day. |
| `/ephemeris:pass` | Hand the current session to another session without closing the day. |
| `/ephemeris:handoff` | Finish the day, record the final state, and mark it ready for cleanup. |
| `/ephemeris:resume` | Resolve the recorded addresses and continue from verified context. |

```mermaid
flowchart LR
    work["Work and source artifacts"] --> daily["Daily GitHub issue"]
    daily --> pass["Session handoff"]
    pass --> resolve["Resolve ctx IDs, issues, PRs, and commits"]
    resolve --> next["Next agent session"]
    next --> daily
```

## Requirements

- [`gh`](https://cli.github.com/), authenticated for the repository that stores
  the daily issues.
- **A repository for the dailies.** Ephemeris does not create the convention,
  it follows one. That repository holds one issue per (date, project) and keeps
  the body template in its own `README.md`.

Ephemeris reads that template before writing anything, and never stores a copy
of it. Reporting formats change; a copy inside a plugin would fall behind in
silence.

## Install

Claude Code:

```
/plugin marketplace add ZenonEl/ephemeris
/plugin install ephemeris@ephemeris
```

Codex:

```
codex plugin marketplace add ZenonEl/ephemeris
codex plugin add ephemeris@ephemeris
```

Both hosts install the same skill from the same directory. Codex has no slash
commands, so there the skill is triggered by phrasing; the command names above
are operation names, and the skill describes each operation on its own.

## Update

```
/plugin marketplace update ephemeris          # Claude Code
codex plugin marketplace upgrade              # Codex, then codex plugin add again
```

Both hosts compare **only the version number**. The number lives in three
manifests and two README badges, so `scripts/check-versions.py` verifies they
agree — a stale manifest means the change never reaches installed copies while
the update command reports everything as current.

## Configuration

Repository addresses live outside this package, in
`~/.config/ephemeris/daily.conf`:

```ini
default = work

[work]
repo     = <owner>/<repo>
assignee = <login>

[personal]
repo     = <owner>/<repo>
```

Every section is a contour. `assignee` is optional — contours may follow
different conventions, and Ephemeris reads each one from its own repository
rather than carrying settings across.

If the file or the requested contour is missing, the instructions require the
agent to ask instead of guessing a default.

## Design choices

### A handoff is an address map

A copied summary becomes a second version of nearby information and can drift
from it. Ephemeris records stable addresses instead: a GitHub comment ID, an
issue or pull request, a commit, a path, or a `ctx:<slug>#<id>` citation. The
receiving session resolves each address and reports anything it cannot open.

The reader decides what to open. An address costs almost nothing to carry and
can be followed later; a summary spends context on a decision that was already
made by someone else.

### A day and a session are different units

Several agent sessions may work during one day. `pass` closes only the current
session; `handoff` closes the work day. This keeps one daily issue per project
and date without forcing intermediate sessions to write a final report.

### Work and personal records stay separate

Ephemeris selects a configured contour before it writes anything. Work and
personal dailies use different repositories rather than labels in one shared
repository. If the contour cannot be selected unambiguously, the instructions
require the agent to ask.

### Several sessions share one daily

The unit of markup is the **session** — not the project, the agent, or the model.
Two terminals on one project in one day are two sessions even when the same
person runs both.

Each session keeps its own analyses inside its own block and edits nothing
outside it:

```markdown
<!-- ephemeris:begin session="checkout" -->
## 🛠 checkout — what this session worked through
<!-- ephemeris:end session="checkout" -->
```

Shared sections stay shared: stage, done, phase goals and blockers are common to
the day, and ownership is written into the status line itself
(`🔒 blocked, checkout's area`, `🔄 led by checkout`). Comments carry the session
in their marker, so `resume` can pick up the right thread.

A session takes `main-<agent>` — `main-claude`, `main-codex` — when nobody else
has written in today's daily yet, and a scope name otherwise: `panel-claude`,
`orders-codex`. The scope is the area the session works in, not a single task.

Sessions are named, never numbered. "The second session" counts from whoever is
speaking; for the other session the second one is somebody else.

### Every action reads the live state first

Sessions run in parallel and the issue changes underneath them, so each command
begins by fetching the daily as it is now: whether one exists for today, whether
there are two of them, which sessions have written, whether the day is already
closed. Nothing is taken from memory or from an earlier step of the same
conversation.

Writes that depend on that reading re-read immediately before writing. The gap
between reading and writing is where a lost update lives — and where a day once
got closed twice in the same minute.

Duplicate dailies happen. The one holding the work is kept, the empty twin is
closed with a reference to it, and both are shown before anything is closed.

### The package is English, the output is not

These instructions are English to keep the agent's context cheap. What a human
reads is written in that human's language: the daily follows its repository and
the surrounding issues, and the terminal follows the user. Markers, attribute
names and status keywords are never translated.

### Cleanup is explicit

A completed handoff receives the `ready-to-close` label. On a later week,
Ephemeris can propose closing older labelled dailies for the same project. It
shows the list first and waits for confirmation.

A daily without the label stays open on purpose: it was never handed off, and
closing it silently would erase that signal.

## Place in the toolchain

| Project | Responsibility |
|---|---|
| [mnemo](https://github.com/ZenonEl/mnemo) | Stores source material, provenance, decisions, and open questions. |
| **Ephemeris** | Tracks the day and passes source addresses between sessions. |
| [herald](https://github.com/ZenonEl/herald) | Moves messages and files between people and agents. |

The projects exchange published formats and links. They do not share a runtime,
database, or library.

## Package layout

```text
.claude-plugin/          Claude Code plugin and marketplace manifests
.codex-plugin/           Codex plugin manifest
.agents/plugins/         Codex marketplace entry
commands/                Five Claude Code commands
skills/daily-handoff/    The portable skill, shared by both hosts
scripts/                 Version-consistency check
```

There is one copy of the skill, not one per host. Two copies would teach two
different sets of rules and drift apart unnoticed.

## Status

Ephemeris is an early `0.9.1` specification package maintained by one author.
Its only executable file checks that the version number matches across
manifests; there are no automated tests, CI, or usage telemetry. The current
value is the documented handoff protocol and its separation of daily state,
source evidence, and communication.

The package is written in English; what it produces follows the language of the
daily repository and of the user.

## Licenses

- `commands/` and `skills/`: [AGPL-3.0-or-later](LICENSE)
- documentation: [CC BY-SA 4.0](LICENSE-docs)
