---
name: Beta Testing Ticket
about: Coordinate beta testing for the latest changes.
title: 'Beta Release: [VERSION]'
labels: beta-testing
assignees: yogendra
---

## Beta Site Details
- **URL:** [https://beta.yogendra.me](https://beta.yogendra.me)
- **Deployed At:** {{ .DEPLOYED_AT }}
- **Commit:** {{ .COMMIT_SHA }}
- **Baseline Tag:** [{{ .BASELINE_TAG }}](https://github.com/yogendra/yogendra.me-v2/tree/{{ .BASELINE_TAG }})
- **Author:** {{ .AUTHOR }}
- **Action Run:** [View Logs]({{ .ACTION_URL }})
- **Full Diff:** [Compare with Last Release]({{ .DIFF_URL }})
- **Build Info:** {{ .BUILD_INFO }}

## Manual Testing Checklist
- [ ] Home page loads correctly
- [ ] New/Updated content is visible
- [ ] Navigation and search are functional
- [ ] No layout issues across devices

## Changelog
{{ .CHANGELOG }}

## Changed Files
```
{{ .CHANGED_FILES }}
```

## Approval
Please comment `LGTM` or `APPROVED` to trigger the production release.
