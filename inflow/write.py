import six
from .measurement import Measurement

__all__ = ['WriteMixin']


class WriteMixin:
    def write(self, *args, **kwargs):
        """ Write a measurement to InfluxDB. """
        first = args[0]

        retention_policy = kwargs.get('retention_policy', None)
        if 'retention_policy' in kwargs:
            del kwargs['retention_policy']

        if isinstance(first, Measurement):
            return self.write_func(first, retention_policy=retention_policy)

        elif type(first) is dict:
            measurements = []
            for measurement in args[1]:
                merge = first.copy()
                merge.update(measurement)

                measurements.append(Measurement(**merge))
            return self.write_func(measurements,
                                   retention_policy=retention_policy)

        elif type(first) is list:
            return self.write_func(first, retention_policy=retention_policy)

        elif isinstance(first, six.string_types):
            return self.write_func(
                Measurement(
                    name=first,
                    **kwargs
                ),
                retention_policy=retention_policy
            )
        else:
            raise ValueError('Can\'t create measurements based on the given arguments.')
