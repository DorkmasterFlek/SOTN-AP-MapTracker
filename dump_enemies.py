#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Dump enemysanity and dropsanity location info.

import json
import os
import re
import sys

sys.path.append(os.path.expanduser('~/Archipelago-SOTN'))

from worlds.sotn import location_table

def pretty_name(key):
    name = re.sub(r'(\w)\(', r'\1 (', key.title())
    name = name.replace('Ii', 'II')  # Fix Akmodan II
    return name.strip()

enemies = {k: v for k, v in location_table.items() if k.startswith('Enemysanity:')}
ekeys = sorted(enemies.keys(), key=lambda x: int(x[13:].split('-')[0]))
drops = {k: v for k, v in location_table.items() if k.startswith('Dropsanity:')}
dkeys = sorted(drops.keys(), key=lambda x: int(x[12:].split('-')[0]))

for k in ekeys:
    l = k[13:].split('-')
    i = int(l[0])
    item = {
        "name": pretty_name(k),
        "type": "toggle",
        "img": "images/items/sanity_checked.png",
        "disabled_img": "images/items/sanity_unchecked.png",
        "codes": f"enemysanity,enemysanity{i}",
    }
    # print(json.dumps(item, indent=4) + ',')
    print(f'"{k}": {enemies[k].location_id % 1000},')

for k in dkeys:
    l = k[12:].split('-')
    i = int(l[0])
    item = {
        "name": pretty_name(k),
        "type": "toggle",
        "img": "images/items/sanity_checked.png",
        "disabled_img": "images/items/sanity_unchecked.png",
        "codes": f"dropsanity,dropsanity{i}",
    }
    # print(json.dumps(item, indent=4) + ',')
    print(f'"{k}": {drops[k].location_id % 1000},')
