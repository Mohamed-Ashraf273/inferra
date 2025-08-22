#!/bin/bash
set -Eeuo pipefail

# Get the repo root directory (two levels up from this script)
base_dir=$(dirname $(dirname "$0"))

if ! command -v pre-commit >/dev/null 2>&1
then
    echo 'Please `pip install pre-commit` to run api_gen.sh.'
    exit 1
fi

# Run generate_init.py script first (relative to repo root)
echo "Generating __init__.py files..."
python3 "${base_dir}/tools/generate_init.py"

# Format code because generate_init.py might reorder imports
echo "Formatting api directory..."
(SKIP=api-gen pre-commit run --files $(find "${base_dir}"/inferra/api -type f) --hook-stage pre-commit || true) > /dev/null
