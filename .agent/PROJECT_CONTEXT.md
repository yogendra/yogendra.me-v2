# Project Context: Yogendra.Me-v2

This is a Hugo-based static site for Yogendra's blog and portfolio. It is designed to be easily enhanced by an AI coding agent.

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

## Key Configuration
- **Base URL**: `https://yogendra.me`
- **Permalinks**: `/:year/:month/:day/:slug/`
- **Taxonomies**: Categories, Tags, Series.

## Common Workflows

### Environment Setup
To initialize the development environment (installs Hugo, Go, Node.js, etc.):
```bash
task init
```

### Local Development
To start the Hugo development server:
```bash
task run
```

### Creating new content
Use the provided task to create a new post:
```bash
task post:create -- "My Post Title"
```

### Build and Deploy
Managed via `Taskfile.yml`:
- `task build`: Builds for local testing.
- `task release:deploy`: Builds and deploys to production Firebase.
- `task beta:deploy`: Builds and deploys to beta Firebase.

## Design and Customization
- The site uses the **Clarity** theme, with customizations in `layouts/`.
- **Shortcodes**: Custom shortcodes are located in `layouts/shortcodes/`.
- **Diagrams**: The project supports [Mermaid.js](https://mermaid.js.org/) diagrams using Hugo's code block rendering (`layouts/_markup/render-codeblock-mermaid.html`). PlantUML and Java support have been removed.

## Future Enhancements
- Adding new blog posts or updating project details.
- Tweaking CSS in `assets/` or layout overrides in `layouts/`.
- Implementing new shortcodes for richer content display.
