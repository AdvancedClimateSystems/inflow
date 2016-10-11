#!/usr/bin/env python

from inflow import Client

client = Client('http://username:pass@localhost:8086/databasename')

client.write(
    'temperature',
    timestamp=1475846182,
    lower_sensor=20.9,
    upper_sensor=23.2
)
