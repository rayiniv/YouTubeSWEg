.DEFAULT_GOAL := pylint

FILES :=                              \
    frontend/main.py                  \
    app/appengine_config.py       \
    app/db_create.py              \
    app/db_insert                 \
    app/tests.py                  

ifeq ($(shell uname), Darwin)          # Apple
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else ifeq ($(CI), true)                # Travis CI
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Docker
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else                                   # UTCS
    PYTHON   := python3
    PIP      := pip3
    PYLINT   := pylint3
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
endif

.pylintrc:
	$(PYLINT) --disable=locally-disabled --reports=no --generate-rcfile > $@

IDB1.log:
	git log > IDB1.log

IDB1.html: app/models.py
	pydoc3 -w app/models.py
	mv models.html IDB1.html	

pylint: .pylintrc
	-$(PYLINT) app/models.py

format:
	$(AUTOPEP8) -i app/models.py

config:
	git config -l

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

versions:
	which make
	make --version
	@echo
	which git
	git --version
	@echo
	which $(PYTHON)
	$(PYTHON) --version
	@echo
	which $(PIP)
	$(PIP) --version
	@echo
	which $(PYLINT)
	$(PYLINT) --version
	@echo
	which $(COVERAGE)
	$(COVERAGE) --version
	@echo
	-which $(PYDOC)
	-$(PYDOC) --version
	@echo
	which $(AUTOPEP8)
	$(AUTOPEP8) --version
	@echo
	$(PIP) list

test: app/models.py
    $(COVERAGE) run    --branch app/models.py >  app/tests.out 2>&1
    $(COVERAGE) report -m                      >> app/tests.out
    cat app/tests.out
