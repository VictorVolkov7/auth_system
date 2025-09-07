# target: migrate - Make migrations for the application and apply them
migrate:
	python3 manage.py makemigrations $(APP) && python3 manage.py migrate

# target: run - Run development server on 0.0.0.0:8000
run:
	python3 manage.py runserver 0.0.0.0:8000

# target: pep8 - Run code style test
pep8:
	flake8 --statistics --count

# target: qa - Run tests
qa:
	pytest

# target: coverage - See test coverage in project
coverage:
	pytest --cov=.

# target: translate - Generate translations to russian locale
translate:
	python manage.py makemessages --locale=ru --ignore=venv/* --ignore=volumes/*

# target: compile-mes - Compile translated messages with previous command to russian locale
compile-mes:
	python manage.py compilemessages --locale=ru

# target: superuser - Create super user
superuser:
	python manage.py createsuperuser

# target: loaddata - load initial fixtures
loaddata:
	python manage.py loaddata auth_system/fixtures/initial_data.json