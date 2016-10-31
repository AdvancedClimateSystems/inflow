.. _querying:

Querying
========

Inflow contains a minimal abstraction over the ``/query`` endpoint of the
InfluxDB HTTP API.

Getting a list of measurements is as simple as:

.. literalinclude:: ../../examples/query_measurements.py
    :language: python

Say you've got a measurement called ``temperature`` (just as in the example
above), which contains a ``value`` field, a ``location`` tag, and contains 2
values. To query that data you would call the ``query`` method as described in
the above example, which will return a list with the following structure:

.. code-block:: python

    [
        {
            'name': 'temperature',
            'values': [
                {
                    'time': '2016-01-10T00:01:00Z',
                    'value': 21.0,
                    'location': 'groningen'
                },
                {
                    'time': '2016-01-10T00:02:00Z',
                    'value': 23.0,
                    'location': 'groningen'
                }
            ]
        }
    ]

You can use any query type that InfluxDB allows, and it should work.

Unix Timestamps
---------------

By default, InfluxDB will return timestamps in RFC3339 format with nanosecond
precision. If you want instead want unix timestamps (in a specific precision),
you can use the ``epoch`` kwarg, like this:

.. literalinclude:: ../../examples/query_measurements_unix.py
    :language: python

In this example, we specify that we want unix timestamps, in seconds. The
``epoch`` argument accepts one of ``h``, ``m``, ``s``, ``ms``, ``u`` and
``ns``.
