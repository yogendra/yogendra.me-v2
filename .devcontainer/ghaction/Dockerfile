# Run from project root
# docker build -t ghcr.io/yogendra/yogendra-me-ghaction:latest -f .devcontainer/ghaction/Dockerfile .
FROM ghcr.io/yogendra/yogendra-me-devcontainer:latest
ADD Taskfile.yml Taskfile.yml

USER root
RUN mkdir /workspace
WORKDIR /workspace

RUN task init