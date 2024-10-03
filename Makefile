install:
	poetry install

build:
	./build.sh

publish:
	poetry publish --dry-run

lint:
	poetry run flake8 task_manager

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

shell:
	poetry run python manage.py shell_plus --ipython

selfcheck:
	poetry check

check: selfcheck test-coverage lint

dev:
	poetry run python manage.py runserver

test-coverage:
	poetry run coverage run manage.py test && poetry run coverage xml
