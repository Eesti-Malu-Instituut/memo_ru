#!/usr/bin/env python
 
import yaml

with open("all_utf8_short.yaml", "r") as stream:
    try:
        print('FOOOOoooo')
        print(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print('BAZzz')
        print(exc)
