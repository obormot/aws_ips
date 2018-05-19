"""
RDS utils
"""
import boto3

from aws_ips.utils import resolve_host


def get_info():
    client = boto3.client('rds')

    data = client.describe_db_instances()

    while data:
        marker = data.get('Marker')

        for instance in data.get('DBInstances', []):
            if instance.get('PubliclyAccessible'):
                hostname = instance.get('Endpoint', {}).get('Address')
                yield {
                    'id': instance.get('DbiResourceId'),
                    'service_name': 'RDS',
                    'public_ip_v4': [resolve_host(hostname)],
                    'public_dns': [hostname],
                }

        data = client.describe_db_instances(Marker=marker) if marker else None
