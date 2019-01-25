.PHONY: default

default: test

install:
	pipenv install --dev --skip-lock

test:
	PYTHONPATH=./src pytest

b:
	python setup.py sdist bdist_wheel

i:
	pip install dist/udemy_dl-0.1.0-py3-none-any.whl

u:
	pip uninstall -y udemy-dl

clean:
	@rm -rf build dist udemy_dl.egg-info

all:	u b a
