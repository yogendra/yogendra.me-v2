---
name: Beta Testing Ticket
about: Coordinate beta testing for the latest changes.
title: 'Beta Release : {{ env.VERSION }}'
labels: beta-testing
assignees: yogendra
---

## Beta Site Details

- **URL:** [https://beta.yogendra.me](https://beta.yogendra.me)
- **Deployed At:** {{ env.DEPLOYED_AT }}
- **Commit:** {{ env.COMMIT_SHA }}
- **Baseline Tag:** [{{ env.BASELINE_TAG }}](https://github.com/yogendra/yogendra.me-v2/tree/{{ env.BASELINE_TAG }})
- **Author:** {{ env.AUTHOR }}
- **Action Run:** [View Logs]({{ env.ACTION_URL }})
- **Full Diff:** [Compare with Last Release]({{ env.DIFF_URL }})

### Build Info
```
{{ env.BUILD_INFO }}
```

### Changelog

```
{{ env.CHANGELOG }}
```

### Changed Files

```
{{ env.CHANGED_FILES }}
```

## Manual Testing Checklist
- [ ] Home page loads correctly
- [ ] New/Updated content is visible
- [ ] Navigation and search are functional
- [ ] No layout issues across devices


## Approval
Please comment `LGTM` or `APPROVED` to trigger the production release.
