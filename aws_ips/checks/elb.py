"""
ELB EC2-Classic utils
"""
import boto3

from aws_ips.utils import resolve_host


def get_info():
    client = boto3.client('elb')

    data = client.describe_load_balancers()

    while data:
        next_marker = data.get('NextMarker')

        for description in data.get('LoadBalancerDescriptions', []):
            if description.get('Scheme') == 'internet-facing':
                yield {
                    'id': description.get('CanonicalHostedZoneNameID'),
                    'service_name': 'ELB',
                    'public_ip_v4': [resolve_host(description.get('DNSName'))],
                    'public_dns': [description.get('DNSName')],
                }

        data = client.describe_load_balancers(Marker=next_marker) if next_marker else None
