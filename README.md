# Yogendra.Me

[![Site Release](https://github.com/yogendra/yogendra.me-v2/actions/workflows/release.yml/badge.svg)](https://github.com/yogendra/yogendra.me-v2/actions/workflows/release.yml)
|
[![Beta Deploy](https://github.com/yogendra/yogendra.me-v2/actions/workflows/beta.yml/badge.svg)](https://github.com/yogendra/yogendra.me-v2/actions/workflows/beta.yml)

* [Beta Site](https://beta.yogendra.me)
* [Production Site](https://yogendra.me)
* [Beta Testing Ticket](https://github.com/yogendra/yogendra.me-v2/issues?q=is%3Aissue%20state%3Aopen%20label%3Abeta-testing)

## Quickstart

```bash
git clone --recurse-submodules git@github.com:yogendra/yogendra.me-v2.git yogendra.me
cd yogendra.me
direnv allow
task init
task run
```

| Action            | Command               |
| ----------------- | --------------------- |
| Initialize        | `task init`           |
| Run local         | `task run`      |
| Deploy to Beta    | `task beta:deploy`    |
| Deploy            | `task release:deploy` |

## Local

### Local Pre-requisites

- Git
- VS Code
- Hugo
- Firebase cli

## Local Workstation with VS Code + Devcontainer

### Devcontainer Pre-requisites

- Docker for Windows / Mac
- VS Code
  - Extension: Remote Cotainer
  - Install local devcontainer cli

```bash
devcontainer open
```

### Build devcontainer

```bash
task dev-container:build
```
