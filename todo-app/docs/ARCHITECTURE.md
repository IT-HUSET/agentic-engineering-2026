# Architecture

## System Overview
<!-- One paragraph: what the system is and what it is built on – language, runtime, main framework.
     Versions stay in the manifest and lockfile. -->

A single-process, server-rendered todo web app: users register, log in, and manage multiple todo lists with todo items (title, note, due date, priority, completion, position). It is written in Python and served by Uvicorn (`run.sh`). FastAPI handles routing and dependency injection (`src/app/main.py`), SQLAlchemy ORM persists to a local SQLite file (`src/app/database.py`), and Jinja2 renders full pages and HTML fragments (`src/app/templates/`). The browser side is HTMX plus Shoelace Web Components and SortableJS, all loaded from CDNs (`src/app/templates/base.html`), with one hand-written script (`src/app/static/js/app.js`). Every endpoint, including those under `/api/`, returns HTML or an empty response with HTMX headers, never JSON. Dependency versions live in `pyproject.toml` and `uv.lock`.

## Key Components
<!-- List major components/modules and their responsibilities. With more than one process,
     deployable units first, then the modules inside each. -->

One deployable unit: the FastAPI app object `app.main:app`.

| Component | Responsibility | Key Files/Dirs |
|-----------|---------------|----------------|
| App entry and wiring | Creates the FastAPI app; lifespan runs `init_db()` and `seed_demo_data()` (demo user plus two lists); mounts `/static`; includes the four routers; handles `SQLAlchemyError` (renders `partials/error.html`, 500) and 401 (HTMX: `HX-Redirect` to `/login?next=...`; otherwise 302) | `src/app/main.py` |
| Persistence | Engine for `sqlite:///./todo.db` with `NullPool`; `SessionLocal`; ORM models `User`, `TodoList`, `Todo` (UUID string keys, `position` columns, composite indexes on owner + position, ORM `cascade="all, delete-orphan"`); `init_db()` via `create_all`; `get_db()` session dependency | `src/app/database.py` |
| Auth and request deps | In-memory `sessions` dict (UUID session id, 1 hour expiry); `get_current_user_id` (raises 401) and `get_optional_user_id` cookie dependencies; `session_id` cookie set httponly, `samesite=lax`, `max_age=3600`; `is_htmx_request` | `src/app/core/deps.py` |
| Page routes | `GET /` redirects by session; `GET /login`, `GET /register`; `GET /app` redirects to the first list or renders the empty state; `GET /app/lists/{list_id}` renders the full app page | `src/app/routes/pages.py` |
| Auth routes | `POST /auth/login` (plain-text password compare, `next` checked by `is_safe_redirect`), `POST /auth/register` (auto-login), `POST /auth/logout`; responses carry `HX-Redirect` | `src/app/routes/auth.py` |
| List routes | `/api/lists`: `GET` (sidebar fragment), `POST` (create, appends at max position + 1), `GET/PUT/DELETE /{list_id}`, `POST /reorder` (takes ordered `list_id` form values; reads the active list from the `Referer` header) | `src/app/routes/todo_lists.py` |
| Todo routes | `/api/todos`: `GET /search` (`ilike` on title within a list), `POST` (quick add, title only), `GET/PUT/DELETE /{todo_id}`, `PATCH /{todo_id}/toggle`, `POST /{todo_id}/reorder` (shifts positions between old and new index); `_verify_list_access` enforces ownership through the parent list (403 on mismatch) | `src/app/routes/todos.py` |
| Template helpers | `is_overdue`, `is_due_today` (calendar-day comparison), `format_date`, `format_date_input`; each router registers them as Jinja globals | `src/app/utils.py` |
| Pydantic models | `LoginRequest`, `RegisterRequest`, `TodoCreate/Update`, `TodoListCreate/Update` with field validators. No route imports them: routes take `Form()` fields and validate inline. Only `tests/test_models.py` uses them | `src/app/models/` |
| Templates | `base.html` (CDN assets), full pages `login.html`, `register.html`, `app.html` (sidebar, main area, Shoelace dialogs); fragments in `partials/` returned by API routes, including out-of-band count updates (`todo_item_with_oob.html`, `todo_deleted_oob.html`) | `src/app/templates/` |
| Client script | Theme toggle persisted in `localStorage`; SortableJS setup for sidebar lists (triggers HTMX `end` on the form) and todos (`htmx.ajax` POST to `/reorder`); edit and delete dialogs fed from `data-*` attributes; re-binds handlers on `htmx:afterSwap`; error toast on `htmx:responseError`; adds no-cache headers on `htmx:configRequest` | `src/app/static/js/app.js` |
| Styles | App styling layered over the Shoelace themes | `src/app/static/css/styles.css` |

## Data Flow
<!-- Describe how data moves through the system. A simple numbered list or diagram reference. -->

