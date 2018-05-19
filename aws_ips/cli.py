"""
Command line handler
"""
import json

from aws_ips.utils import jprint
from aws_ips.checks import (
    apigateway,
    cloudfront,
    ec2,
    elasticsearch,
    elb,
    elbv2,
    rds,
    lightsail,
    redshift,
)

# Used to output one complete JSON
_ITEMS = []


def _get_results(services):
    if 'apigateway' in services or 'all' in services:
        for item in apigateway.get_info():
            yield item

    if 'cloudfront' in services or 'all' in services:
        for item in cloudfront.get_info():
            yield item

    if 'ec2' in services or 'all' in services:
        for item in ec2.get_info():
            yield item

    if 'elasticsearch' in services or 'all' in services:
        for item in elasticsearch.get_info():
            yield item

    if 'elb' in services or 'all' in services:
        for item in elb.get_info():
            yield item

    if 'elbv2' in services or 'all' in services:
        for item in elbv2.get_info():
            yield item

    if 'rds' in services or 'all' in services:
        for item in rds.get_info():
            yield item

    if 'lightsail' in services or 'all' in services:
        for item in lightsail.get_info():
            yield item

    if 'redshift' in services or 'all' in services:
        for item in redshift.get_info():
            yield item


def _print_text(item, verbose):
    if verbose:
        print('Service name {}:'.format(item.get('service_name')))
        print('Instance ID: {}'.format(item.get('id')))

    for ip_v4 in item.get('public_ip_v4', []):
        print(ip_v4)

    for ip_v6 in item.get('public_ip_v6', []):
        print(ip_v6)

    if verbose:
        for dns_name in item.get('public_dns', []):
            print(dns_name)
        print()


def _print_json_line(item, verbose):
    if not verbose:
        del item['id']
        del item['service_name']
        del item['public_dns']

    # clean empty public_ip_v6 lists
    if 'public_ip_v6' in item and not item['public_ip_v6']:
        del item['public_ip_v6']

    print(json.dumps(item, sort_keys=True))


def _collect_items(item, verbose):
    """
    Used to collect all items to output them as one big JSON at once
    """
    global _ITEMS

    if not verbose:
        del item['id']
        del item['service_name']
        del item['public_dns']

    # clean empty public_ip_v6 lists
    if 'public_ip_v6' in item and not item['public_ip_v6']:
        del item['public_ip_v6']

    if verbose:
        _ITEMS.append(item)
    else:
        for ip_v4 in item.get('public_ip_v4', []):
            _ITEMS.append(ip_v4)

        for ip_v6 in item.get('public_ip_v6', []):
            _ITEMS.append(ip_v6)


def handler(args):
    """
    :param args: type: argparse.Namespace
    :return:
    """
    services = args.service.split(',') if args.service else ['all']
    for item in _get_results(services):
        if args.format == 'text':
            _print_text(item, args.verbose)

        if args.format == 'jl':
            _print_json_line(item, args.verbose)

        if args.format == 'json' or args.format == 'pretty':
            _collect_items(item, args.verbose)

    if args.format == 'json':
        print(json.dumps(_ITEMS, sort_keys=True))

    if args.format == 'pretty':
        jprint(_ITEMS)
