"""
Various utils
"""
import json


def jprint(anything):
    """
    pprint() alternative
    """
    print(json.dumps(anything, default=str, sort_keys=True, indent=4))
