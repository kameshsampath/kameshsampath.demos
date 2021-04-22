# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Kamesh Sampath <kamesh.sampath@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import pytest

ISSUER_HOSTS = [
    ("redhat.com", 'a031c46782e6e6c662c2c87c76da9aa62ccabd8e'),
    ("foobar.org", None)
]
from ansible_collections.kameshsampath.demos.plugins.module_utils.ssl.utils import get_ca_issuer_thumbprints


class TestSSLUtils:

    @pytest.mark.parametrize('host_name,expected_fingerprint', ISSUER_HOSTS)
    def test_valid_host(self, host_name, expected_fingerprint):
        try:
            actual = get_ca_issuer_thumbprints(hostname=host_name)
        except:
            actual = None

        print(f"Actual fingerprint is {actual}")
        assert actual == expected_fingerprint
