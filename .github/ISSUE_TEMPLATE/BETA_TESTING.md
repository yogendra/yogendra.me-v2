---
name: Beta Testing Ticket
about: Coordinate beta testing for the latest changes.
title: 'Beta Release: [VERSION]'
labels: beta-testing
assignees: yogendra
---

## Beta Site Details
- **URL:** [https://beta.yogendra.me](https://beta.yogendra.me)
- **Deployed At:** ${{ github.event.head_commit.timestamp }}
- **Commit:** ${{ github.sha }}

## Changelog
<!-- changelog_start -->
[Automatically filled by GitHub Action]
<!-- changelog_end -->

## Approval
Please comment `LGTM` or `APPROVED` to trigger the production release.
