import six
from functools import partial
from .utils import to_comma_separated_string, escape

__all__ = ['Measurement']


escape_tags = partial(escape, [',', '=', ' '])
escape_measurements = partial(escape, [',', ' '])
escape_string_values = partial(escape, ['"'])


def to_line_value(value):
    """ Adds quotes and escapes the value if it is a string. If the value is
    not a string, it is returned verbatim. """
    if isinstance(value, six.string_types):
        return '"{}"'.format(escape_string_values(value))

    return value


class Measurement:
    """ A measurement that can be written (by the client) to InfluxDB. """

    def __init__(self, name, timestamp=None, tags=None, **values):
        self.name = name
        self.timestamp = timestamp
        self.values = values
        self.tags = tags

    def to_line(self):
        tags = None
        if self.tags is not None:
            tags = sorted([(escape_tags(k), escape_tags(v))
                           for k, v in self.tags.items()])

        values = [(escape_tags(k), to_line_value(v))
                  for k, v in self.values.items()]

        return '{name}{tags} {values} {timestamp}'.format(
            name=escape_measurements(self.name),
            tags=(',' + to_comma_separated_string(tags)
                  if tags is not None
                  else ''),
            values=to_comma_separated_string(values),
            timestamp=self.timestamp
        )
