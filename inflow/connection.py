from requests import post, get
from six.moves.urllib.parse import urlparse, quote_plus

from .exceptions import (QueryFailedException, WriteFailedException,
                         DatabaseNotFoundException, UnauthorizedException,
                         ForbiddenException)

__all__ = ['Connection']

# All these types of queries should issue a GET request.
GET_QUERIES = ['SELECT', 'SHOW']


def get_method(query):
    """ Determines which method should be used to execute this query.

    These query types should be issues using a GET:

      * SELECT
      * SHOW

    These query types should be issues using a POST:

      * SELECT INTO
      * ALTER
      * CREATE
      * DELETE
      * DROP
      * GRANT
      * KILL
      * REVOKE
    """
    if 'INTO' not in query:
        for word in GET_QUERIES:
            if word in query:
                return get

    return post


def parse_query_response(response):
    """ Parses the query response and returns a list of response objects. """
    retval = []
    data = response.json()
    series = data['results'][0]['series']

    for s in series:
        parsed = dict(
            name=s['name'],
            values=[]
        )

        for v in s['values']:
            parsed['values'].append({
                key: value
                for key, value in zip(s['columns'], v)
            })

        retval.append(parsed)

    return retval


class Connection:
    """ Represents a connection to an InfluxDB instance. """

    def __init__(self, uri, precision='s', retention_policy=None):
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
        self.retention_policy = retention_policy

    def get_write_url(self, retention_policy=None):
        """ Returns the url needed to write measurements to InfluxDB. """
        url = '{}/write?precision={}&db={}'.format(
            self.uri,
            self.precision,
            self.db
        )

        if retention_policy is not None:
            url = '{}&rp={}'.format(url, retention_policy)
        elif self.retention_policy is not None:
            url = '{}&rp={}'.format(url, self.retention_policy)

        return url

    def get_query_url(self, query, epoch):
        """ Returns the url needed to query measurements from InfluxDB.  """
        url = '{}/query?db={}&q={}'.format(
            self.uri,
            self.db,
            quote_plus(query)
        )

        if epoch is not None:
            if epoch not in ['h', 'm', 's', 'ms', 'u', 'ns']:
                raise ValueError('Invalid epoch provided, must be one of '
                                 'h, m, s, ms, u or ns.')

            url = '{}&epoch={}'.format(url, epoch)

        return url

    def write(self, measurement, retention_policy=None):
        """ Write a single measurement to the InfluxDB API. """
        if type(measurement) is list:
            data = '\n'.join([m.to_line(self.precision) for m in measurement])
        else:
            data = measurement.to_line(self.precision)

        rv = post(self.get_write_url(retention_policy), auth=self.auth,
                  data=data)

        error = rv.json().get('error', None)

        if rv.status_code == 400 or rv.status_code == 500:
            raise WriteFailedException(error)
        elif rv.status_code == 401:
            raise UnauthorizedException(error)
        elif rv.status_code == 403:
            raise ForbiddenException(error)
        elif rv.status_code == 404:
            raise DatabaseNotFoundException(error)

    def query(self, query, epoch=None):
        """ Execute a query on InfluxDB. """
        method = get_method(query)
        rv = method(self.get_query_url(query, epoch), auth=self.auth)

        error = rv.json().get('error', None)

        if rv.status_code == 400:
            raise QueryFailedException(error)
        elif rv.status_code == 401:
            raise UnauthorizedException(error)
        elif rv.status_code == 403:
            raise ForbiddenException(error)

        return parse_query_response(rv)
