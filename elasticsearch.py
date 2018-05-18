"""
Elasticsearch utils
"""
import boto3

from utils import resolve_host


def get_info():
    result = []
    client = boto3.client('es')

    domains = []
    data = client.list_domain_names()

    for domain in data.get('DomainNames', []):
        domains.append(domain.get('DomainName'))

    if domains:
        data = client.describe_elasticsearch_domains(DomainNames=domains)
        for domain in data.get('DomainStatusList'):
            result.append({
                'elasticsearch_domain_id': domain.get('DomainId'),
                'elasticsearch_hostname': domain.get('Endpoint'),
                'elasticsearch_ip': resolve_host(domain.get('Endpoint')),
            })

    return result
