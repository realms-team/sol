.PHONY: docs
init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock

test:
	# This runs all of the tests, on both Python 2 and Python 3.
	pytest

publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg sensorobjectlibrary.egg-info

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"
