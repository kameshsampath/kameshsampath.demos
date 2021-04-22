#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Kamesh Sampath <kamesh.sampath@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

from urllib.parse import urlparse


def is_https(url):
    """
    Check if the url is an https url
    Args:
        url: the url to check the protocol scheme
    Returns:
        "true" if the url is https
    """
    parse_result = urlparse(url)

    return parse_result.scheme == 'https'


def get_oidc_provider_name(url):
    """
    Gets the name of the OIDC provider from url, the name is usally the hostname and path segments
    of the url.
    For example if URL is  https://s3.ap-south-1.amazonaws.com/my-open-id-provider,
    Then the name is "s3.ap-south-1.amazonaws.com/my-open-id-provider"
    Args:
        url: the url form which the name to be extracted
    Returns:
        the name which is hostname + path segments of the url
    """
    parse_result = urlparse(url)
    return parse_result.hostname + parse_result.path


def get_host_name_port(url):
    """
    Extracts the hostname and port from the url.
    Args:
        url: the url form which the hostname and port to be extracted
    Returns:
        A tuple of hostname and port
    """
    parse_result = urlparse(url)
    if parse_result:
        if parse_result.scheme == 'https':
            return (parse_result.hostname, 443)
        elif parse_result.scheme == 'http':
            return (parse_result.hostname, 80)
    return None
