#!/bin/bash

SCRIPT_PATH="$(realpath "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
PROJECT_ROOT="$(realpath "$SCRIPT_DIR/..")"

cd "${PROJECT_ROOT}/src"
make distclean
rm -rf "./build/"
rm -rf "./nanobanana-output/"
rm -rf "./sections/"
rm -f "./presentation.tex"
find "./img" ! -name 'dog.png' -type f -exec rm -f {} +

