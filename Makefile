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
	pip install dist/udemydl-*-py3-none-any.whl

u:
	pip uninstall -y udemydl

clean:
	@rm -rf build dist *.egg-info .pytest_cache

upload:
	twine upload  dist/*

all:	u b i
