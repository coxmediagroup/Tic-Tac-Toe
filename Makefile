.PHONY: unit

unit:
	nosetests --tests tests/ --verbosity=3

unit-debug:
	nosetests --tests tests/ --verbosity=3 -s
