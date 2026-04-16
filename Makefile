install:
	uv sync --dev

migrate:
	uv run python manage.py migrate

start:
	uv run python manage.py runserver

build:
	./build.sh