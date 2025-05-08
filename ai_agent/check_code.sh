#!/bin/bash
# Simple script to run Ruff linting on the project

# Make sure we're in the project root
cd "$(dirname "$0")"

echo "Running Ruff linting checks..."
uv run ruff check .

echo "Running Ruff formatting checks..."
uv run ruff format --check .

# Return success if we get here
exit 0 