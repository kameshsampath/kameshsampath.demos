# Kamesh's OpenShift/Kubernetes Demos Ansible Collection

This repo contains the `kameshsampath.demos` Ansible Collection. The collection includes many modules and roles that are used as part of my [OpenShift](https://try.openshift.com) Demos. The roles and modules helps you set up and configure OpenShift resources and other underlying Cloud Provider resources.

You can find [documentation for this collection on the GitHub pages](https://kameshsampath.github.io/kameshsampath.demos/).

__WARNING__

    Still work in progress and subject to lot of changes

## Development

It's recommended to use a Virtual Environment for developing. [Install Poetry](https://python-poetry.org/docs/#installation), clone the sources from https://github.com/kameshsampath/kameshsampath.demos then run:

```shell
   cd $PROJECT_HOME
   # get to its own virtual environment
   poetry shell
   poetry install
```