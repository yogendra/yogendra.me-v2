# Run from project root
# docker build -t ghcr.io/yogendra/yogendra-me-ghaction:latest -f .devcontainer/ghaction/Dockerfile .
FROM ghcr.io/yogendra/yogendra-me-devcontainer:latest

USER root
RUN mkdir /workspace && \
    useradd -m -u 1001 -s /bin/bash gha && \
    chown gha:gha /workspace && \
    echo "gha ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/gha && \
    chmod 0440 /etc/sudoers.d/gha

USER gha
WORKDIR /workspace

ADD Taskfile.yml Taskfile.yml

RUN task init