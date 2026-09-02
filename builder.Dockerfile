FROM ubuntu:24.04

LABEL org.opencontainers.image.source="https://github.com/yogendra/yogendra.me-v2"
LABEL org.opencontainers.image.description="Pre-baked build environment for yogendra.me Hugo blog"

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/root/miniconda/bin:/root/miniconda/envs/yogendra-me/bin:/usr/local/bin:$PATH"

# 1. Install base curl, sudo, git, ca-certificates so Task CLI and Taskfile can run
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git sudo \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Task CLI
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin v3.38.0

# 3. Copy only Taskfile, Taskinit.yml, and environment.yml to build environment
WORKDIR /tmp/setup
COPY Taskfile.yml Taskinit.yml environment.yml ./

# 4. Run task init to install all tools (os-packages, conda, python-env, hugo, dart-sass, go, nodejs)
RUN task init && \
    npm install -g wrangler && \
    rm -rf /tmp/setup /var/lib/apt/lists/*

WORKDIR /workspace

CMD ["task", "build"]
