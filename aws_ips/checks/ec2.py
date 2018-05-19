"""
EC2 utils
"""
import boto3


def get_info():
    client = boto3.client('ec2')
    data = client.describe_instances()

    while data:
        next_token = data.get('NextToken')

        for reservation in data['Reservations']:
            for instance in reservation['Instances']:
                ec2_instance_id = instance.get('InstanceId')
                ec2_public_ip_v4 = set()
                ec2_public_ip_v6 = set()
                ec2_public_dns_names = set()

                # PublicIpAddress and PublicDnsName exists for EC2-Classic
                if instance.get('PublicIpAddress', False):
                    ec2_public_ip_v4.add(instance.get('PublicIpAddress'))
                    ec2_public_dns_names.add(instance.get('PublicDnsName'))

                # NetworkInterfaces exists for EC2-VPC
                for interface in instance.get('NetworkInterfaces', []):
                    if interface.get('Association', {}).get('PublicIp', False):
                        ec2_public_ip_v4.add(interface['Association']['PublicIp'])
                        ec2_public_dns_names.add(interface['Association']['PublicDnsName'])

                    for ip6 in interface.get('Ipv6Addresses'):
                        ec2_public_ip_v6.add(ip6['Ipv6Address'])

                if ec2_public_ip_v4:
                    yield {
                        'id': ec2_instance_id,
                        'service_name': 'EC2',
                        'public_ip_v4': list(ec2_public_ip_v4),
                        'public_ip_v6': list(ec2_public_ip_v6),
                        'public_dns': list(ec2_public_dns_names),
                    }

        data = client.describe_instances(NextToken=next_token) if next_token else None
