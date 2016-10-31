Error Handling
==============

If you're doing something that the InfluxDB API deems wrong, it will return an
error. These errors can occur when trying to query or write data.  The
exceptions described below wrap the errors returned by the InfluxDB API, and
you should probably make sure you handle them in your code.

Exception types
---------------
.. autoclass:: inflow.InfluxDBException
.. autoclass:: inflow.QueryFailedException
.. autoclass:: inflow.WriteFailedException
.. autoclass:: inflow.DatabaseNotFoundException
.. autoclass:: inflow.UnauthorizedException
.. autoclass:: inflow.ForbiddenException
