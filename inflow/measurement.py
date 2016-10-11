from .utils import dict_to_comma_separated_string

__all__ = ['Measurement']


class Measurement:
    """ A measurement that can be written (by the client) to InfluxDB. """

    def __init__(self, name, timestamp=None, tags=None, **values):
        self.name = name
        self.timestamp = timestamp
        self.values = values

        # TODO: sanitize tags (cannot contain certain characters)
        self.tags = tags

    def to_line(self):
        return '{name}{tags} {values} {timestamp}'.format(
            name=self.name,
            tags=(',' + dict_to_comma_separated_string(sorted(self.tags))
                  if self.tags is not None
                  else ''),
            values=dict_to_comma_separated_string(self.values),
            timestamp=self.timestamp
        )
