.. _the_client:

The Client
==========

Writing Measurements
--------------------

You can write measurements in a few different ways, but writing a single
"temperature" measurement is as simple as:

.. code:: python

    from inflow import Client
    client = Client('http://username:pass@localhost:8086/databasename')
    client.write('temperature', value=21.3)

No time is specified in the above example, so inflow automatically set's the
measurement's time to the current time. Also, no tags are provided to the
`write` method, so no tags are attached to the measurement.

A more complex example of writing a single measurement:

.. code:: python

    from inflow import Client

    client = Client('http://username:pass@localhost:8086/databasename')

    client.write(
        'temperature'
        tags={
            'location': 'groningen',
            'sensor_type': 'ni1000'
        },
        value=21.3,
        timestamp=1475845863
    )

Writing multiple measurements is also possible:

.. code:: python

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

However, this is a bit verbose. That's why you can also do this:

.. code:: python

    from inflow import Client, Measurement

    client = Client('http://username:pass@localhost:8086/databasename')

    temperature = Measurement(
        name='temperature',
        tags={
            'location': 'groningen',
            'sensor_type': 'ni1000'
        }
    )

    client.write(temperature, [
        (21.3, 1475845863),
        (20.1, 1475845863)
    ])

Precision
---------

Currently, inflow only supports a precision in seconds. This may change in the
future, though.


