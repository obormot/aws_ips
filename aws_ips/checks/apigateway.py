"""
API Gateway utils
"""
import boto3

from aws_ips.utils import resolve_host


def get_info():
    client = boto3.client('apigateway')
    data = client.get_rest_apis()

    while data:
        position = data.get('position')

        for api in data.get('items', []):
            hostname = '{}.execute-api.{}.amazonaws.com'.format(api.get('id'), client.meta.region_name)
            ips = resolve_host(hostname)
            if ips:  # if resolves to a public IP
                yield {
                    'id': api.get('id'),
                    'service_name': 'API Gateway',
                    'public_ip_v4': ips,
                    'public_dns': [hostname],
                    'tags': api.get('tags'),
                }

        data = client.get_rest_apis(position=position) if position else None
