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
                hostname = description.get('DNSName')
                ips = resolve_host(hostname)
                if ips:  # if resolves to a public IP
                    yield {
                        'id': '{}-{}'.format(description.get('CanonicalHostedZoneId'), description.get('LoadBalancerName')),
                        'service_name': 'ELBv2',
                        'public_ip_v4': ips,
                        'public_dns': [hostname],
                    }

        data = client.describe_load_balancers(Marker=next_marker) if next_marker else None
