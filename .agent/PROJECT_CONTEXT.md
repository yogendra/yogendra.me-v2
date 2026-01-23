# Project Context: Yogendra.Me-v2

This is a Hugo-based static site for Yogendra's blog and portfolio. It is designed to be easily enhanced by an AI coding agent.

## Core Technologies
- **Static Site Generator**: [Hugo](https://gohugo.io/)
- **Theme**: `hugo-clarity`
- **Hosting/Deployment**: [Firebase Hosting](https://firebase.google.com/products/hosting)
- **CI/CD**: Custom shell scripts in `scripts/` and GitHub Actions.

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
- `scripts/`: Utility scripts for development and CI/CD.

## Key Configuration
- **Base URL**: `https://yogendra.me`
- **Permalinks**: `/:year/:month/:day/:slug/`
- **Taxonomies**: Categories, Tags, Series.

## Common Workflows

### Local Development
To start the Hugo development server:
```bash
hugo serve -D
```
Or for local environment specific config:
```bash
hugo serve -e local
```

### Creating new content
Use the provided script or standard hugo command:
```bash
hugo new posts/2025/my-new-post.md
```

### Build and Deploy
The `scripts/ci` script manages builds and deployments:
- `scripts/ci build`: Builds for various environments.
- `scripts/ci deploy`: Builds and deploys to production Firebase.
- `scripts/ci deploy-beta`: Builds and deploys to beta Firebase.

## Design and Customization
- The site uses the **Clarity** theme, with customizations in `layouts/`.
- **Shortcodes**: Custom shortcodes are located in `layouts/shortcodes/`.
- **PlantUML**: The project supports PlantUML diagrams (prepared via `scripts/ci prepare`).

## Future Enhancements
- Adding new blog posts or updating project details.
- Tweaking CSS in `assets/` or layout overrides in `layouts/`.
- Implementing new shortcodes for richer content display.
