"""
RDS utils
"""
import boto3

from utils import resolve_host


def get_info():
    result = []
    client = boto3.client('rds')

    data = client.describe_db_instances()

    while data:
        marker = data.get('Marker')

        for instance in data.get('DBInstances', []):
            if instance.get('PubliclyAccessible'):
                hostname = instance.get('Endpoint', {}).get('Address')
                result.append({
                    'rds_id': instance.get('DbiResourceId'),
                    'rds_public_ip': resolve_host(hostname),
                    'rds_public_dns_name': hostname,
                })

        data = client.describe_db_instances(Marker=marker) if marker is not None else None

    return result
