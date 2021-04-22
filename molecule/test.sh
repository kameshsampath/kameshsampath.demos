#!/usr/bin/env bash

set -eo pipefail

SCENARIO_NAME=${1:-default}

molecule create -s ${SCENARIO_NAME} || true

molecule test -s ${SCENARIO_NAME}
