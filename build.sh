#!/usr/bin/env bash
set -o errexit

curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

uv sync --frozen
cd $(dirname $(find . | grep manage.py$))
uv run python manage.py collectstatic --no-input
uv run python manage.py migrate
