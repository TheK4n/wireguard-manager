


<h1 align="center">Wireguard Manager</h1>

<p align="center">
  <a href="https://github.com/TheK4n">
    <img src="https://img.shields.io/github/followers/TheK4n?label=Follow&style=social">
  </a>
  <a href="https://github.com/TheK4n/wireguard-manager">
    <img src="https://img.shields.io/github/stars/TheK4n/wireguard-manager?style=social">
  </a>
</p>

* [Project description](#chapter-0)
* [Requirements](#chapter-1)
* [Installation](#chapter-2)
* [Usage](#chapter-3)


<a id="chapter-0"></a>
## Project description 

Wireguard manager with Telegram integration


<a id="chapter-1"></a>
## Requirements

* **wg**  - Wireguard CLI
* **qrencode** - Generate qrcode
<a id="chapter-2"></a>
## Installation

```.env``` example:
```bash
TOKEN=123456789:ABCDEFG  # tg bot token
ADMIN=123456789  # your tg id
```

Clone repository and installing dependencies:

```bash
git clone https://github.com/TheK4n/wireguard-manager.git
cd wireguard-manager
make init
wg-manager init
make tg  # initialize tg bot
```

<a id="chapter-3"></a>
## Usage
```bash
wg-manage add "client_name"  # adds client, shows qrcode
```
```bash
wg-manage get "client_name"  # shows client qrcode
```
```bash
wg-manage rm "client_name"  # removes client
```



<h1 align="center"><a href="#top">▲</a></h1>
