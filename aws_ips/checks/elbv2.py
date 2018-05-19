"""
ELBv2 utils
"""
import boto3

from aws_ips.utils import resolve_host


def get_info():
    client = boto3.client('elbv2')

    data = client.describe_load_balancers()

    while data:
        next_marker = data.get('NextMarker')

        for description in data.get('LoadBalancers', []):
            if description.get('Scheme') == 'internet-facing':
                yield {
                    'id': '{}-{}'.format(description.get('CanonicalHostedZoneId'), description.get('LoadBalancerName')),
                    'service_name': 'ELBv2',
                    'public_ip_v4': [resolve_host(description.get('DNSName'))],
                    'public_dns': [description.get('DNSName')],
                }

        data = client.describe_load_balancers(Marker=next_marker) if next_marker else None
