# Paperclip — Skills Reference

## What This Project Does
Open-source orchestration platform for zero-human companies. A Node.js server and React UI that orchestrates a team of AI agents to run a business. Supports multiple agent adapters (OpenClaw, Claude Code, Codex, Cursor, Bash, HTTP). Features org charts, budgets, governance, goal alignment, and agent coordination. Monorepo managed with pnpm.

## How to Run
- Install: `pnpm install`
- Dev (full stack, watch mode): `pnpm dev`
- Dev (once): `pnpm dev:once`
- Dev (server only): `pnpm dev:server`
- Dev (UI only): `pnpm dev:ui`
- Build all: `pnpm build`
- Test: `pnpm test` (vitest)
- Test (single run): `pnpm test:run`
- Typecheck: `pnpm typecheck`
- E2E tests: `pnpm test:e2e` (Playwright)
- Requires: Node.js 20+, pnpm 9.15.4, PostgreSQL (DATABASE_URL required)
- Default port: 3100

## Key Files
- `server/src/`: Main server source code (Express API)
- `packages/`: Monorepo packages
  - `packages/db/`: Database layer (Drizzle ORM, PostgreSQL)
  - `packages/shared/`: Shared types and utilities
  - `packages/adapters/`: Agent adapter implementations
  - `packages/adapter-utils/`: Adapter utility functions
  - `packages/plugins/`: Plugin packages
- `cli/`: Command-line interface (`pnpm paperclipai`)
- `scripts/`: Build, release, and utility scripts
- `docs/`: Documentation (Mintlify)
- `tests/e2e/`: End-to-end Playwright tests
- `evals/`: Evaluation suite (promptfoo)

## Database
- Generate migrations: `pnpm db:generate`
- Run migrations: `pnpm db:migrate`
- Backup: `pnpm db:backup`
- Requires `DATABASE_URL` environment variable

## Common Tasks
- Start development: `pnpm dev` (watches for changes, rebuilds automatically)
- Run CLI: `pnpm paperclipai`
- Check forbidden tokens: `pnpm check:tokens`
- Release: `pnpm release` (or `pnpm release:canary` / `pnpm release:stable`)
- Run docs locally: `pnpm docs:dev`
- Run smoke tests: `pnpm smoke:openclaw-join`
