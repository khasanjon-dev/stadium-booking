del:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -delete
	rm -rf stadium.sqlite3
make:
	python3 manage.py makemigrations
mig:
	python3 manage.py migrate
add:
	poetry export --without-hashes --format=requirements.txt > requirements.txt
create:
	python3 manage.py createsuperuser
