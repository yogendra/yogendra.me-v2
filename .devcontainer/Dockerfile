ARG VARIANT="jammy"
ARG HUGO_VERSION="0.125.4"

FROM mcr.microsoft.com/vscode/devcontainers/base:${VARIANT}
ARG TARGETPLATFORM
ARG HUGO_VERSION

LABEL org.opencontainers.image.description Dev-container for Yogendra.Me Development
LABEL org.opencontainers.image.source  https://github.com/yogendra/yogendra.me-v2/blob/main/.devcontainer/Dockerfile
LABEL org.opencontainers.image.vendor Yogi Rampuria (@yogendra)
LABEL org.opencontainers.image.title Yogendra.Me Dev-container

# Install basic tools

RUN \
  git config --global user.name "Yogi Rampuria" && \
  git config --global user.email "yogendrarampuria@gmail.com" && \
  export DEBIAN_FRONTEND=noninteractive


RUN \
  set -e \
  && apt-get update \
  && apt-get install -qqy wget apt-transport-https gnupg2 curl direnv fzf  xclip  asciidoctor pandoc python3-docutils python3 python3-pip python-is-python3 sudo \
  && apt-get autoremove \
  && apt-get autoclean \
  && apt-get clean \
  && pip3 install rst2html

RUN \
  echo 'eval "$(direnv hook bash)"' >> /home/vscode/.bash_profile && \
  sh -c "$(curl -fsSL https://starship.rs/install.sh)" -- -y && \
  echo 'eval "$(starship init bash)"' >> /home/vscode/.bash_profile && \
  echo 'source /usr/share/doc/fzf/examples/completion.bash' >> /home/vscode/.bash_profile && \
  echo 'source /usr/share/doc/fzf/examples/key-bindings.bash' >> /home/vscode/.bash_profile && \
  chown -R vscode:vscode /home/vscode/.bash_profile && \
  mkdir -p /home/vscode/.config && \
  chown -R vscode:vscode /home/vscode/.config && \
  curl -sSL https://raw.githubusercontent.com/yogendra/dotfiles/master/.config/starship.toml -o /home/vscode/.config/starship.toml

RUN \
  set -e \
  && HUGO_RELEASE=https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz \
  && if [ "$TARGETPLATFORM" = "linux/arm64" ]; then \
      HUGO_RELEASE=https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-arm64.tar.gz; \
  fi \
  && wget -qO- $HUGO_RELEASE | tar -C /usr/local/bin -xz hugo

RUN \
  set -e ;\
  if [ "$TARGETPLATFORM" = "linux/arm64" ]; then apt-get install -qqy npm ; npm install -g firebase-tools ;\
  else curl -sL https://firebase.tools | bash ;\
  fi


ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
