#!/usr/bin/env python

from inflow import Client

client = Client('http://username:pass@localhost:8086/databasename')

temperature = dict(
    name='temperature',
    tags={
        'location': 'groningen',
        'sensor_type': 'ni1000'
    }
)

client.write(temperature, [
    {'value': 21.3, 'timestamp': 1475845863},
    {'value': 20.1, 'timestamp': 1475846182}
])
