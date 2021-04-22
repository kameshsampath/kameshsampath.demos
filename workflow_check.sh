#!/usr/bin/env bash

set -eo pipefail

SECRETS_ENV=~/.ssh/gh_act_env
GH_ACTOR=kameshsampath
EVENT=${1:-push}

act --secret-file $SECRETS_ENV \
  --actor "$GH_ACTOR" "$EVENT"
