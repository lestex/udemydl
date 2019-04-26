.PHONY: default

default: test

shell:
	pipenv --python 3.6.4
	pipenv shell

install:
	pipenv install --dev --skip-lock

test:
	PYTHONPATH=./src pytest

b:
	python setup.py sdist bdist_wheel

i:
	pip install dist/udemydl-0.1.0-py3-none-any.whl

u:
	pip uninstall -y udemydl

clean:
	@rm -rf build dist udemy_dl.egg-info .pytest_cache

upload:
	twine upload  dist/*

all:	u b i
