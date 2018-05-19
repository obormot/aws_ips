"""
CloudFront utils
"""
import boto3

from utils import resolve_host


def get_info():
    result = []
    client = boto3.client('cloudfront')

    data = client.list_distributions()
    data = data.get('DistributionList')

    while data:
        next_marker = data.get('NextMarker')
        for distribution in data.get('Items', []):
            if distribution.get('Enabled'):
                result.append({
                    'cloudfront_id': distribution['Id'],
                    'cloudfront_public_dns': distribution['DomainName'],
                    'cloudfront_public_ip': resolve_host(distribution['DomainName']),
                })

        data = (
            client.list_distributions(Marker=next_marker).get('DistributionList')
            if next_marker is not None else None
        )

    return result
