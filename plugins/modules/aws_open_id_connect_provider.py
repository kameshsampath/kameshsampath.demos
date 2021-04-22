#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Kamesh Sampath <kamesh.sampath@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

import boto3

from ansible_collections.kameshsampath.demos.plugins.module_utils.url import utils as url_utils
from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.kameshsampath.demos.plugins.module_utils.ssl import utils
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry, boto3_tag_list_to_ansible_dict, \
    ansible_dict_to_boto3_tag_list, \
    compare_aws_tags
from urllib.parse import urlparse

__metaclass__ = type

DOCUMENTATION = r'''
---
module: aws_openid_connect_provider
short_description: Create, Update or Delete OpenID Connect Provider
description:
    - Create, update or delete L(AWS IAM OpenID Connect provider,https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html). 
options:
    thumbprints:
        description: 
         - Optional thumbprint(SHA1) of the Root Certificate Authority associated with the 
         - Provider URL.  This is usually requried when you have rotating certificates.
         - When not provided the fingerprints is computed form the provider url.
        type: list
        elements: str
    url:
        description:
          - The https URL of the identity provider.
        required: true
        type: str
    client_ids:
        description:
         - A list of client IDs (also known as audiences).  
         - If not provided, 'sts.amazonaws.com' is added as default client id
        type: list
        elements: str
    state:
        description: Whether to create or delete the AWS OpenID Connect Provider
        choices:
        - present
        - absent
        default: present
        type: str
    purge_tags:
        description:
          - Delete any tags not specified in the task that are on the OpenID Connect Provider.
            This means you have to specify all the desired tags on each task affecting an Provider.
        default: true
        type: bool
    purge_thumbprints:
        description:
          - Delete any Thumbprints not specified in the task that are on the OpenID Connect Provider.
            This means you have to specify all the Thumbprints tags on each task affecting an Provider.
        default: true
    purge_client_ids:
        description:
          - Delete any Client IDs not specified in the task that are on the OpenID Connect Provider.
            This means you have to specify all the  Client IDs tags on each task affecting an Provider.
        default: true
        type: bool
    tags:
        description: 
          - The AWS Resource Tags to add to the OpenID Connect Provider
        type: dict
        
extends_documentation_fragment:
- amazon.aws.aws

author:
  - Kamesh (@kameshsampath)
'''

EXAMPLES = r'''
# Create an OpenID Provider with URL https://s3.ap-southeast-1.amazonaws.com/rosa-demos-oidc
kameshsampath.demos.aws_open_id_connect_provider:
state: present
url: s3.ap-southeast-1.amazonaws.com/rosa-demos-oidc
  
# Create an OpenID Provider with URL https://s3.ap-southeast-1.amazonaws.com/rosa-demos-oidc
# with tags
kameshsampath.demos.aws_open_id_connect_provider:
state: present
url: s3.ap-southeast-1.amazonaws.com/rosa-demos-oidc
tags:
  Name: rosa-demos-oidc
  Author: kameshsampath
   
# Delete an OpenID Provider with URL https://s3.ap-southeast-1.amazonaws.com/rosa-demos-oidc
kameshsampath.demos.aws_open_id_connect_provider:
state: absent
url: https://s3.ap-southeast-1.amazonaws.com/rosa-demos-oidc
'''

