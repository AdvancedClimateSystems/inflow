#!/usr/bin/env python

from inflow import Client

client = Client('http://username:pass@localhost:8086/databasename')

client.write(
    'temperature',
    tags={
        'location': 'groningen',
        'sensor_type': 'ni1000'
    },
    value=21.3,
    timestamp=1475845863
)
