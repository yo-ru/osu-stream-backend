shell:
	pipenv shell

lint:
	pipenv run pre-commit run --all-files

install:
	PIPENV_VENV_IN_PROJECT=1 pipenv install

install-dev:
	PIPENV_VENV_IN_PROJECT=1 pipenv install --dev

uninstall:
	pipenv --rm

update:
	pipenv update --dev
	pipenv requirements > requirements.txt
	pipenv requirements --dev > requirements-dev.txt

run:
	pipenv run python main.py

clean:
	pipenv clean