RETURN = r'''
provider_arn:
    description: 
      - The Provider ARN of the created OpenId Connect Provider, this returned only during create.
    type: string
    sample: 'arn:aws:iam::1234567890:oidc-provider/s3.ap-southeast-1.amazonaws.com/rosa-demos-oidc'
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

    def diff_and_merge_lists(self, new_list, old_list):
        """
        Compute the differences between two lists new_list and old_list,
        filter duplicates out and return list of unique elements merged
        from two lists
        Args:
             new_list: the list of new elements that needs to be merged with old_list
             old_list: the existing or old list of elements
        Returns:
            List of unique elements form both new_list and old_list
        """
        new_list = set(new_list)
        only_new = new_list - old_list
        merged_list = list(old_list) + list(only_new)
        list_of_unique_elements = list(set(merged_list))
        return list_of_unique_elements

    @AWSRetry.backoff(tries=3, delay=5)
    def _get_provider_arn(self, url):
        """
        Get the OpenID Connect Provider ARN from the Provider URL by iterating through the list
        of OpenID Connect Providers and find the matching name.
        Args:
            url: The OpenID Connect Provider URL
        Returns:
           The AWS ARN of the OpenID Connect Provider
       """
        providers = self.connection.list_open_id_connect_providers()
        name = url_utils.get_oidc_provider_name(url)

        if name:
            for p in providers['OpenIDConnectProviderList']:
                provider_name = p['Arn'].split('/', 1)[1]
                if name == provider_name:
                    return p['Arn']
        return None

    @AWSRetry.jittered_backoff()
    def _manage_tags(self, arn, match, new_tags, purge_tags):
        """
        Args:
        Returns:
            If the
        """
        changed = False
        old_tags = boto3_tag_list_to_ansible_dict(match['Tags'])
        tags_to_set, tags_to_delete = compare_aws_tags(
            old_tags, new_tags,
            purge_tags=purge_tags,
        )

        if tags_to_set:
            print(f"Setting Tags for {arn}")
            self.connection.tag_open_id_connect_provider(
                OpenIDConnectProviderArn=arn,
                Tags=ansible_dict_to_boto3_tag_list(tags_to_set))
            changed |= True

        if tags_to_delete:
            print(f"Purging Tags for {arn}")
            self.connection.untag_open_id_connect_provider(
                OpenIDConnectProviderArn=arn,
                TagKeys=tags_to_delete)
            changed |= True
        return changed

    @AWSRetry.jittered_backoff()
    def _manage_thumbprints(self, arn, match, new_thumbprints, purge_thumbprints):
        changed = False

        if purge_thumbprints or len(new_thumbprints) > 5:
            print(f"Purge and Setting Thumbprints for {arn}")
            unique_thumbprints = set(new_thumbprints)
            to_be_set = new_thumbprints
            self.connection.update_open_id_connect_provider_thumbprint(
                OpenIDConnectProviderArn=arn,
                ThumbprintList=to_be_set)
            changed |= True
        else:
            print(f"Merging Thumbprints for {arn}")
            old_thumbprints = set(match["ThumbprintList"])
            to_be_set = self.diff_and_merge_lists(new_thumbprints, old_thumbprints)
            self.connection.update_open_id_connect_provider_thumbprint(
                OpenIDConnectProviderArn=arn,
                ThumbprintList=to_be_set)
            changed |= True
        return changed

    @AWSRetry.jittered_backoff()
    def _mannage_client_ids(self, arn, match, new_client_ids, purge_client_ids):
        changed = False
        to_be_set = None

        if purge_client_ids:
            old_client_ids = match['ClientIDList']
            for client_id in old_client_ids:
                self.connection.remove_client_id_from_open_id_connect_provider(
                    OpenIDConnectProviderArn=arn,
                    ClientID=client_id)
            to_be_set = new_client_ids
        else:
            old_client_ids = set(match['ClientIDList'])
            to_be_set = self.diff_and_merge_lists(new_client_ids, old_client_ids)

        for client_id in to_be_set:
            self.connection.add_client_id_to_open_id_connect_provider(
                OpenIDConnectProviderArn=arn,
                ClientID=client_id)

        changed |= True
        return changed

    @AWSRetry.backoff(tries=3, delay=5)
    def create_or_update_open_id_connect_provider(self):

        url = self.module.params['url']

        if not url_utils.is_https(url):
            self.module.fail_json(f"OpenID Connect Provider requires an HTTPS url, but got '{url}")

        thumbprints = self.module.params['thumbprints']
        client_ids = self.module.params['client_ids']
        tags = self.module.params['tags']
        purge_tags = self.module.params['purge_tags']
        purge_client_ids = self.module.params['purge_client_ids']
        purge_thumbprints = self.module.params['purge_thumbprints']

        if thumbprints:
            i = 0
            # only take first five values if more than five thumbprints are given
            thumbprints = thumbprints[:5] if len(thumbprints) > 5 else thumbprints
            while i < len(thumbprints):
                thumbprints[i] = thumbprints[i].lower()
                i += 1
        else:
            hostname, port = url_utils.get_host_name_port(url)
            thumbprint = utils.get_ca_issuer_thumbprints(hostname=hostname, port=port)
            if thumbprint:
                thumbprints = [thumbprint]
            else:
                self.module.fail_json(f"Error getting Issuer thumbprint Connect Provider with '{url}")

        result = {'changed': False}

        try:
            arn = self._get_provider_arn(url)
        except botocore.exceptions.ClientError as e:
            self.module.fail_json_aws(e, msg="Could not create or update OpenID Connect Provider '{0}'".format(url))

        if arn:  # Check if update is required
            print("Update OpenID Provider with Arn '{0}'".format(arn))
            res = {'changed': False}

            try:
                response = self.connection.get_open_id_connect_provider(OpenIDConnectProviderArn=arn)

                # Check if thumbprints have changed
                if thumbprints and len(thumbprints) > 0 and response['ThumbprintList'] != thumbprints:
                    res['changed'] = True
                    self._manage_thumbprints(arn, response, thumbprints, purge_thumbprints)

                # Check if ClientID List have changed
                if client_ids and len(client_ids) > 0 and response['ClientIDList'] != client_ids:
                    res['changed'] = True
                    self._mannage_client_ids(arn, response, client_ids, purge_client_ids)

                # Check if Tags Have changed
                if tags:
                    res['changed'] = self._manage_tags(arn, response, tags, purge_tags)

                self.module.exit_json(**res)
            except botocore.exceptions.ClientError as e:
                self.module.fail_json_aws(e, msg="Could not create or update OpenID Connect Provider '{0}'".format(url))
        else:
            print("Create OpenID Provider with url '{0}'".format(url))
            if not client_ids:
                client_ids = ['sts.amazonaws.com']

            if tags:
                tagList = ansible_dict_to_boto3_tag_list(tags)
            else:
                tagList = []

            # only take first five values if more than five thumbprints are given
            thumbprints = thumbprints[:5] if len(thumbprints) > 5 else thumbprints

            try:
                resp = self.connection.create_open_id_connect_provider(
                    Url=url,
                    ThumbprintList=thumbprints,
                    ClientIDList=client_ids,
                    Tags=tagList
                )
                result['changed'] = True
                result['Arn'] = resp['OpenIDConnectProviderArn']
                self.module.exit_json(**result)
            except botocore.exceptions.ClientError as e:
                self.module.fail_json_aws(e, msg="Could not create OpenID Connect Provider '{0}'".format(url))

    @AWSRetry.backoff(tries=3, delay=5)
    def delete_open_id_connect_provider(self):
        url = self.module.params['url']
        print("Deleting OpenID Provider with url '{0}'".format(url))

        result = dict(
            changed=False
        )

        try:
            arn = self._get_provider_arn(url)
            if arn:
                self.connection.delete_open_id_connect_provider(OpenIDConnectProviderArn=arn)
                result['changed'] = True
            else:
                print(f"No OpenID Provider with url '{0}' exists".format(url))
            self.module.exit_json(**result)
        except botocore.exceptions.ClientError as e:
            self.module.fail_json_aws(e, msg="Could not delete OpenID Connect Provider '{0}'".format(url))


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        client_ids=dict(required=False, type='list', element="str"),
        url=dict(required=True, type='str'),
        thumbprints=dict(required=False, type='list', element="str"),
        state=dict(default='present', required=False, choices=['present', 'absent']),
        purge_tags=dict(type='bool', required=False, default=True),
        purge_thumbprints=dict(type='bool', required=False, default=True),
        purge_client_ids=dict(type='bool', required=False, default=True),
        tags=dict(type='dict', required=False),
    )

    module = AnsibleAWSModule(
        argument_spec=module_args,
        supports_check_mode=True, )

    openid_provider = OpenIdConnectProvider(module)

    state = module.params['state']

    if state == "present":
        result = openid_provider.create_or_update_open_id_connect_provider()
        module.exit_json(**result)
    elif state == "absent":
        result = openid_provider.delete_open_id_connect_provider()
        module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
