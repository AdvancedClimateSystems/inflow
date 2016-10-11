from requests import post

try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse

__all__ = ['Connection']


class Connection:
    """ Represents a connection to an InfluxDB instance. """

    def __init__(self, uri, precision='s'):
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

        self.precision = precision

    @property
    def write_url(self):
        return '{}/write?precision={}&db={}'.format(
            self.uri,
            self.precision,
            self.db
        )

    def write(self, measurement):
        """ Write a single measurement to the InfluxDB API. """
        if type(measurement) is list:
            data = '\n'.join([m.to_line(self.precision) for m in measurement])
        else:
            data = measurement.to_line(self.precision)

        return post(self.write_url, auth=self.auth, data=data)
