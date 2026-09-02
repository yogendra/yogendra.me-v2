FROM lscr.io/linuxserver/code-server:latest

LABEL org.opencontainers.image.source="https://github.com/yogendra/yogendra.me-v2"
LABEL org.opencontainers.image.description="VS Code in browser for yogendra.me blogging"

# Allow abc user passwordless sudo for local dev flexibility
RUN echo "abc ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/abc && \
    chmod 0440 /etc/sudoers.d/abc

# Install Hugo, Git, Task, Node, Python tools, and blog dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    sudo \
    build-essential \
    ruby-asciidoctor \
    asciidoctor \
    graphviz \
    pandoc \
    python3 \
    python3-pip \
    python3-setuptools \
    && rm -rf /var/lib/apt/lists/*

# Install Task CLI
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin v3.38.0

# Install Hugo Extended & Dart Sass
RUN curl -sSL "https://github.com/gohugoio/hugo/releases/download/v0.165.0/hugo_extended_0.165.0_linux-amd64.tar.gz" | \
    tar -C /usr/local/bin -xz hugo && \
    curl -sLJ "https://github.com/sass/dart-sass/releases/download/1.97.3/dart-sass-1.97.3-linux-x64.tar.gz" | \
    tar -xz --strip-components=1 -C /usr/local/bin

# Install Python tools
RUN pip3 install --no-cache-dir --break-system-packages docutils pygments rst2html

# Ensure git safe directory for mounted repo
RUN git config --system --add safe.directory /workspace

# Pre-install useful VS Code extensions for Markdown, Hugo, Mermaid, and Spellcheck
USER abc
RUN code-server --install-extension yzhang.markdown-all-in-one || true \
    && code-server --install-extension bpruitt-goddard.mermaid-markdown-syntax-highlighting || true \
    && code-server --install-extension bierner.markdown-preview-github-styles || true \
    && code-server --install-extension streetsidesoftware.code-spell-checker || true \
    && code-server --install-extension timonwong.shellcheck || true

USER root
WORKDIR /workspace