1. Startup: Uvicorn imports `app.main:app`; the lifespan creates tables in `./todo.db` and seeds `demo@example.com` if absent (`src/app/main.py`).
2. Login: the HTMX form in `login.html` posts to `/auth/login`; on success the route stores a session in the in-memory dict, sets the `session_id` cookie, and returns `HX-Redirect`; on failure it returns `partials/error.html` into `#error-container` (`src/app/routes/auth.py`).
3. Page load: `/app/lists/{list_id}` reads the cookie via `get_session`, queries the user's lists and the active list's todos ordered by `position`, and renders `app.html` (`src/app/routes/pages.py`).
4. Interaction: HTMX attributes in the templates call `/api/lists` and `/api/todos`; each route resolves the user through `get_current_user_id`, checks ownership through the list's `user_id`, commits through a `get_db` session, and returns a fragment that HTMX swaps into a target (`#main-content`, `#sidebar-lists`, `#todos-list`, `#todo-{id}`).
5. Side effects on other regions: create, toggle and delete of a todo return an `hx-swap-oob` span that updates the sidebar's incomplete count `#list-{id}-count` (`src/app/templates/partials/todo_item_with_oob.html`, `todo_deleted_oob.html`).
6. Reordering: SortableJS drag events either submit the sidebar form (`hx-trigger="end"` on `#sidebar-lists`) or call `htmx.ajax` with the new index; the server rewrites `position` values (`src/app/static/js/app.js`, `src/app/routes/todo_lists.py`, `src/app/routes/todos.py`).
7. Unauthenticated API call: `get_current_user_id` raises 401; the handler in `main.py` answers HTMX requests with `HX-Redirect` to `/login?next=...` (API paths fall back to `next=/app`).

## Integration Points
<!-- External services, APIs, databases the system depends on. -->

| Service | Purpose | Config Location |
|---------|---------|-----------------|
| SQLite file `todo.db` | All persistent data; created on startup, path relative to the working directory; git-ignored (`*.db`) | `src/app/database.py` (`DATABASE_URL`), `.gitignore` |
| In-process session store | Login sessions; a Python dict, lost on restart | `src/app/core/deps.py` (`sessions`) |
| Shoelace via jsDelivr CDN | Web Components, light and dark theme CSS, icon base path | `src/app/templates/base.html` |
| HTMX via unpkg CDN | Declarative AJAX and fragment swaps | `src/app/templates/base.html` |
| SortableJS via jsDelivr CDN | Drag-and-drop reordering of lists and todos | `src/app/templates/base.html` |
| Browser `localStorage` | Persists the theme choice (`theme` key) | `src/app/static/js/app.js` |

## Key Constraints
<!-- Architectural decisions or constraints that shape the system. Reference ADRs if available. -->

- Educational, not production: passwords are stored and compared in plain text, and sessions are in memory (`README.md`, `src/app/database.py`, `src/app/core/deps.py`).
- HTML over the wire: routes return Jinja fragments and `HX-*` headers; there is no JSON API.
- Paths are relative to the working directory (`src/app/templates`, `src/app/static`, `./todo.db`), so the app must be started from the project root; `run.sh` does `cd "$(dirname "$0")"` first.
- Schema is created by `Base.metadata.create_all`; there are no migrations, so column changes need the database file recreated.
- Cascading deletes rely on the ORM relationship cascade; no code enables SQLite's `PRAGMA foreign_keys`, so the `ondelete="CASCADE"` clauses are not enforced by the database itself.
- Ownership is enforced per route by filtering on `TodoList.user_id`; todos are authorized through their parent list (`_verify_list_access`).
- Front-end libraries come from public CDNs at pinned versions in `base.html`; the UI does not work offline.

## Testing

- **Framework:** pytest with FastAPI's `TestClient` (httpx). Both are runtime dependencies in `pyproject.toml` by design ("workshop simplicity"). `[tool.pytest.ini_options]` sets `pythonpath = ["src"]` and `testpaths = ["tests"]`. Run with `uv run pytest` (`README.md`).
- **Layout:** flat `tests/` package, one file per area, test classes grouping related cases.

  | File | Covers | Tests |
  |------|--------|-------|
  | `tests/test_auth.py` | Register, login, logout, `next` redirect, open-redirect guard, protected pages and API 401 | 13 |
  | `tests/test_todo_lists.py` | List CRUD, empty-name error, cascade to todos, reorder | 8 |
  | `tests/test_todos.py` | Todo CRUD, toggle, OOB count on delete, reorder up and down, search (case-insensitive, empty query), cross-user access | 13 |
  | `tests/test_integration.py` | Multi-step user journeys (register to verify after re-login), cascades, `next` on protected routes, count updates, search | 6 |
  | `tests/test_models.py` | Pydantic validators in `src/app/models/` | 19 |
  | `tests/test_utils.py` | `is_overdue` and `is_due_today` calendar-day semantics | 4 |

- **Fixtures (`tests/conftest.py`):** `db_session` (fresh in-memory SQLite with `StaticPool`, tables created and dropped per test); `client` (overrides `get_db` with `db_session`, clears the `sessions` dict before and after); `test_user`; `authenticated_client` (creates a session directly and sets the `session_id` cookie); `test_list`; `test_todo`.
- **Helpers:** `tests/test_utils.py` builds todos as `SimpleNamespace` objects (`_todo`, `_midnight`) instead of ORM rows.
- **Patterns:** route tests assert on status codes, `HX-Redirect` headers, rendered HTML substrings, and database state read back through `db_session`.
- **Integration and E2E:** "integration" means multi-request journeys through `TestClient`; there is no browser or E2E suite, so HTMX swaps, SortableJS and `app.js` are untested.
- **Coverage:** no coverage tool or threshold is configured.
- **Gotcha:** `TestClient(app)` runs the lifespan, and `init_db()` and `seed_demo_data()` use the module-level engine, not the override. Tests therefore create and seed `./todo.db` in the working directory even though requests use the in-memory database.
