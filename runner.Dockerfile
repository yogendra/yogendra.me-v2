FROM ghcr.io/actions/actions-runner:latest

LABEL org.opencontainers.image.source="https://github.com/yogendra/yogendra.me-v2"
LABEL org.opencontainers.image.description="Self-hosted runner + build environment for yogendra.me"

ARG HUGO_VERSION=0.165.0
ARG DART_SASS_VERSION=1.97.3
ARG TASK_VERSION=3.38.0

ENV DEBIAN_FRONTEND=noninteractive

USER root

# System packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git sudo \
    asciidoctor graphviz pandoc \
    python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Python tools (syntax highlighting + RST support)
RUN pip3 install --no-cache-dir --break-system-packages pygments docutils

# Node.js 22.x + Wrangler (Cloudflare Pages CLI)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g wrangler

# Hugo extended
RUN curl -sSL \
    "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz" \
    | tar -C /usr/local/bin -xz hugo

# Dart Sass (installs sass + src/ snapshot into /usr/local/bin)
RUN curl -sSL \
    "https://github.com/sass/dart-sass/releases/download/${DART_SASS_VERSION}/dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz" \
    | tar -xz --strip-components=1 -C /usr/local/bin

# Task CLI
RUN curl -sSL https://taskfile.dev/install.sh | sh -s -- -d -b /usr/local/bin v${TASK_VERSION}

# Allow runner user to use sudo without password
RUN echo "runner ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER runner
WORKDIR /home/runner
