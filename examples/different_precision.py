#!/usr/bin/env python

from inflow import Client

client = Client(
    "http://username:pass@localhost:8086", db="databasename", precision="ms"
)
client.write("temperature", value=21.3, timestamp=1476191999000)
