# `databases/` (legacy duplicate folder)

This project's skeleton included both `server/database/` (used by the running app —
see `app/main.py`) and `server/databases/` (this folder). To avoid breaking either
naming convention, `databases/` is kept as a set of thin wrappers/re-exports around
the real implementation in `server/database/`. If you're integrating with the API,
use `server/database/`; this folder exists purely for compatibility.
