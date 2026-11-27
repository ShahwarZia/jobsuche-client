# jobsuche-client

Typed async Python client and FastAPI wrapper for the unofficial
Bundesagentur für Arbeit Jobsuche API.

## Commands
- Install: `uv sync`
- Lint: `uv run ruff check`
- Format: `uv run ruff format`
- Type check: `uv run mypy src`
- Tests: `uv run pytest`

## Workflow rules
- Propose a plan before editing files. Wait for my approval.
- After every change run lint, type check and tests. All must pass.
- Do not commit or push. I do that.
- Do not add dependencies without asking.
- Type hints on every function (mypy strict). No `Any` without a comment explaining why.

## API facts (verified 27 Nov 2026)
- Base URL: https://rest.arbeitsagentur.de/jobboerse/jobsuche-service
- Header: `X-API-Key: jobboerse-jobsuche`
- Search: GET /pc/v6/jobs (v4 returns 403)
- Details: GET /pc/v4/jobdetails/{base64(refnr)} (v3, v5, v6 return 403)
- Field names are German. Models expose English names via `Field(alias=...)`.
- Empty search omits `ergebnisliste`. List fields need `default_factory=list`.
- `angebotsart=1` means regular jobs. Default to it.

## Tests
- Unit tests never hit the network. Use tests/fixtures with httpx.MockTransport.
- Live API tests are marked `contract` and excluded from the default run.
- Never edit fixture files to make a test pass.