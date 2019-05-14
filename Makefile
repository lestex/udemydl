.PHONY: help env install test b i u clean upload all
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

env: ## init virtual env
	pipenv --python 3.7.3
	pipenv shell

install: ## install dependencies
	pipenv install --dev --skip-lock

test: ## run tests
	PYTHONPATH=./src pytest

b: ## generate package
	python setup.py sdist bdist_wheel

i: ## install package from dist 
	pip install dist/udemydl-*-py3-none-any.whl

u: ## uninstall package
	pip uninstall -y udemydl

clean: ## clean directories
	@rm -rf build dist *.egg-info .pytest_cache

upload: ## upload package to pypi pypi.org
	twine upload  dist/*

all:	u b i  ## run all
