.DEFAULT_GOAL := pylint

FILES :=                              \
    frontend/main.py                  \
    backend/appengine_config.py       \
    backend/db_create.py              \
    backend/db_insert                 \
    backend/tests.py                  

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

YouTubeSWEg.log:
	git log > YouTubeSWEg.log

pylint: .pylintrc
	-$(PYLINT) frontend/main.py
	-$(PYLINT) frontend/appengine_config.py
	-$(PYLINT) backend/db_create.py
	-$(PYLINT) backend/db_insert.py
	-$(PYLINT) backend/tests.py  

format:
	$(AUTOPEP8) -i frontend/main.py
	$(AUTOPEP8) -i frontend/appengine_config.py
	$(AUTOPEP8) -i backend/db_create.py
	$(AUTOPEP8) -i backend/db_insert.py
	$(AUTOPEP8) -i backend/tests.py  

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