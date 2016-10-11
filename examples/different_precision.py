#!/usr/bin/env python

from inflow import Client
client = Client('http://mon.mijnbaopt.nl:8086/jaapz', precision='ms')
client.write('temperature', value=21.3, timestamp=1476191999000)
