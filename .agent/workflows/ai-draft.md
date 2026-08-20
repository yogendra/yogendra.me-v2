---
description: Interactive workflow to research, outline, and draft a technical blog post with AI
---

Use this workflow to turn an idea or topic into a complete technical blog post:

1. **Scaffold the Post**:
```bash
task post:create -- "Your Article Title"
```

2. **Formulate the Content Brief**:
   - What is the specific question or topic?
   - Target audience (Beginner / Intermediate / Advanced).
   - What diagrams are needed? (Architecture, Sequence, Flowchart).

3. **Draft the Article**:
   - Fill in frontmatter (`title`, `description`, `tags`, `categories`, `series`).
   - Add Mermaid diagrams with ```mermaid code blocks.
   - Include copy-pasteable configuration and CLI commands.

4. **Verify on Homelab Staging**:
   - Open `https://blog.hs.yogendra.me` to review the live draft.

5. **Publish**:
   - Set `draft: false` in frontmatter.
   - Commit & push to `main` branch to trigger GitHub Actions deployment.
