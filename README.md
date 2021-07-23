# RomBuster

<p>
    <a href="https://entysec.netlify.app">
        <img src="https://img.shields.io/badge/developer-EntySec-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/RomBuster">
        <img src="https://img.shields.io/badge/language-Python-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/RomBuster/stargazers">
        <img src="https://img.shields.io/github/stars/EntySec/RomBuster?color=yellow">
    </a>
</p>

RomBuster is a router exploitation tool that allows to disclosure network router admin password.

## Features

* Exploits vulnerabilities in most popular routers such as `D-Link`, `Zyxel`, `TP-Link` and `Huawei`.
* Optimized to exploit multiple routers at one time from list.
* Simple CLI and API usage.

## Installation

```shell
pip3 install git+https://github.com/EntySec/RomBuster
```

## Basic usage

To use RomBuster just type `rombuster` in your terminal.

```
usage: rombuster [-h] [-o OUTPUT] [-i INPUT] [-a ADDRESS] [--shodan SHODAN]
                 [--zoomeye ZOOMEYE] [-p PAGES]

RomBuster is a router exploitation tool that allows to disclosure network
router admin password.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output result to file.
  -i INPUT, --input INPUT
                        Input file of addresses.
  -a ADDRESS, --address ADDRESS
                        Single address.
  --shodan SHODAN       Shodan API key for exploiting devices over Internet.
  --zoomeye ZOOMEYE     ZoomEye API key for exploiting devices over Internet.
  -p PAGES, --pages PAGES
                        Number of pages you want to get from ZoomEye.
```

### Examples

**Exploiting single router**

Let's hack my router just for fun.

```shell
rombuster -a 192.168.99.1
```

**Exploiting routers from Internet**

Let's try to use Shodan search engine to exploit routers over Internet.

```shell
rombuster --shodan PSKINdQe1GyxGgecYz2191H2JoS9qvgD
```

**NOTE:** Given Shodan API key (`PSKINdQe1GyxGgecYz2191H2JoS9qvgD`) is my PRO API key, you can use this key or your own, be free to use all our resources for free :)

**Exploiting routers from input file**

Let's try to use opened database of routers.

```shell
rombuster -i routers.txt -o passwords.txt
```

**NOTE:** It will exploit all routers in `routers.txt` list by their addresses and save all obtained passwords to `passwords.txt`.

## API usage

RomBuster also has their own Python API that can be invoked by importing RomBuster to your code.

```python
from rombuster import RomBuster
```

### Basic functions

There are all RomBuster basic functions that can be used to exploit specified router.

* `exploit(address)` - Exploit single router by given address.

### Examples

**Exploiting single router**

```python
from rombuster import RomBuster

rombuster = RomBuster()
creds = rombuster.exploit('192.168.99.1')

print(creds)
```

## All tools

<p>
    <a href="https://github.com/EntySec/Ghost">
        <img src="https://img.shields.io/badge/EntySec-Ghost-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/HatSploit">
        <img src="https://img.shields.io/badge/EntySec-HatSploit-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/HatVenom">
        <img src="https://img.shields.io/badge/EntySec-HatVenom-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/RomBuster">
        <img src="https://img.shields.io/badge/EntySec-RomBuster-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/CamRaptor">
        <img src="https://img.shields.io/badge/EntySec-CamRaptor-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/CamOver">
        <img src="https://img.shields.io/badge/EntySec-CamOver-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/Shreder">
        <img src="https://img.shields.io/badge/EntySec-Shreder-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/Paranoid">
        <img src="https://img.shields.io/badge/EntySec-Paranoid-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/membrane">
        <img src="https://img.shields.io/badge/EntySec-membrane-f34c79.svg">
    </a>
    <a href="https://github.com/EntySec/pwny">
        <img src="https://img.shields.io/badge/EntySec-pwny-448eff.svg">
    </a>
</p>
