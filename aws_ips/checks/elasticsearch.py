"""
Elasticsearch utils
"""
import boto3

from aws_ips.utils import resolve_host


def get_info():
    client = boto3.client('es')

    domains = []
    data = client.list_domain_names()

    for domain in data.get('DomainNames', []):
        domains.append(domain.get('DomainName'))

    if domains:
        data = client.describe_elasticsearch_domains(DomainNames=domains)
        for domain in data.get('DomainStatusList'):
            yield {
                'id': domain.get('DomainId'),
                'service_name': 'Elasticsearch',
                'public_ip_v4': [resolve_host(domain.get('Endpoint'))],
                'public_dns': [domain.get('Endpoint')],
            }
