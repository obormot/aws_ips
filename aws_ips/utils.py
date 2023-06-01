"""
Various utils
"""
import json
import subprocess


def jprint(anything):
    """
    pprint() alternative
    """
    print(json.dumps(anything, default=str, sort_keys=True, indent=4))


def resolve_host(hostname):
    """
    Resolve hostname
    """
    if not hostname:
        return ''

    out = subprocess.check_output(['dig', '+short', hostname])
    return out.decode('ascii').split() if out else ''
