#!/bin/bash
# Script to automatically fix common linting issues with Ruff

# Make sure we're in the project root
cd "$(dirname "$0")"

echo "Auto-fixing linting issues with Ruff..."
uv run ruff check --fix .

echo "Auto-formatting code with Ruff..."
uv run ruff format .

echo "Done!"
exit 0 