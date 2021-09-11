# Yogendra.Me

![Build and Deploy](https://github.com/yogendra/yogendra.me-v2/actions/workflows/merge.yml/badge.svg)

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
- Java
- Graphviz
- Platuml

## Local Workstation with VS Code + Devcontainer

### Devcontainer Pre-requisites

- Docker for Windows / Mac
- VS Code
  - Extension: Remote Cotainer
  - Install local devcontainer cli

```bash
devcontainer open
```
