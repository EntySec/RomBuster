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

    def start(self):
        if self.args.list:
            with open(self.args.list, 'r') as f:
                lines = f.read().strip().split('\n')
                for line in lines:
                    self.exploit(line)
            for credential in self.credentials:
                self.print_success(credential)
        elif self.args.address:
            self.exploit(self.args.address)
            for credential in self.credentials:
                self.print_success(credential)
        else:
            self.print_error("No list or address specified!")

def main():
    cli = RomBusterCLI()
    cli.start()
