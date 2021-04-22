# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Kamesh Sampath <kamesh.sampath@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

from OpenSSL import SSL
import socket
import certifi


def get_ca_issuer_thumbprints(hostname, port=443, digest_algorithm='sha1'):
    """
    Get ROOT CA Thumbprint form the Server Root Certificate Chain
    Args:
        hostname: the server hostname
        port: the server https port to connect to, default to 443
        digest_algorithm: the digest algorithm to use, defaults to 'sha1'
    Returns:
        the SHA1 fingerprint of the issuer CA certiciate
    """
    fingerprint = None
    try:
        context = SSL.Context(method=SSL.TLSv1_METHOD)
        context.load_verify_locations(cafile=certifi.where())

        conn = SSL.Connection(context, socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        conn.connect((hostname, port))
        conn.do_handshake()
        conn.set_tlsext_host_name(hostname.encode())
        certs = conn.get_peer_cert_chain()
        fp = None
        if certs and len(certs) > 1:
            str_digest = certs[-1].digest(digest_algorithm).decode()
            fp = str_digest.replace(":", "").lower()
        return fp
    except socket.error as e:
        print(f"Socket Error {e}")
        pass

    return fingerprint
