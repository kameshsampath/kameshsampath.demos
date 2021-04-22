CURRENT_DIR = $(shell pwd)

COLLECTION_FQN=kameshsampath.demos
MODULE_DOCS_FOLDER=$(CURRENT_DIR)/source/modules
MODULES := $(wildcard ../plugins/modules/*.py)
MODULES_RSTS:= $(wildcard ./source/modules/*.rst)
MODULE_DOCS := $(MODULES:../plugins/modules/%.py=source/modules/%.rst)
template := $(CURRENT_DIR)/source/_templates/module.rst.j2

export ANSIBLE_COLLECTIONS_PATH ?= $(realpath $(CURRENT_DIR))/collections
export GITHUB_WORKSPACE ?= $(realpath $(CURRENT_DIR)/..)/.git

.PHONY:	all
all:	clean create-docs-tree	do_html

.PHONY:	do_html
do_html:	|	$(MODULE_DOCS)
	$(MAKE) -f Makefile.sphinx html
	touch $(CURRENT_DIR)/build/html/.nojekyll

.PHONY:	clean
clean:
	@rm -rf $(CURRENT_DIR)/build
	@rm -rf $(MODULE_DOCS_FOLDER)

create-docs-tree:
	@mkdir -p $(MODULE_DOCS_FOLDER)

install-collections:
	poetry env use python
	mkdir -p $(ANSIBLE_COLLECTIONS_PATH)
	poetry run ansible-galaxy collection install -vv git+file://$(GITHUB_WORKSPACE)

source/modules/%.rst:	../plugins/modules/%.py
	poetry env use python
	poetry run ansible-doc-extractor  --template $(template) $(MODULE_DOCS_FOLDER) $<
