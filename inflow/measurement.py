import six

from functools import partial
from datetime import datetime

from .utils import to_comma_separated_string, escape

__all__ = ['Measurement']

EPOCH = datetime(1970, 1, 1)

PRECISION_MULTIPLIERS = {
    'ns': 10**9,
    'u': 1000000.0,
    'ms': 1000.0,
    's': 1.0,
    'm': 0.017,
    'h': 0.000278
}

escape_tags = partial(escape, [',', '=', ' '])
escape_measurements = partial(escape, [',', ' '])
escape_string_values = partial(escape, ['"'])


def to_line_value(value):
    """ Adds quotes and escapes the value if it is a string. If the value is
    not a string, it is returned verbatim. """
    if isinstance(value, six.string_types):
        return '"{}"'.format(escape_string_values(value))

    return value


def to_timestamp(timestamp):
    """ Converts a datetime object to timestamp. Needed for py3 and py2 cross
    compat."""
    try:
        return timestamp.timestamp()

    # Python 2 does not have timestamp method, so we use a surrogate.
    except AttributeError:
        return (timestamp - EPOCH).total_seconds()


class Measurement:
    """ A measurement that can be written (by the client) to InfluxDB. """

    def __init__(self, name, timestamp=None, tags=None, **values):
        self.name = name
        self.values = values
        self.tags = tags

        if timestamp is None:
            self.timestamp = datetime.now()
        elif isinstance(timestamp, six.integer_types):
            self.timestamp = datetime.fromtimestamp(timestamp)
        else:
            self.timestamp = timestamp

    def to_line(self, precision='s'):
        tags = None
        if self.tags is not None:
            tags = sorted([(escape_tags(k), escape_tags(v))
                           for k, v in self.tags.items()])

        values = [(escape_tags(k), to_line_value(v))
                  for k, v in self.values.items()]

        multiplier = PRECISION_MULTIPLIERS[precision]

        return '{name}{tags} {values} {timestamp}'.format(
            name=escape_measurements(self.name),
            tags=(',' + to_comma_separated_string(tags)
                  if tags is not None
                  else ''),
            values=to_comma_separated_string(values),
            timestamp=int(to_timestamp(self.timestamp) * multiplier)
        )
