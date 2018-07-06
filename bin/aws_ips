#!/usr/bin/env python
import argparse

from aws_ips.cli import handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--service', type=str, default='',
        help='Comma separated list of services to check. Available services are apigateway, cloudfront, ec2, '
             'elasticsearch, elb, elbv2, lightsail, rds, redshift. Default is all.')
    parser.add_argument(
        '-f', '--format', type=str, default='text',
        help='Output format. Available formats are text, json, pretty (pretty json), jl (json lines). Default is test.')
    parser.add_argument(
        '-v', '--verbose', default=False, dest='verbose', action='store_true',
        help='Enable verbose output. The verbose output includes additional things like'
             'service names, instance IDs and DNS.')

    handler(parser.parse_args())

if __name__ == '__main__':
    main()
