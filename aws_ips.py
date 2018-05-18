#!/usr/bin/env python
import ec2
import redshift
from utils import jprint


def main():
    jprint(ec2.get_info())
    jprint(redshift.get_info())


if __name__ == '__main__':
    main()
