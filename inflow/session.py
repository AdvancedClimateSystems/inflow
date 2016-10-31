from .write import WriteMixin

__all__ = ['Session']


class Session(WriteMixin):
    def __init__(self, connection, autocommit_every=None, retention_policy=None):
        self.connection = connection
        """ The connection where the measurements will be written to. """

        self.autocommit_every = autocommit_every
        """ When set to a number, this session will autocommit whenever the
        amount of cached measurements exceeds this number. """

        self.retention_policy = retention_policy
        """ The retention policy this session should write to. Overrides the
        connection's retention policy. """

        self.measurements = []
        """ Contains all uncommitted measurements. """

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        self.commit()

    def write_func(self, measurement, **kwargs):
        if type(measurement) is list:
            self.measurements.extend(measurement)
        else:
            self.measurements.append(measurement)

        if self.autocommit_every is not None:
            if len(self.measurements) >= self.autocommit_every:
                self.commit()

    def commit(self):
        """ Write out all cached measurements at once. """
        self.connection.write(self.measurements,
                              retention_policy=self.retention_policy)
        self.measurements = []
