
PYTHON := python3

.DEFAULT_GOAL := test

test:
	$(PYTHON) chapter1.py
	$(PYTHON) chapter2.py

run\:%: \
	practice=practice$(shell echo $@ | sed -E 's/[^0-9]+//g')
	chapter=chapter$(shell expr `echo $@ | sed -E 's/^[^0-9]+|[0-9][^0-9]*$$//g'` + 1)

run\:%.sh:
	@(source $(chapter).sh && $(practice))

run\:%:
	@$(PYTHON) -B -c 'import $(chapter); $(chapter).$(practice)()'

