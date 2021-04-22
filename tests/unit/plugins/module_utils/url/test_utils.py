# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Kamesh Sampath <kamesh.sampath@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import pytest

URLS = [
    ("https://s3.ap-southeast-1.amazonaws.com/test-add-rosa-demos-oidc",
     "s3.ap-southeast-1.amazonaws.com/test-add-rosa-demos-oidc"),
    ("https://s3.ap-southeast-1.amazonaws.com", "s3.ap-southeast-1.amazonaws.com"),
    ("foobar", None)
]

HOSTS = [
    ("https://s3.ap-southeast-1.amazonaws.com/test-add-rosa-demos-oidc", ("s3.ap-southeast-1.amazonaws.com", 443)),
    ("http://example.com", ("example.com", 80))
]

from ansible_collections.kameshsampath.demos.plugins.module_utils.url.utils import get_oidc_provider_name, \
    get_host_name_port, is_https


class TestURLUtils:

    @pytest.mark.parametrize('url,provider_name', URLS)
    def test_provider_name(self, url, provider_name):
        try:
            actual = get_oidc_provider_name(url=url)
        except:
            actual = None

        assert actual == provider_name

    @pytest.mark.parametrize('url,hostname_port', HOSTS)
    def test_hostname_port(self, url, hostname_port):
        try:
            actual = get_host_name_port(url=url)
        except:
            actual = None

        assert actual == hostname_port

    @pytest.mark.parametrize('url,expected',
                             [("https://s3.ap-southeast-1.amazonaws.com/test-add-rosa-demos-oidc", True),
                              ("http://example.com", False)])
    def test_is_https(self, url, expected):
        try:
            actual = is_https(url=url)
        except:
            actual = None

        assert actual == expected
