test:
	venv/bin/python test_project/manage.py test test_project/ -v 2

pep8:
	pep8 --exclude=*migrations* --max-line-length=119 --show-source django_typograf/
	pep8 --exclude=*migrations* --max-line-length=119 --show-source test_project/

pyflakes:
	pylama --skip=*migrations* -l pyflakes django_typograf/
	pylama --skip=*migrations* -l pyflakes test_project/

lint:
	make pep8
	make pyflakes

ci_test:
	python test_project/manage.py test test_project/ -v 2
	make lint
