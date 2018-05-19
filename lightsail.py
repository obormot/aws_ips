"""
Lightsail utils
"""
import boto3

from utils import resolve_host


def get_info():
    result = []
    client = boto3.client('lightsail')

    data = client.get_instances()
    while data:
        next_page_token = data.get('nextPageToken')

        for instance in data.get('instances', []):
            result.append({
                'lightsail_id': instance.get('name'),
                'lightsail_public_ip': instance.get('publicIpAddress'),
            })

        data = client.get_instances(pageToken=next_page_token) if next_page_token else None

    data = client.get_load_balancers()
    while data:
        next_page_token = data.get('nextPageToken')

        for balancer in data.get('loadBalancers', []):
            result.append({
                'lightsail_id': balancer.get('name'),
                'lightsail_public_dns_name': balancer.get('dnsName'),
                'lightsail_public_ip': resolve_host(balancer.get('dnsName')),
            })

        data = client.get_load_balancers(pageToken=next_page_token) if next_page_token else None

    return result
