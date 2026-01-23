# Yogendra.Me

[![Build Site](https://github.com/yogendra/yogendra.me-v2/actions/workflows/publish.yml/badge.svg)](https://github.com/yogendra/yogendra.me-v2/actions/workflows/publish.yml)
|
[![Build Devcontainer](https://github.com/yogendra/yogendra.me-v2/actions/workflows/publish-devcontainer.yml/badge.svg)](https://github.com/yogendra/yogendra.me-v2/actions/workflows/publish-devcontainer.yml)

## Quickstart

```bash
git clone --recurse-submodules git@github.com:yogendra/yogendra.me-v2.git yogendra.me
cd yogendra.me
direnv allow
task init
task local:run
```

| Action            | Command               |
| ----------------- | --------------------- |
| Initialize        | `task init`           |
| Run local         | `task local:run`      |
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
