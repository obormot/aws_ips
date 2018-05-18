"""
Redshift utils
"""
import boto3


def get_info():
    result = []
    client = boto3.client('redshift')
    data = client.describe_clusters()

    for cluster in data.get('Clusters', []):
        if cluster.get('PubliclyAccessible', False):
            result.append({
                'redshift_cluster_id': cluster.get('ClusterIdentifier'),
                'redshift_cluster_hostname': cluster.get('Endpoint', {}).get('Address'),
                'redshift_cluster_ips': [node.get('PublicIPAddress') for node in cluster.get('ClusterNodes')],
            })

    return result
