# Decisions
> Status: Discovered – requires validation by team

<!-- Reverse-engineered from the code. No ADRs exist (`docs/adrs/` absent), so every entry below is an
     implicit decision inferred from the code, with evidence. Validate, then promote contested ones to ADRs. -->

## Current ADRs

| ID | Title | Status | Scope |
|----|-------|--------|-------|

None found: there is no `docs/adrs/` directory and no ADR-shaped file in the tree.

## Superseded

<!-- Inferred from drift between docs or unused code and the running code; confirm before relying on them. -->

| Prior Decision | Superseded By | Notes |
|----------------|---------------|-------|
| Reorder lists and todos with up/down buttons (`README.md` Features) | Drag-and-drop reordering with SortableJS (`src/app/static/js/app.js`, `POST /api/lists/reorder`, `POST /api/todos/{id}/reorder`) | No up/down controls exist in the templates; the README line is stale or the requirement changed. Inferred, Medium confidence |
| Validate request input through Pydantic models (`src/app/models/auth.py`, `todo.py`, `todo_list.py`) | Inline validation of `Form()` fields in each route (`src/app/routes/*.py`) | No route imports the models; only `tests/test_models.py` does, and the rules differ (e.g. list color pattern). Could also be unfinished work rather than a reversal. Inferred, Low confidence |

## Still Current

- **Language and web framework**: Python `>=3.11` with FastAPI, served by Uvicorn as one ASGI app `app.main:app`. Evidence: `pyproject.toml`, `src/app/main.py`, `run.sh`
- **Rendering model – HTML over the wire**: Every endpoint, including `/api/*`, returns Jinja2 HTML (full pages or fragments) or an empty response with `HX-*` headers; there is no JSON API. Evidence: `src/app/routes/*.py` (`TemplateResponse`, `HX-Redirect`), `src/app/templates/partials/`
- **Front-end stack without a build step**: HTMX 2.0.4 for requests and swaps, Shoelace 2.19.1 Web Components for UI, SortableJS 1.15.6 for drag-and-drop, all from public CDNs at pinned versions, plus one plain global-function script. Evidence: `src/app/templates/base.html`, `src/app/static/js/app.js`
- **Cross-region UI updates via out-of-band swaps**: Fragments that change the sidebar count carry an `hx-swap-oob` span instead of the client refetching. Evidence: `src/app/templates/partials/todo_item_with_oob.html`, `todo_deleted_oob.html`
- **Persistence – SQLite through SQLAlchemy ORM**: One local file `./todo.db`, `NullPool`, `check_same_thread=False`, SQLAlchemy 2.x used through the legacy `Query` API and `declarative_base`. Evidence: `src/app/database.py`
- **Schema management – `create_all`, no migrations**: Tables are created at startup; schema changes need the database file recreated. Evidence: `src/app/database.py` (`init_db`), `src/app/main.py` (`lifespan`)
- **Data model shape**: Three tables `users` → `todo_lists` → `todos`, UUID4 strings as primary keys, integer `position` columns for user-defined order with composite `(owner, position)` indexes, `created_at`/`updated_at` timestamps. Evidence: `src/app/database.py`
- **Cascades in the ORM, not the database**: Deletes cascade through `cascade="all, delete-orphan"`; the `ondelete="CASCADE"` clauses are not enforced because SQLite foreign keys are never enabled. Evidence: `src/app/database.py`, `tests/test_integration.py::test_delete_user_cascades_to_lists_and_todos`
- **Authentication – own email and password, plain text**: Credentials stored and compared in plain text, deliberately, as an educational simplification. Evidence: `src/app/database.py` (comment "Plain text - educational only!"), `src/app/routes/auth.py`, `README.md` (Educational Notice)
- **Sessions – in-memory dict with a cookie**: UUID4 session ids in a module-level dict, 1-hour fixed expiry, `httponly` `samesite=lax` cookie; lost on restart, single process only. Evidence: `src/app/core/deps.py`
- **Authorization – per-user ownership checked in every route**: Lists filtered by `TodoList.user_id`; todos authorized through their parent list (`_verify_list_access`). No roles, no sharing. Evidence: `src/app/routes/todo_lists.py`, `src/app/routes/todos.py`
- **Module boundaries**: `src/` layout with package `app`; one router per resource (`auth`, `pages`, `todo_lists`, `todos`) with URL split pages at `/` and `/app/...`, fragments under `/api/...`, auth posts under `/auth/...`; all ORM models and DB wiring in one file `database.py`; auth dependencies in `core/deps.py`; template helpers in `utils.py`. Evidence: `src/app/`, `src/app/main.py` (`include_router`), `CLAUDE.md` (Conventions)
- **Error convention for HTMX**: Validation errors return an `sl-alert` fragment with status `200` so HTMX swaps it in; `401` becomes a login redirect (`HX-Redirect` or `302`); `SQLAlchemyError` becomes a `500` fragment. Evidence: `src/app/main.py`, `src/app/templates/partials/error.html`, `tests/test_auth.py`
- **Environment and packaging tooling**: uv manages dependencies and the lockfile; hatchling builds the wheel from `src/app`. Evidence: `pyproject.toml`, `uv.lock`, `run.sh`
- **Test tooling**: pytest with FastAPI `TestClient`, a fresh in-memory SQLite per test via a `get_db` override; pytest and httpx are runtime dependencies on purpose "for workshop simplicity". No browser or E2E tests. Evidence: `pyproject.toml` (NOTE comment), `tests/conftest.py`
- **No code-quality tooling**: No formatter, linter, type checker, coverage tool or CI workflow is configured. Evidence: `pyproject.toml`, absence of config files and `.github/`
- **Deployment topology – single local process**: One Uvicorn process started from the project root (relative paths for templates, static files and the database), `--reload` on `0.0.0.0`; no container, no config or environment variables, no production deployment. Evidence: `run.sh`, `README.md`, `src/app/database.py` (`DATABASE_URL` hard-coded)
- **Demo data seeded at startup**: A demo user with two lists is created idempotently on every start so the app is usable immediately. Evidence: `src/app/main.py` (`seed_demo_data`), `src/app/templates/login.html` (pre-filled credentials)

## Pending

- None found in the code.
