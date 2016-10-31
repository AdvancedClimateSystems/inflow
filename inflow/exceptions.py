__all__ = ['InfluxDBException', 'QueryFailedException', 'WriteFailedException',
           'DatabaseNotFoundException']


class InfluxDBException(Exception):
    """ Generic exception for InfluxDB HTTP error's, all other exceptions
    subclass from this one.

    The message in this exception (and it's subclasses) is the raw error
    message returned by the InfluxDB HTTP API.
    """
    pass


class QueryFailedException(InfluxDBException):
    """ Thrown when a query is rejected by the API. For example, this happens
    when you have a syntactically incorrect query.  """
    pass


class WriteFailedException(InfluxDBException):
    """ Thrown when a write is rejected by the API. """
    pass


class DatabaseNotFoundException(InfluxDBException):
    """ Thrown when trying to write to a non-existing database. """
    pass
