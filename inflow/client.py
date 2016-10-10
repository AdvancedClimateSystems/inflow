from collections import namedtuple

try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse

__all__ = ['Client']


Connection = namedtuple('Connection', ['auth', 'uri', 'db'])


class Client:
    """ The InfluxDB client. """

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

        uri = '{}://{}'.format(
            parsed.scheme,
            parsed.hostname
        )

        if parsed.port is not None:
            uri += ':{}'.format(parsed.port)

        self.connection = Connection(
            auth=((parsed.username, parsed.password)
                  if parsed.username is not None
                  else None),
            uri='{}://{}:{}'.format(
                parsed.scheme,
                parsed.hostname,
                parsed.port
            ),
            db=parsed.path[1:]
        )
