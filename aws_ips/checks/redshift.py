"""
Redshift utils
"""
import boto3


def get_info():
    client = boto3.client('redshift')
    data = client.describe_clusters()

    for cluster in data.get('Clusters', []):
        if cluster.get('PubliclyAccessible', False):
            yield {
                'id': cluster.get('ClusterIdentifier'),
                'service_name': 'Redshift',
                'public_ip_v4': [node.get('PublicIPAddress') for node in cluster.get('ClusterNodes')],
                'public_dns': [cluster.get('Endpoint', {}).get('Address')],
            }
