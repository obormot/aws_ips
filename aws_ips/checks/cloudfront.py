"""
CloudFront utils
"""
import boto3

from aws_ips.utils import resolve_host


def get_info():
    client = boto3.client('cloudfront')

    data = client.list_distributions()
    data = data.get('DistributionList')

    while data:
        next_marker = data.get('NextMarker')
        for distribution in data.get('Items', []):
            if distribution.get('Enabled'):
                hostname = distribution['DomainName']
                ips = resolve_host(hostname)
                if ips:  # if resolves to a public IP
                    yield {
                        'id': distribution['Id'],
                        'service_name': 'CloudFront',
                        'public_ip_v4': ips,
                        'public_dns': [hostname],
                    }

        data = client.list_distributions(Marker=next_marker).get('DistributionList') if next_marker else None
