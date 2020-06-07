#!/bin/bash

source ./setup.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE:-$0}")" > /dev/null; pwd)"

${SCRIPT_DIR}/install_conda_modules.sh
${SCRIPT_DIR}/install_flac.sh
${SCRIPT_DIR}/install_libsnd.sh
