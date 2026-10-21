# CLAUDE.md

Owner: Alex. Personal project (not MKS code — never paste company code or data here).

## Mode — edit this one line per project
MODE: LEARN
<!-- BUILD = you write the code. LEARN = I write the logic; you explain concepts,
     signatures and errors, and only write boilerplate/styling (e.g. Tailwind). -->

---

## 1. Think before coding (Karpathy)
- State assumptions in 1–3 bullets before any non-trivial change.
- If the request has 2+ readings, list them and ask ONE discriminating question. Don't pick silently.
- If a simpler approach exists than what I asked for, say so before building mine.
- Confused? Say what's unclear. Don't paper over it with code.
- Trivial fixes (typo, rename, one-liner): skip this, just do it.

## 2. Simplicity first (Karpathy)
- Minimum code that solves the stated problem. No speculative features, flags, or "for later" hooks.
- No new abstraction (class, base class, plugin layer) until there are 2 real callers.
- No new dependency without naming it and why stdlib isn't enough.
- If the result is long, check whether a much shorter version does the same job. Prefer that.

## 3. Surgical changes (Karpathy)
- Touch only lines the task needs. No drive-by reformatting, renaming, or "cleanup".
- Match the existing style of the file, even if you'd write it differently.
- Remove imports/vars/functions that YOUR change made unused. Leave pre-existing dead code alone — mention it instead.
- Keep variable names stable when only values change (env/config differences).

## 4. Goal-driven execution (Karpathy)
- Turn every task into a check I can run: a test, a command, an expected output.
  - "Fix bug" → write a failing test/repro first, then make it pass.
  - "Refactor X" → tests pass before and after, behaviour unchanged.
- After changing code, RUN it. Report the actual output, not "this should work".
- Never claim something is done that you didn't execute.

---

## How I work
- One step at a time. Small diff → I run it → I confirm → next step.
- One commit per working step. Imperative message: `Add section-split for email body`.
- Side question mid-task? Answer in 1–2 lines, then return to the main thread.
- When I ask "why", answer the why — tight, no lecture.

## Output format (I have ADHD)
- First line = the command, `path/file.py:42`, or the code. Never a preamble.
- Diffs or full replacement blocks. Never "change the part where...".
- Runnable commands, not descriptions of commands.
- Number multi-step work. Max 5 items per list.
- Each reply ends with: `Step N of M done: X. Next: Y` — one action, under 2 minutes.
- Errors: location → expected vs actual → cause → fix. No "uh oh".
- Don't explain code I didn't ask about.
- Destructive actions (rm -rf, force push, migrations, dropping tables): STOP and confirm first.
- 3 attempts still broken → stop iterating, name the assumption that might be wrong, ask one diagnostic question.

## Engineering defaults
**Data integrity**
- Quarantine over silent correction. Bad input → explicit error path / quarantine folder, never auto-fix.
- IDs stay strings: postal codes, tax IDs (NIP), invoice numbers, account numbers. Never cast to int.
- Use explicit sentinels/guards (`-1`, `None` checks) and fail loudly at boundaries.
- `copy.deepcopy` per record when filling nested dicts from a template.

**Python**
- One venv per project. Pin deps in `requirements.txt` (or `pyproject.toml`).
- Paths via `pathlib`, anchored on `Path(__file__).resolve().parent`. Never rely on CWD.
- Read text with `encoding="utf-8-sig"` when files may have a BOM.
- CLI scripts: non-zero exit code on failure + a short status token on stdout (`STATUS:OK`, `STATUS:NO_MATCH`) so callers can branch.
- Config-driven: mappings/labels in a JSON config, not hardcoded in logic.
- Type hints on public functions. f-strings. No bare `except:`.

**Regex / parsing**
- Escape variables in patterns (`re.escape`).
- Named groups over string slicing/trimming.
- Anchor on stable patterns (e.g. postcode `\d{2}-\d{3}`), not on labels that vary.
- When labels repeat across sections, split into sections first, then search within the slice.

**Privacy / local-first**
- Sensitive data stays local. Don't add calls to external APIs or hosted AI without asking.
- Secrets in `.env` (gitignored). Never print or commit tokens.

## Stack I use (only relevant parts apply per project)
- Python (FastAPI, SQLAlchemy, Alembic, PyMuPDF, RapidOCR, lxml), PostgreSQL, SQL
- React + TypeScript + Tailwind
- Docker, Git, GitHub
- R for stats/econometrics
- Dev machine: Nobara Linux (Fedora-based) — use `dnf`, bash commands

## Project specifics
- What this project does (1 line): app that uses spotify API to pull songs based on user's location, weather, time of day, season
- Run: `source .venv/bin/activate && python -m app.main`
- Test: pytest -q
- Lint: 
- Entry point: app/main.py
- Don't touch: .env`, `data/raw/`, `migrations/` (ask first)
- Gotchas: Spotify tokens expire after 1 h, so refresh before calls. Market IDs stay strings.
