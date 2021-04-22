#!/usr/bin/env bash

set -eo pipefail

export ACT=true
SECRETS_ENV=./hacking/gh_act_env
GH_ACTOR=kameshsampath
EVENT=${1:-release}

act --secret-file $SECRETS_ENV \
  --eventpath=hacking/event-v0.1.3.json \
  --actor "$GH_ACTOR" "$EVENT"
