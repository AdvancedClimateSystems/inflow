.. _measurements:

Writing Measurements
====================

Examples
--------

You can write measurements in a few different ways, but writing a single
"temperature" measurement is as simple as:

.. code:: python

    from inflow import Client
    client = Client('http://username:pass@localhost:8086/databasename')
    client.write('temperature', value=21.3)

No time is specified in the above example, so inflow automatically set's the
measurement's time to the current time. Also, no tags are provided to the
``write`` method, so no tags are attached to the measurement.

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
        {'value': 21.3, 'timestamp': 1475845863},
        {'value': 20.1, 'timestamp': 1475846182}
    ])

In the above examples, every ``write`` call will issue a direct call to the
InfluxDB API. You can accumulate measurements and write them all at once using
:ref:`sessions`.

Multiple Values
---------------

In all the examples above, we assume there is only one actual ``value`` for
the given measurements. However, InfluxDB supports having an arbitrary amount
of values for every measurements. This is also possible in Inflow:

.. code:: python

    from inflow import Client

    client.write(
        'temperature',
        timestamp=1475846182,
        lower_sensor=20.9,
        upper_sensor=23.2
    )

This will create a measurement with the ``lower_sensor`` and ``upper_sensor``
values. This method also works when manually writing ``Measurement``
instances, and when writing lists of dicts.

Precision
---------

Currently, inflow only supports a precision in seconds. This may change in the
future, though.
