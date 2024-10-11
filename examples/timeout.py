#!/usr/bin/env python

from inflow import Client

client = Client("http://username:pass@localhost:8086", db="databasename", timeout=0.01)

client.write("temperature", value=21.3)
