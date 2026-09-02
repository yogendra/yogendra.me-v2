FROM lscr.io/linuxserver/code-server:latest

LABEL org.opencontainers.image.source="https://github.com/yogendra/yogendra.me-v2"
LABEL org.opencontainers.image.description="VS Code in browser for yogendra.me blogging"

ENV DEBIAN_FRONTEND=noninteractive
ENV HOME="/root"
ENV PATH="/root/miniconda/bin:/root/miniconda/envs/yogendra-me/bin:/app/code-server/bin:/usr/local/bin:$PATH"

# 1. Base tools, git safe directory, and passwordless sudo for abc user
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl git sudo \
    && rm -rf /var/lib/apt/lists/* \
    && echo "abc ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/abc \
    && chmod 0440 /etc/sudoers.d/abc \
    && git config --system --add safe.directory /workspace

# 2. Install Task CLI
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin v3.38.0

# 3. Use Taskfile & Taskinit.yml as the SINGLE source of truth
WORKDIR /tmp/setup
COPY Taskfile.yml Taskinit.yml environment.yml ./
RUN task init && \
    npm install -g wrangler && \
    rm -rf /tmp/setup /var/lib/apt/lists/*

# 4. Pre-install VS Code extensions for blogging
RUN mkdir -p /config /app/code-server/extensions && \
    chown -R abc:abc /config /app/code-server/extensions

USER abc
ENV HOME="/config"
RUN /app/code-server/bin/code-server --extensions-dir /app/code-server/extensions --user-data-dir /config/data --install-extension yzhang.markdown-all-in-one \
    && /app/code-server/bin/code-server --extensions-dir /app/code-server/extensions --user-data-dir /config/data --install-extension bpruitt-goddard.mermaid-markdown-syntax-highlighting \
    && /app/code-server/bin/code-server --extensions-dir /app/code-server/extensions --user-data-dir /config/data --install-extension bierner.markdown-preview-github-styles \
    && /app/code-server/bin/code-server --extensions-dir /app/code-server/extensions --user-data-dir /config/data --install-extension streetsidesoftware.code-spell-checker \
    && /app/code-server/bin/code-server --extensions-dir /app/code-server/extensions --user-data-dir /config/data --install-extension timonwong.shellcheck

USER root
WORKDIR /workspace
