ARG VARIANT="hirsute"
ARG HUGO_VERSION="0.95.0"

FROM golang:latest as hugobuild
ARG HUGO_VERSION

RUN \
  apt-get update && \
  apt-get install -qqy build-essential && \
  mkdir -p $HOME/src && \
  cd $HOME/src && \
  git clone --depth 1 --branch v${HUGO_VERSION} https://github.com/gohugoio/hugo.git &&  \
  cd hugo && \
  go mod download github.com/yuin/goldmark && \
  go get github.com/gohugoio/hugo/common/herrors && \
  go install --tags extended





FROM mcr.microsoft.com/vscode/devcontainers/base:${VARIANT}
ARG TARGETPLATFORM

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
  apt-get update && \
  apt-get install -qqy --no-install-recommends wget apt-transport-https gnupg2 curl direnv fzf  xclip

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



# Install hugo

COPY --from=hugobuild /go/bin/hugo /usr/local/bin
# RUN \
#   apt-get update && \
#   apt-get install -qqy hugo



# Install asciidoctor, pandoc and docutils (rst)
RUN \
  apt-get update && \
  apt-get install -qqy asciidoctor pandoc python-docutils

# Install plantuml
RUN  \
  apt-get update && \
  apt-get install -qqy default-jre graphviz  && \
  curl -sSL http://sourceforge.net/projects/plantuml/files/plantuml.jar/download -o lib/plantuml.jar


RUN if [ "$TARGETPLATFORM" = "linux/arm64" ]; then \
  apt-get update && \
  apt-get install -qqy  nodejs npm chromium-browser  && \
  npm install -g firebase-tools ;\
  elif [ "$TARGETPLATFORM" = "linux/amd64" ] ; then \
  curl -sL https://firebase.tools | bash ;\
  fi

ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
