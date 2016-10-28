#!/usr/bin/env python

from inflow import Client
client = Client('http://username:pass@localhost:8086/databasename')
client.write('temperature', value=21.3)
