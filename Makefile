test:
	py.test --cov-report term-missing --cov-report html --cov inflow

doc:
	python setup.py build_sphinx

upload:
	python setup.py sdist bdist_wheel --universal upload
