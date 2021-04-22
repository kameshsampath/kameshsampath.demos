ENV_FILE := .env
include ${ENV_FILE}
export $(shell sed 's/=.*//' ${ENV_FILE})
CURRENT_DIR = $(shell pwd)

ANSIBLE_BUILDER := poetry run ansible-builder

VERSION=`cat $(FILE)`
COLLECTION_FQN=kameshsampath.demos
TEST_ARGS ?= ""
PYTHON_VERSION ?= `python -c 'import platform; print("{0}.{1}".format(platform.python_version_tuple()[0], platform.python_version_tuple()[1]))'`

clean:
	rm -f kameshsampath-demos-${VERSION}.tar.gz
	rm -rf ansible_collections
	rm -rf tests/output

build: clean
	ansible-galaxy collection build

test-sanity:
	ansible-test sanity --docker -v --color --python $(PYTHON_VERSION) $(?TEST_ARGS)

test-integration:
	ansible-test integration --docker -v --color --retry-on-error --python $(PYTHON_VERSION) --continue-on-error --diff --coverage $(?TEST_ARGS)

test-molecule:
	molecule test

test-unit:
	ansible-test units --docker -v --color --python $(PYTHON_VERSION) $(?TEST_ARGS)

.PHONY:
buildee:
	$(ANSIBLE_BUILDER) build -f $(BUILDER_EE_FILE) \
	   --context $(CURRENT_DIR)/$(BUILDER_EE_CONTEXT) \
  	   --tag $(ANSIBLE_RUNNER_IMAGE) \
       --container-runtime $(CONTAINER_RUNTIME)

.PHONY:	push
push:	buildee
	@$(CONTAINER_RUNTIME) push $(ANSIBLE_RUNNER_IMAGE)