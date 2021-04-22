#!/usr/bin/env bash

set -eo pipefail

COLLECTIONS_PATH="$HOME/MyLabs/ansible/collections/"

DOCS_FOLDER=./docs/plugin_docs

export COLLECTIONS_PATH

mkdir -p $DOCS_FOLDER

antsibull-docs collection --use-current \
  -squash-hierarchy \
  --dest-dir $DOCS_FOLDER kamesampath.demos