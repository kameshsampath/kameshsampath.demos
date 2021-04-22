#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Kamesh Sampath <kamesh.sampath@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import boto3

from ansible_collections.kameshsampath.demos.plugins.module_utils.url import utils as url_utils
from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry, boto3_tag_list_to_ansible_dict

DOCUMENTATION = r'''
---
module: aws_open_id_connect_provider_info
short_description: Retrives information about AWS OpenID Connect Providers.
description:
  - Retrives AWS OpenID Connect Providers, with ability to filter the providers
    using the url.
options:
  url:
    description: 
    - The url of the OpenID Connect provider. If not set all the available OpenID Connect Providers will be retrieved.
    type: str
extends_documentation_fragment:
  - amazon.aws.aws
author:
  - Kamesh (@kameshsampath)
'''

EXAMPLES = r'''
---

# Get all available OpenID Connect Providers
- name: Get all OpenID Connect Providers
  kameshsampath.demos.aws_openid_connect_provider_info:
  
# Check if Provider exists by name 
- name: Get all OpenID Connect by url
  kameshsampath.demos.aws_openid_connect_provider_info:
    url: 'https://example.com/my-provider'
'''

RETURN = r'''
---
# These are examples of possible return values, and in general should use other names for return values.
open_id_connect_providers:
    description: 
     - The list of OpenID Connect Providers with its details such as url,
       arn, list of client ids, list of associated thumbprints, creation date and 
       tags.
    type: complex
    returned: list
    sample: [
     {
       "Url": 'https://s3.ap-southeast-1.amazonaws.com/rosa-demos-oidc',
       "ClientIDList": [ "sts.amazonaws.com"],
       "ThumbprintList": [ "a9d53002e97e00e043244f3d170d6f4c414104fd"],
       "CreateDate": "2015-1-1",
       "Tags":{
          Name:  "rosa-demos-oidc",
          Subject: "demos"
        },
       "Arn": 'arn:aws:iam::123456790:oidc-provider/s3.ap-southeast-1.amazonaws.com/rosa-demos-oidc'
       }
    ]
        
provider_exist:
    description: 
     - If the provider checked for exists
    type: boolean
    returned: when the provider by url exists
    sample: 'false'

'''

try:
    import botocore.exceptions
except ImportError:
    pass


class OpenIdConnectProvider:
    """Handles OpenId Connect Provider"""

    def __init__(self, module):
        self.module = module

        try:
            self.connection = module.client("iam")
        except botocore.exceptions.ClientError as e:
            self.module.fail_json_aws(e, msg="Unknown boto error")

    @AWSRetry.backoff(tries=3, delay=5)
    def _get_provider_info(self, arn):
        try:
            provider_info = self.connection.get_open_id_connect_provider(OpenIDConnectProviderArn=arn)
            print(f"Provider Info {provider_info}")
            del provider_info['ResponseMetadata']
            provider_info['Arn'] = arn
            # the Provider urls are always https
            provider_info['Url'] = 'https://' + provider_info['Url']
            # Convert that Tags to Ansible Key Pair Value
            if provider_info['Tags']:
                provider_info['Tags'] = boto3_tag_list_to_ansible_dict(provider_info['Tags'])

            return provider_info
        except botocore.exceptions.ClientError as e:
            self.module.fail_json_aws(e,
                                      msg="Unable to get  OpenID Connect Provider '{0}'".format(
                                          p['Arn']))

    @AWSRetry.backoff(tries=3, delay=5)
    def list_open_id_connect_providers(self, url, state):
        print(f"Getting OpenID Providers by {url}\n")
        try:
            openid_connect_providers = self.connection.list_open_id_connect_providers()
        except botocore.exceptions.ClientError as e:
            self.module.fail_json_aws(e, msg="Could not check existence of OpenID Connect Provider '{0}'".format(arn))

        result = result = dict(
            changed=False,
            open_id_connect_providers=[],
            provider_exist=False
        )

        if state == "list":
            if "OpenIDConnectProviderList" in openid_connect_providers:
                providers = openid_connect_providers["OpenIDConnectProviderList"]
                for p in providers:
                    provider_info = self._get_provider_info(p['Arn'])
                    result['open_id_connect_providers'].append(provider_info)
            self.module.exit_json(**result)
        else:
            name = url_utils.get_oidc_provider_name(url)
            if not name:
                self.module.fail_json(f"Invalid OpenID Connect Provider URL '{url}")
            if "OpenIDConnectProviderList" in openid_connect_providers:
                providers = openid_connect_providers["OpenIDConnectProviderList"]
                for p in providers:
                    provider_name = p['Arn'].split('/', 1)[1]
                    if name == provider_name:
                        result['provider_exist'] = True
                        provider_info = self._get_provider_info(p['Arn'])
                        result['open_id_connect_providers'].append(provider_info)

            self.module.exit_json(**result)


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        url=dict(required=False),
    )

    module = AnsibleAWSModule(
        argument_spec=module_args,
        supports_check_mode=True, )

    openid_provider = OpenIdConnectProvider(module)

    url = module.params['url']

    if url:
        state = "filter"
    else:
        state = "list"

    openid_provider.list_open_id_connect_providers(url, state)


def main():
    run_module()


if __name__ == '__main__':
    main()
