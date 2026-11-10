---
name: nextjs
description: >-
  Next.js 16 (App Router) rules for digimuza apps built from system-template:
  server vs client components, runtime env (one image, many environments),
  proxy.ts, WorkOS session, shadcn/ui, i18n. Use when editing pages, layouts,
  route handlers, server actions, proxy, or app configuration.
---

# Next.js (main framework)

Next.js 16 App Router, React 19, Turbopack, `output: "standalone"`. This version
has breaking changes: read the relevant guide in `node_modules/next/dist/docs/`
before writing code you're unsure about (see `AGENTS.md`).

## Hard rules

- **One image, many environments.** Never read config from `NEXT_PUBLIC_*`:
  Next inlines those at build time. Public URLs (`CONVEX_URL`, `SITE_URL`, …)
  are read at runtime on the server (`getPublicEnv()` in `env.ts`) and passed
  to client components as props. Server config comes from `lib/server-env.ts`
  (env + Infisical, loaded by `scripts/start.mjs` in the container).
- Every page is dynamic (`export const dynamic = "force-dynamic"` in the root
  layout); nothing environment-specific is prerendered.
- **Access:** pages under `/app` call `requireSession({ permission })`
  (redirects); Convex re-checks every call. UI checks (`<Can>`, `useCan`) are
  hints only.
- Middleware is `proxy.ts` (Node runtime). It only refreshes the WorkOS session;
  it guards nothing. Keep `/api/health` and `/api/v1` out of its matcher.
- Server-only modules start with `import "server-only"`.

## Patterns

| Need | Pattern |
| --- | --- |
| Data in a page | server page does `requireSession()`, renders a client view that uses `useQuery(api.…)` (live) |
| Server → Convex | `systemServer()` from `lib/system-server.ts` (forwards the WorkOS token, traces, normalizes errors) |
| Mutations from UI | `useMutation` + `useAction()` from `components/app/use-action` (toasts with error code and operation ID) |
| Server actions | `"use server"` files; never return secrets |
| Agent API | route handlers under `app/api/v1/*` with `createAgentClient({ apiKey })`; decide nothing there |
| UI | shadcn/ui in `components/ui` (`npx shadcn@latest add <name>`), app pieces in `components/app`, Lucide icons, Tailwind v4 tokens; the client's accent is `--primary` |
| UI design | Every UI change, however small, goes through the `impeccable` skill: context step, craft floor while editing, `polish` + detector at the end, and a look at desktop and phone widths in light and dark |
| Strings | `getT()` (server) / `useT()` (client), keys in `lib/i18n/messages.ts`, `lt` and `en` |
| Brand | `brand.ts` only |

## Checks before you finish

`pnpm typecheck && pnpm lint && pnpm test && pnpm build`. For UI changes, look
at the page in light and dark, desktop and phone.
