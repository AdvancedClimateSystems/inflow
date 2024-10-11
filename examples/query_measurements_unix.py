#!/usr/bin/env python

from inflow import Client

client = Client("http://username:pass@localhost:8086", db="databasename")
results = client.query('SELECT * FROM "temperatures"', epoch="s")
