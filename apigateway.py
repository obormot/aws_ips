"""
APIGateway utils
"""
import boto3

from utils import resolve_host


def get_info():
    result = []
    client = boto3.client('apigateway')
    data = client.get_rest_apis()

    while data:
        position = data.get('position')

        for api in data.get('items', []):
            hostname = '{}.execute-api.{}.amazonaws.com'.format(api.get('id'), client.meta.region_name)
            result.append({
                'apigateway_id': api.get('id'),
                'apigateway_ip': resolve_host(hostname),
                'apigateway_hostname': hostname,
            })

        data = client.get_rest_apis(position=position) if position is not None else None

    return result
