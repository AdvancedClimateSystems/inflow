from .connection import Connection
from .session import Session
from .write import WriteMixin

__all__ = ['Client']


class Client(WriteMixin):
    """ The InfluxDB client. """

    def __init__(self, uri, precision='s'):
        self.connection = Connection(uri, precision)

    def write_func(self, measurement):
        return self.connection.write(measurement)

    def session(self, autocommit_every=None):
        return Session(self.connection, autocommit_every)
