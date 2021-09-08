# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.194.0/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version: bionic, focal
ARG VARIANT="focal"
FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}

# [Optional] Uncomment this section to install additional OS packages.
RUN \
  export DEBIAN_FRONTEND=noninteractive && \
  apt-get update && \
  apt-get -y install --no-install-recommends wget apt-transport-https gnupg

RUN \
  wget -qO- https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public  | apt-key add - && \
  echo "deb https://adoptopenjdk.jfrog.io/adoptopenjdk/deb focal main" > /etc/apt/sources.list.d/adoptopenjdk.list && \
  apt-get update && \
  apt-get install -y adoptopenjdk-11-hotspot-jre graphviz && \
  curl -sSL http://sourceforge.net/projects/plantuml/files/plantuml.jar/download -o lib/plantuml.jar

RUN \
  curl -sSL firebase.tools | bash

RUN \
  curl -sSL https://github.com/gohugoio/hugo/releases/download/v0.88.1/hugo_extended_0.88.1_Linux-64bit.tar.gz | tar -C /usr/local/bin -xzvf- hugo

ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
