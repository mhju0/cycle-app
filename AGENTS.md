# Repository guidance

Public support and privacy pages for the Cycle iOS app (source app: the local `period-tracker` repo). GitHub Pages serves `main` from the root at https://mhju0.github.io/cycle-app/, so merging to `main` publishes. Hand-written HTML and one stylesheet; no build step.

- At session start, read `.memory/README.md` if it exists (private, git-ignored). Before ending a session that changed something, update `.memory/handoff.md`.
- The privacy page must match what the app actually does (no network code, analytics, ads or accounts). Check the app's `docs/spec.md` before changing it.
