#!/usr/bin/env python

from inflow import Client, Measurement

client = Client('http://username:pass@localhost:8086/databasename')

client.write([
    Measurement(
        name='temperature',
        tags={
            'location': 'groningen',
            'sensor_type': 'ni1000'
        },
        value=21.3,
        timestamp=1475845863
    ),
    Measurement(
        name='temperature',
        tags={
            'location': 'groningen',
            'sensor_type': 'ni1000'
        },
        value=20.1,
        timestamp=1475848864
    )
])
