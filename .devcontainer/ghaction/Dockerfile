# Run from project root
# docker build -t ghcr.io/yogendra/yogendra-me-ghaction:latest -f .devcontainer/ghaction/Dockerfile .
FROM ghcr.io/yogendra/yogendra-me-devcontainer:latest

USER root
RUN mkdir /workspace && \
    useradd -m -u 1001 -s /bin/bash runner && \
    chown runner:runner /workspace && \
    echo "runner ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/runner && \
    chmod 0440 /etc/sudoers.d/runner

USER runner
WORKDIR /workspace

ADD Taskfile.yml Taskfile.yml

RUN task init