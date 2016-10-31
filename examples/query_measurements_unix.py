#!/usr/bin/env python

from inflow import Client

client = Client('http://username:pass@localhost:8086/databasename')
results = client.query('SELECT * FROM "temperatures"', epoch='s')
