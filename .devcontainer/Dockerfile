ARG VARIANT="hirsute"

FROM mcr.microsoft.com/vscode/devcontainers/base:${VARIANT}
ARG TARGETPLATFORM

# [Optional] Uncomment this section to install additional OS packages.

# Install basic tools

RUN \
  git config --global user.name "Yogi Rampuria" &&\
  git config --global user.email "yogendrarampuria@gmail.com" &&\
  export DEBIAN_FRONTEND=noninteractive

RUN \
  apt-get update && \
  apt-get install -qqy --no-install-recommends wget apt-transport-https gnupg2 curl

# Install hugo
RUN \
  apt-get update && \
  apt-get install -qqy hugo

# Install asciidoctor
RUN \
  apt-get update && \
  apt-get install -qqy asciidoctor

# Install platuml
RUN  \
  apt-get update && \
  apt-get install -qqy default-jre graphviz  && \
  curl -sSL http://sourceforge.net/projects/plantuml/files/plantuml.jar/download -o lib/plantuml.jar


RUN if [ "$TARGETPLATFORM" = "linux/arm64" ]; then \
  apt-get update && \
  apt-get install -qqy  nodejs npm chromium-browser  && \
  npm install -g firebase-tools \
  elif [[ $TARGETPLATFORM == "linux/amd64" ]] ;\
  curl -sL https://firebase.tools | bash ;\
  fi

ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
