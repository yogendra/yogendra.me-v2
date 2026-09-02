# syntax=docker/dockerfile:1
# ---------------------------------------------------------------------------
# Stage 1: Tool installer
#   Use a throwaway Ubuntu stage to download/install all build tools so we
#   can COPY --from them into the final runner image cleanly, without
#   polluting it with curl, apt caches, or intermediate files.
# ---------------------------------------------------------------------------
FROM ubuntu:24.04 AS tool-builder

ENV DEBIAN_FRONTEND=noninteractive
ARG HUGO_VERSION=0.165.0
ARG DART_SASS_VERSION=1.97.3
ARG TASK_VERSION=3.38.0

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl tar gzip \
    && rm -rf /var/lib/apt/lists/*

# Hugo extended (amd64)
RUN curl -sSL \
    "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz" \
    | tar -C /usr/local/bin -xz hugo

# Dart Sass (amd64)
RUN curl -sSL \
    "https://github.com/sass/dart-sass/releases/download/${DART_SASS_VERSION}/dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz" \
    | tar -xz --strip-components=1 -C /usr/local/bin

# Task CLI
RUN curl -sSL https://taskfile.dev/install.sh | sh -s -- -d -b /usr/local/bin v${TASK_VERSION}

# ---------------------------------------------------------------------------
# Stage 2: Final runner image
#   Based on the official GitHub Actions runner so it works as a self-hosted
#   runner with no job container needed (no container: block in workflow).
#   All build tools are COPY'd in from stage 1.
# ---------------------------------------------------------------------------
FROM ghcr.io/actions/actions-runner:latest

LABEL org.opencontainers.image.source="https://github.com/yogendra/yogendra.me-v2"
LABEL org.opencontainers.image.description="Self-hosted runner + build environment for yogendra.me"

USER root

ENV DEBIAN_FRONTEND=noninteractive

# System packages needed for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git sudo \
    asciidoctor graphviz pandoc \
    python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Python tools (Pygments for syntax highlighting, rst2html for RST content)
RUN pip3 install --no-cache-dir --break-system-packages pygments docutils

# Node.js 22.x (for wrangler / npm)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Wrangler (Cloudflare Pages CLI)
RUN npm install -g wrangler

# COPY tools from stage 1
COPY --from=tool-builder /usr/local/bin/hugo   /usr/local/bin/hugo
COPY --from=tool-builder /usr/local/bin/sass   /usr/local/bin/sass
COPY --from=tool-builder /usr/local/bin/src    /usr/local/bin/src
COPY --from=tool-builder /usr/local/bin/task   /usr/local/bin/task

# Allow runner user to run sudo without password (needed for some CI steps)
RUN echo "runner ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER runner
WORKDIR /home/runner
