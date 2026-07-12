# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

FastAPI backend for "Google Tasks API" — a FastAPI backend inspired by Google Tasks, featuring lists,
tasks, due dates, priorities, labels, JWT authentication, server-rendered dashboard pages (Jinja2 +
Bootstrap), and a PostgreSQL database via SQLAlchemy/Alembic.

## Commands

The app runs inside Docker Compose; most `make` targets shell into the `backend` container.

```sh
make build            # docker compose build --no-cache
make up                # start db + backend (uvicorn --reload on :8000)
make down / make restart
make logs / make logs-app / make logs-db

make shell             # shell into the backend container
make db-shell          # psql into the db container (via docker exec)
make psql              # psql from host, reading creds out of .env

make alembic-upgrade                 # alembic upgrade head
make alembic-revision msg="message"  # alembic revision --autogenerate -m "message"

make test               # pytest -v (inside container)
make lint               # ruff check .
make format             # ruff format .

make reset-db           # drops volumes, recreates db, then backend (run alembic-upgrade after)
```

Equivalent commands can be run directly with `docker compose exec backend <cmd>`, or locally with `uv`/`pip`
if `DATABASE_URL` env vars point at a reachable Postgres instance. Config is loaded from a `.env` file (see
`.env-example` for required vars: `SECRET_KEY`, `ALGORITHM`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`,
`DB_PORT`).

To run a single test: `docker compose exec backend pytest -v app/tests/test_main.py::test_name`.
Note: `app/tests/test_main.py` currently has no working test bodies — the test suite is a stub, not yet a
safety net for regressions.

## Architecture

- **Entrypoint**: `app/main.py` builds the `FastAPI()` app, calls `Base.metadata.create_all(bind=engine)`
  (tables are created at startup rather than solely through Alembic), mounts `app/static/`, and wires in the
  five routers under `app/routers/`. Docker/uvicorn point at `app.main:app`. The root-level `main.py` is an
  unrelated `uv init` stub — not part of the running app.
- **Routers** (`app/routers/`), each an `APIRouter` with its own prefix:
  - `auth.py` (`/auth`) — user registration and `/auth/token` login (JSON body: `email`/`password`),
    issues JWTs. Protected routes authenticate via `HTTPBearer` (a raw `Authorization: Bearer <token>`
    header), not the OAuth2 password/form flow.
  - `todos.py` (`/todos`) — CRUD for the authenticated user's own todos.
  - `admin.py` (`/admin`) — todo CRUD across all users, gated by `user_role == "admin"`.
  - `users.py` (`/users`) — current-user profile fetch/update and password change.
  - `views.py` (`/dashboard`) — server-rendered Jinja2 pages (login/register), not JSON API.
- **Auth model**: `app/dependencies.py` defines `get_current_user`, which decodes the JWT (via
  `app.core.settings.SECRET_KEY`/`ALGORITHM`) into a plain dict `{"username", "id", "user_role"}` — there is
  no ORM user object attached to the request, so handlers re-query `User` by id when they need more fields.
  `user_dependency` / `db_dependency` (`Annotated[...]` aliases in `dependencies.py`) are the standard way
  handlers pull the current user / DB session; reuse them rather than re-declaring `Depends(...)` inline.
  Password hashing uses `bcrypt_context` (passlib); token creation logic lives in `app/services.py`
  (`authenticate_user`, `create_access_token`).
- **Data layer**: `app/core/database.py` creates the SQLAlchemy `engine`/`session_local`/declarative `Base`
  from `DATABASE_URL` (built in `app/core/settings.py` from discrete `DB_*` env vars, loaded via
  `environs`). Models live in `app/models/` (`User`, `Todos`, `List`) and are re-exported through
  `app/models/__init__.py` — new models must be added there too, since `app/alembic/env.py` imports
  `app.models` as a whole to populate `target_metadata` for autogeneration. `Todos.list_id` and
  `List.owner_id` exist as FKs but there is currently no `lists` router.
- **Schemas**: Pydantic request/response models live in `app/schemas/` (`user.py`, `todo.py`), separate from
  the SQLAlchemy models in `app/models/`. Keep this split when adding new resources.
- **Migrations**: Alembic is configured to point at `app/alembic` (see root `alembic.ini`,
  `script_location = app/alembic`). `app/alembic/env.py` reads `DATABASE_URL` from
  `app.core.settings` rather than `alembic.ini`, and imports `app.models` for autogenerate — new model
  modules need `from .newmodel import X` added to `app/models/__init__.py` or they won't be picked up.
- **Templates/static**: `app/templates/` (Jinja2: `layout.html`, `login.html`, `register.html`, `home.html`)
  and `app/static/` (Bootstrap 5.3.8 vendored, plus project CSS/JS) back the `/dashboard` views router.
- **API docs collections**: Bruno (`.bruno/`) and an OpenAPI-derived collection (`docs/collection/`) contain
  request examples grouped by Auth/Todos/Admin/Users — useful references for expected request/response
  shapes when a router lacks a Pydantic response model.

## Notes

- Lint/format is Ruff (see `.pre-commit-config.yaml`); no project-specific `[tool.ruff]` overrides exist in
  `pyproject.toml`, so defaults apply.
- `Dockerfile` installs from `requirements.txt` via a custom `PIP_INDEX_URL` (`pypi.devneeds.ir`); `uv.lock`
  reflects `pyproject.toml`'s dependencies for local `uv` usage — keep both in sync if adding a dependency.
