#!/usr/bin/env python
import ec2
from utils import jprint


def main():
    jprint(ec2.get_info())


if __name__ == '__main__':
    main()
