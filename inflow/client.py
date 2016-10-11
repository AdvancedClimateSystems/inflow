import six
from requests import post

from .utils import dict_to_comma_separated_string

try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse

__all__ = ['Client', 'Measurement']


class Connection:
    """ Represents a connection to an InfluxDB instance. """

    def __init__(self, uri):
        parsed = urlparse(uri)

        if parsed.hostname is None or\
                parsed.scheme is None:
            raise ValueError('Given URI is invalid.')

        if parsed.scheme not in ['http', 'https']:
            raise ValueError('Given scheme is not supported, should be '
                             'either http or https, while you specified '
                             '{}'.format(parsed.scheme))

        if parsed.path == '' or parsed.path == '/':
            raise ValueError('Should specify a database name.')

        self.uri = '{}://{}'.format(
            parsed.scheme,
            parsed.hostname
        )

        if parsed.port is not None:
            self.uri += ':{}'.format(parsed.port)

        self.auth = ((parsed.username, parsed.password)
                     if parsed.username is not None
                     else None)

        self.db = parsed.path[1:]

    @property
    def write_url(self):
        return '{}/write?db={}'.format(
            self.uri,
            self.db
        )

    def write(self, measurement):
        """ Write a single measurement to the InfluxDB API. """
        if type(measurement) is list:
            data = '\n'.join([m.to_line() for m in measurement])
        else:
            data = measurement.to_line()

        post(self.write_url, auth=self.auth, data=data)


class Measurement:
    """ A measurement that can be written (by the client) to InfluxDB. """
    def __init__(self, name, timestamp=None, tags=None, **values):
        self.name = name
        self.tags = tags
        self.timestamp = timestamp
        self.values = values

    def to_line(self):
        return '{name}{tags} {values} {timestamp}'.format(
            name=self.name,
            tags=(dict_to_comma_separated_string(sorted(self.tags))
                  if self.tags is not None
                  else ''),
            values=dict_to_comma_separated_string(self.values),
            timestamp=self.timestamp
        )


class Client:
    """ The InfluxDB client. """

    def __init__(self, uri):
        self.connection = Connection(uri)

    def write(self, *args, **kwargs):
        """ Write a measurement to InfluxDB. """
        first = args[0]

        if isinstance(first, Measurement):
            self.connection.write(first)

        elif type(first) is dict:
            measurements = []
            for measurement in args[1]:
                merge = first.copy()
                merge.update(measurement)

                measurements.append(Measurement(**merge))
            self.connection.write(measurements)

        elif type(first) is list:
            self.connection.write(first)

        elif isinstance(first, six.string_types):
            self.connection.write(Measurement(
                name=first,
                **kwargs
            ))
