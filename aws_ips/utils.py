"""
Various utils
"""
import json
import socket


def jprint(anything):
    """
    pprint() alternative
    """
    print(json.dumps(anything, default=str, sort_keys=True, indent=4))


def resolve_host(hostname):
    """
    Resolve hostname
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return ''
