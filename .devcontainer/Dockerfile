# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.194.0/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version: bionic, focal
ARG VARIANT="focal"
FROM mcr.microsoft.com/vscode/devcontainers/base:dev-${VARIANT}

# [Optional] Uncomment this section to install additional OS packages.
RUN \
  export DEBIAN_FRONTEND=noninteractive && \
  apt-get update && \
  apt-get -y install --no-install-recommends wget apt-transport-https gnupg2

RUN \
  wget -qO- https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public  | apt-key add - && \
  echo "deb https://adoptopenjdk.jfrog.io/adoptopenjdk/deb focal main" > /etc/apt/sources.list.d/adoptopenjdk.list && \
  apt-get update && \
  apt-get install -y adoptopenjdk-11-hotspot-jre graphviz && \
  curl -sSL http://sourceforge.net/projects/plantuml/files/plantuml.jar/download -o lib/plantuml.jar

RUN \
  curl -sSL firebase.tools | bash
RUN \
  sudo apt-get install -y asciidoctor

RUN \
  curl -sSL https://github.com/gohugoio/hugo/releases/download/v0.92.0/hugo_0.92.0_Linux-ARM64.tar.gz | tar -C /usr/local/bin -xzvf- hugo

RUN \
  git config --global user.name "Yogi Rampuria" ;\
  git config --global user.email "yogendrarampuria@gmail.com"

# ADD entrypoint.sh /entrypoint.sh

# ENTRYPOINT ["/entrypoint.sh"]
