.. _sessions:

Sessions
========

In the examples listed in :ref:`measurements`, every call to ``write`` will
issue a direct call to the InfluxDB API. There might be situations where you'd
want to accumulate measurements and write them all at once. That's what
sessions are for:

.. code:: python

    from inflow import Client

    client = Client('http://username:pass@localhost:8086/databasename')
    session = client.session()

    session.write('temperature', value=23.1, timestamp=1475848864)
    session.write('temperature', value=25.0, timestamp=1475849823)

    session.commit()

In the above example, a session is created in which we issue our ``write``
calls. After doing some ``write`` calls, we call ``commit`` on the session.
This will issue the write to the InfluxDB API. If ``commit`` isn't called on
the sessions, the data given in the ``write``'s will be lost.

.. note:: The session's ``write`` method works exactly the same as that of the
          normal client.

As a Context Manager
--------------------

You can also use the session as a context manager:

.. code:: python

    from inflow import Client

    client = Client('http://username:pass@localhost:8086/databasename')

    with client.session() as session:
        session.write('temperature', value=23.1, timestamp=1475848864)
        session.write('temperature', value=25.0, timestamp=1475849823)

When the context manager exits, the session is automatically committed.

Autocommitting
--------------

You can also have the session autocommit after a certain amount of ``write``
calls, using ``autocommit_every``:

.. code:: python
    
    from inflow import Client

    client = Client('http://username:pass@localhost:8086/databasename')
    session = client.session(autocommit_every=5)

    session.write('temperature', value=23.1, timestamp=1475848864)
    session.write('temperature', value=25.0, timestamp=1475849823)
    session.write('temperature', value=22.9, timestamp=1475849825)
    session.write('temperature', value=28.2, timestamp=1475849912)

    # This next write call will trigger the autocommit.
    session.write('temperature', value=25.1, timestamp=1475849999)
