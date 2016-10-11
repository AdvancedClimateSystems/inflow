from .connection import Connection
from .session import Session
from .write import WriteMixin

__all__ = ['Client']


class Client(WriteMixin):
    """ The InfluxDB client. """

    def __init__(self, uri):
        self.connection = Connection(uri)

    def write_func(self, measurement):
        self.connection.write(measurement)

    def session(self, autocommit_every=None):
        return Session(self.connection, autocommit_every)
