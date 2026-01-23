ARG VARIANT="jammy"

# Stage 1: Base - System-level tools and configuration
FROM mcr.microsoft.com/vscode/devcontainers/base:${VARIANT} AS base

USER root

# Install system-level tools
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -qqy --no-install-recommends \
        wget \
        apt-transport-https \
        gnupg2 \
        curl \
        direnv \
        fzf \
        xclip \
        python3 \
        python3-pip \
        sudo \
    && sh -c "$(curl -fsSL https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin \
    && sh -c "$(curl -fsSL https://starship.rs/install.sh)" -- -y \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# System-level configuration
RUN \
  git config --global user.name "Yogi Rampuria" && \
  git config --global user.email "yogendrarampuria@gmail.com" && \
  echo 'eval "$(direnv hook bash)"' >> /home/vscode/.bash_profile && \
  echo 'eval "$(starship init bash)"' >> /home/vscode/.bash_profile && \
  echo 'source /usr/share/doc/fzf/examples/completion.bash' >> /home/vscode/.bash_profile && \
  echo 'source /usr/share/doc/fzf/examples/key-bindings.bash' >> /home/vscode/.bash_profile && \
  mkdir -p /home/vscode/.config && \
  curl -sSL https://raw.githubusercontent.com/yogendra/dotfiles/master/.config/starship.toml -o /home/vscode/.config/starship.toml && \
  chown -R vscode:vscode /home/vscode/.bash_profile /home/vscode/.config

# Stage 2: Developer - Final image for development
FROM base AS developer

LABEL org.opencontainers.image.description="Dev-container for Yogendra.Me Development"
LABEL org.opencontainers.image.source="https://github.com/yogendra/yogendra.me-v2/blob/main/.devcontainer/Dockerfile"
LABEL org.opencontainers.image.vendor="Yogi Rampuria (@yogendra)"
LABEL org.opencontainers.image.title="Yogendra.Me Dev-container"

USER vscode

ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
