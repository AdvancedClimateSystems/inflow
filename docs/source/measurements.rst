.. _measurements:

Writing Measurements
====================

Examples
--------

You can write measurements in a few different ways, but writing a single
"temperature" measurement is as simple as:

.. literalinclude:: ../../examples/single_write.py
    :language: python

No time is specified in the above example, so inflow automatically set's the
measurement's time to the current time. Also, no tags are provided to the
``write`` method, so no tags are attached to the measurement.

A more complex example of writing a single measurement:

.. literalinclude:: ../../examples/single_write_more.py
    :language: python

Writing multiple measurements is also possible:

.. literalinclude:: ../../examples/write_multiple_verbose.py
    :language: python

However, this is a bit verbose. That's why you can also do this:

.. literalinclude:: ../../examples/write_multiple_succinct.py
    :language: python

In the above examples, every ``write`` call will issue a direct call to the
InfluxDB API. You can accumulate measurements and write them all at once using
:ref:`sessions`.

.. note:: In every example, we use timestamp ints (in seconds) to specify the
          time for each measurement. You can also set the timestamp to a
          datetime. Inflow will automatically convert both to the right
          precision when writing to InfluxDB.

Multiple Values
---------------

In all the examples above, we assume there is only one actual ``value`` for
the given measurements. However, InfluxDB supports having an arbitrary amount
of values for every measurements. This is also possible in Inflow:

.. code:: python

.. literalinclude:: ../../examples/write_multiple_values.py
    :language: python

This will create a measurement with the ``lower_sensor`` and ``upper_sensor``
values. This method also works when manually writing ``Measurement``
instances, and when writing lists of dicts.

Precision
---------

By default, Inflow assumes the timestamps that are written to InfluxDB are in
seconds. However, you can specify a custom precision when creating the client:

.. literalinclude:: ../../examples/different_precision.py
    :language: python

The precision needs to be one of: `h`, `m`, `s`, `ms`, `u` or `ns`.

Retention policies
------------------

By default, Inflow will write to the database's default retention policy.
However, you can explicitly specify which retention policy your measurements
should be written to:

.. literalinclude:: ../../examples/explicit_retention_policy.py
    :language: python
