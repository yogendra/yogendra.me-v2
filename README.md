# Yogendra.Me

[![Build Site](https://github.com/yogendra/yogendra.me-v2/actions/workflows/publish.yml/badge.svg)](https://github.com/yogendra/yogendra.me-v2/actions/workflows/publish.yml)
|
[![Build Devcontainer](https://github.com/yogendra/yogendra.me-v2/actions/workflows/publish-devcontainer.yml/badge.svg)](https://github.com/yogendra/yogendra.me-v2/actions/workflows/publish-devcontainer.yml)

## Quickstart

```bash
git clone --recurse-submodules git@github.com:yogendra/yogendra.me-v2.git yogendra.me
cd yogendra.me
direnv allow
scripts/init
script/ci prepare
hugo serve
```

| Action            | Command                  |
| ----------------- | ------------------------ |
| Plant UML Prepare | `scripts/ci prepare`     |
| Run local         | `hugo -e local`          |
| Deploy to Beta    | `scripts/ci deploy-beta` |
| Deploy            | `scrtips/ci deploy`      |

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
scripts/ci devcontainer-build
```
