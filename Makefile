install:
	poetry install

build:
	./build.sh

publish:
	poetry publish --dry-run

lint:
	poetry run flake8 task_manager