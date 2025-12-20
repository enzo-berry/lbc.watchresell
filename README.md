# lbc.watchresell
⚠️ Disclaimer: This source is outdated and may no longer function as intended. Use at your own risk.

## Overview
A python project to scrap [leboncoin](https://www.leboncoin.fr) new articles and sending it to a discord channel.

The anti-scrapping system [datadome](https://datadome.co) is bypassed using [Capsolver](https://www.capsolver.com).

## How to use
Build the Docker image from the repo :
```
docker build -f Dockerfile -t lbc-watchresell:v2 ./
```
Create the container :
```
docker create \
-v <path_to_config_folder>:/usr/src/lbc-watchresell/config \
--name lbc \
lbc-watchresell:v2
```
You have to mount the ***config***  folder with the following files in it:
- config.py
  - User agent to emulate the browser
  - proxy (if needed)
  - capsolver API key (if your IP become evil)
  - Discord bot token
  - Check period (in second) -> time between to add check
- lbc.json
  - URL of your LBC search
  - Discord channel id
