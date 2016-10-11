import six
from .measurement import Measurement

__all__ = ['WriteMixin']


class WriteMixin:
    def write(self, *args, **kwargs):
        """ Write a measurement to InfluxDB. """
        first = args[0]

        if isinstance(first, Measurement):
            return self.write_func(first)

        elif type(first) is dict:
            measurements = []
            for measurement in args[1]:
                merge = first.copy()
                merge.update(measurement)

                measurements.append(Measurement(**merge))
            return self.write_func(measurements)

        elif type(first) is list:
            return self.write_func(first)

        elif isinstance(first, six.string_types):
            return self.write_func(Measurement(
                name=first,
                **kwargs
            ))
        else:
            raise ValueError('Can\'t create measurements based on the given arguments.')
