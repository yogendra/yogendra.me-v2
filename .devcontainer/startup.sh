#!/usr/bin/env bash

set -Eeuo pipefail
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_DIR=$( cd ${SCRIPT_DIR}/.. ; pwd)

direnv allow 

hugo -DFE  --cleanDestinationDir -e local serve
echo "Hugo started"
