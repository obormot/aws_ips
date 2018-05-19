"""
Lightsail utils
"""
import boto3

from aws_ips.utils import resolve_host


def get_info():
    client = boto3.client('lightsail')

    data = client.get_instances()
    while data:
        next_page_token = data.get('nextPageToken')

        for instance in data.get('instances', []):
            yield {
                'id': instance.get('name'),
                'service_name': 'Lightsail',
                'public_ip_v4': [instance.get('publicIpAddress')],
            }

        data = client.get_instances(pageToken=next_page_token) if next_page_token else None

    data = client.get_load_balancers()
    while data:
        next_page_token = data.get('nextPageToken')

        for balancer in data.get('loadBalancers', []):
            yield {
                'id': balancer.get('name'),
                'service_name': 'Lightsail',
                'public_ip_v4': [resolve_host(balancer.get('dnsName'))],
                'public_dns': [balancer.get('dnsName')],
            }

        data = client.get_load_balancers(pageToken=next_page_token) if next_page_token else None
