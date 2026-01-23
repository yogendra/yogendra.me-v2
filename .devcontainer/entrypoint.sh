#!/bin/bash

set -e

Check if running in GitHub vs locally
if [ -n "$GITHUB_ACTIONS" ]
then
  echo "** Running github action script **"
  echo task init
  echo task release:publish
  echo "** **"
elif [ $# -gt 0 ]; then
  exec "$@"
else
  tail -f /dev/null
fi