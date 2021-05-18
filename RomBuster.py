#!/usr/bin/env python3

import argparse

description = "RomBuster is a RomPager exploitation tool that allows to disclosure network router admin password."
parser = argparse.ArgumentParser(description=description)
parser.add_argument('--ip-list', dest='list', help='IP addresses list.')
args = parser.parse_args()
