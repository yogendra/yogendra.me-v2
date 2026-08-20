# Yogendra.Me — Agent Operating Context (AGENTS.md)

This repo is a Hugo static blog/portfolio (yogendra.me) that is intentionally
designed to be enhanced by an AI coding agent. This file is the canonical
project context, readable by every agent that works here (Hermes, Antigravity /
Gemini CLI, Claude Code, Codex, OpenCode).

## Core Technologies

- **Static Site Generator**: [Hugo](https://gohugo.io/)
- **Theme**: `hugo-clarity`
- **Orchestration**: [go-task](https://taskfile.dev/) (`Taskfile.yml`, `Taskinit.yml`)
- **Hosting/Deployment**: [Firebase Hosting](https://firebase.google.com/products/hosting)
- **CI/CD**: Task-based automation in GitHub Actions.

## Important Directories

- `content/`: Where all the written content lives.
  - `posts/`: Blog posts, organized by year (e.g., `content/posts/2024/`).
  - `projects/`: Portfolio projects.
- `layouts/`: Custom HTML templates and shortcodes.
- `assets/`: Resources like CSS and JS that are processed by Hugo.
- `static/`: Static files (images, PDF, etc.) served directly.
- `config/`: Configuration files split by environment.
  - `_default/`: Base configurations.
  - `local/`, `firebase/`, `github/`: Environment-specific overrides.
- `.agents/skills/`: Authoritative skill docs for content + publishing (see below).

## Key Configuration

- **Base URL**: `https://yogendra.me`
- **Permalinks**: `/:year/:month/:day/:slug/`
- **Taxonomies**: Categories, Tags, Series.

## Agent Skills (source of truth for workflows)

- `.agents/skills/tech-blogging/SKILL.md` — how to write/publish technical posts (page-bundle conventions, frontmatter standards, Mermaid diagrams, staging, publishing checklist).
- `.agents/skills/publisher/SKILL.md` — release/beta verification + LGTM approval runbook.
- The `Taskfile.yml` also exposes these as runnable tasks (see below).

Do NOT duplicate skill content into this file — point to the skills. This file
only carries project facts and agent-binding workflow notes.

## Common Workflows (via go-task / `task`)

### Environment Setup
```bash
task init
```

### Local Development
```bash
task run
```
Runs the Hugo dev server with drafts (`-D`), future-dated (`-F`), and expired (`-E`) posts enabled.

### Creating a new post
```bash
task post:create -- "My Post Title"
```
Creates `content/posts/YYYY/MM/<slug>/index.md` with draft frontmatter.

### Build and Deploy
- `task build` — builds for local testing.
- `task beta:deploy` — deploys to beta Firebase (Cloudflare `beta.yogendra-me.pages.dev`).
- `task release:deploy` — builds + deploys to production Firebase + GitHub Pages.

### Live Staging
- **Preview URL**: `https://blog.hs.yogendra.me` — an always-on homelab container watches the repo, auto-rebuilding drafts/future on save.

## Design and Customization

- Clarity theme with customizations in `layouts/`.
- **Shortcodes**: custom shortcodes in `layouts/shortcodes/`.
- **Diagrams**: Mermaid.js via Hugo code-block rendering. PlantUML and Java support have been removed.

## Creating & Publishing a Post (agent workflow)

1. Scaffold: `task post:create -- "Your Title"` → `content/posts/YYYY/MM/<slug>/index.md`, `draft: true`.
2. Draft per `.agents/skills/tech-blogging/SKILL.md` (Mermaid diagram, copy-pasteable config, tags/categories/series).
3. Verify live at `https://blog.hs.yogendra.me`.
4. Publish (approval-only): flip `draft: false`, then `git add content/posts/YYYY/MM/<slug>/`, `git commit -m "feat(blog): publish <slug>"`, `git push origin main`. GitHub Actions deploys to `yogendra.me` + GitHub Pages.
   - For full release verification + LGTM: `python3 .agents/skills/publisher/scripts/verify_beta.py --approve`.

## Core Agent Invariant

When an agent receives a research topic (e.g. via Telegram/DM), treat it as a
**draft-first** task: scaffold, research + outline + draft, present on the
staging URL, and **DO NOT publish (flip `draft: false` or push) without explicit
user approval.** Hermes agents load the `blog-yogendrame` skill for the operational
wrapper.