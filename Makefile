shell:
	pipenv shell

lint:
	pipenv run pre-commit run --all-files

install:
	pipenv install

install-dev:
	pipenv install --dev

uninstall:
	pipenv --rm

update:
	pipenv update --dev
	pipenv requirements > requirements.txt
	pipenv requirements --dev > requirements-dev.txt

run:
	pipenv run python3.12 main.py

clean:
	pipenv clean