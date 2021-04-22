.. _install:

Installing the Collection
-------------------------

Before using the `kamesampath.demos` collection, you need to install it with the Ansible Galaxy CLI:

.. code-block:: bash

    ansible-galaxy collection install https://github.com/kameshsampath/kameshsampath.demos.git,main

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

.. code-block:: yaml

    collections:
      - name: https://github.com/kameshsampath/kameshsampath.demos.git
        type: git
        version: 0.0.1

Using the Collection
--------------------

It's preferable to use content in this collection using their Fully Qualified Collection Namespace (FQCN), for example `kameshsampath.demos`:

.. code-block:: yaml

    # Create an AWS OpenID Connect Provider
    - name: "Create OpenID Connect Provider"
      kameshsampath.demos.aws_open_id_connect_provider:
        state: present
        url: https://s3.ap-southeast-1.amazonaws.com

    # Get info about am AWS OpenID Connect Provider
    - name: "Create OpenID Connect Provider"
      kameshsampath.demos.aws_open_id_connect_provider_info:
        state: present
        url: https://s3.ap-southeast-1.amazonaws.com