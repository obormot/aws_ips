"""
EC2 utils
"""
import boto3


def get_info():
    result = []
    client = boto3.client('ec2')
    data = client.describe_instances()

    while data:
        next_token = data.get('NextToken')
        for reservation in data['Reservations']:
            for instance in reservation['Instances']:
                ec2_instance_id = instance.get('InstanceId')
                ec2_public_ips = set()
                ec2_public_ip6s = set()
                ec2_public_dns_names = set()

                # PublicIpAddress and PublicDnsName exists for EC2-Classic
                if instance.get('PublicIpAddress', False):
                    ec2_public_ips.add(instance.get('PublicIpAddress'))
                    ec2_public_dns_names.add(instance.get('PublicDnsName'))

                # NetworkInterfaces exists for EC2-VPC
                for interface in instance.get('NetworkInterfaces', []):
                    if interface.get('Association', {}).get('PublicIp', False):
                        ec2_public_ips.add(interface['Association']['PublicIp'])
                        ec2_public_dns_names.add(interface['Association']['PublicDnsName'])

                    for ip6 in interface.get('Ipv6Addresses'):
                        ec2_public_ip6s.add(ip6['Ipv6Address'])

                if ec2_public_ips:
                    result.append({
                        'ec2_instance_id': ec2_instance_id,
                        'ec2_public_ips': list(ec2_public_ips),
                        'ec2_public_ip6s': list(ec2_public_ip6s),
                        'ec2_public_dns_names': list(ec2_public_dns_names),
                    })

        if next_token is None:
            data = None
        else:
            data = client.describe_instances(NextToken=next_token)

    return result
