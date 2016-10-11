#!/usr/bin/env python

from inflow import Client
client = Client('http://mon.mijnbaopt.nl:8086/jaapz')
client.write('temperature', value=21.3)
