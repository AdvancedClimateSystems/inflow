.. image:: https://travis-ci.org/AdvancedClimateSystems/inflow.svg?branch=develop
    :target: https://travis-ci.org/AdvancedClimateSystems/inflow

.. image:: https://coveralls.io/repos/github/AdvancedClimateSystems/inflow/badge.svg?branch=develop
    :target: https://coveralls.io/github/AdvancedClimateSystems/inflow?branch=develop

Inflow
======

A simple `InfluxDB`_ Python client library. It is an alternative for the
`official InfluxDB Python client library`_.

Inflow officially supports Python 2.7 and up, but the latest Python 3 version
is recommended.

InfluxDB is supported from version 1.0 and up.

Documentation is hosted on `Read the Docs`_.

Source code can be found on `GitHub`_.

.. warning:: This project is still very much in development, stuff might work,
             or not.  API's might change, or even be removed. So be careful.
             This message will be removed once a stable version is released.  

Example
-------

You can write measurements in a few different ways, but writing a single
"temperature" measurement is as simple as:

.. code:: python

    from inflow import Client
    client = Client('http://username:pass@localhost:8086/databasename')
    client.write('temperature', value=21.3)

For more examples and docs on how to use the client, go to :ref:`measurements`
and :ref:`querying`.

Installing
----------

.. code::

    $ pip install inflow

License
-------

Inflow is licensed under `Mozilla Public License`_. © 2016 `Advanced Climate
Systems`_.

.. External References:
.. _Advanced Climate Systems: http://www.advancedclimate.nl/
.. _Mozilla Public License: https://github.com/AdvancedClimateSystems/inflow/blob/master/LICENSE
.. _InfluxDB: https://github.com/influxdata/influxdb
.. _official InfluxDB Python client library: https://github.com/influxdata/influxdb-python
.. _Read the Docs: https://inflow.readthedocs.io/en/latest
.. _GitHub: https://github.com/AdvancedClimateSystems/inflow
