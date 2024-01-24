test:
	py.test --cov-report term-missing --cov-report html --cov inflow

doc:
	python setup.py build_sphinx

build:
	python setup.py sdist bdist_wheel

upload: build
	python -m twine upload dist/*
