from .write import WriteMixin

__all__ = ['Session']


class Session(WriteMixin):
    def __init__(self, connection, autocommit_every=None):
        self.connection = connection
        """ The connection where the measurements will be written to. """

        self.autocommit_every = autocommit_every
        """ When set to a number, this session will autocommit whenever the
        amount of cached measurements exceeds this number. """

        self.measurements = []
        """ Contains all uncommitted measurements. """

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        self.commit()

    def write_func(self, measurement):
        if type(measurement) is list:
            self.measurements.extend(measurement)
        else:
            self.measurements.append(measurement)

        if self.autocommit_every is not None:
            if len(self.measurements) >= self.autocommit_every:
                self.commit()

    def commit(self):
        """ Write out all cached measurements at once. """
        self.connection.write(self.measurements)
        self.measurements = []
