from .connection import Connection
from .session import Session
from .write import WriteMixin

__all__ = ['Client']


class Client(WriteMixin):
    """ The InfluxDB client. """

    def __init__(self, uri, precision='s', retention_policy=None, timeout=None):
        self.connection = Connection(uri, precision, retention_policy, timeout)

    def write_func(self, measurement, **kwargs):
        return self.connection.write(measurement, **kwargs)

    def session(self, autocommit_every=None, retention_policy=None):
        return Session(self.connection, autocommit_every, retention_policy)

    def query(self, query, epoch=None):
        return self.connection.query(query, epoch)
