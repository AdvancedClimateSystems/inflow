test:
	py.test --cov-report term-missing --cov-report html --cov inflow

doc:
	python setup.py build_sphinx
