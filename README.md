


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
* **psql >= 13.6** - PostgreSQL
* **curl**
* **qrencode** - Generate qrcode
<a id="chapter-2"></a>
## Installation

```.env``` example:
```bash
TOKEN=123456789:ABCDEFG  # tg bot token
ADMIN=123456789  # your tg id
WG_PORT=51830
PG_HOST=127.0.0.1
PG_DB=wg
PG_USER=wg_admin
PG_PASS=1234
PG_PORT=5432
```

Clone repository and installing dependencies:

```bash
git clone https://github.com/TheK4n/wireguard-manager.git
cd wireguard-manager
pip3 install -r requirements.txt
bash scripts/init.sh  # initialize wireguard
```

<a id="chapter-3"></a>
## Usage



<h1 align="center"><a href="#top">▲</a></h1>
