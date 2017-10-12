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

        self.temporary_retention_policy = None
        """ The retention policy this session should commit the measurements to.
        Clears on commit. """

        self.measurements = []
        """ Contains all uncommitted measurements. """

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        self.commit()

    def write_func(self, measurement, **kwargs):
        self.temporary_retention_policy = kwargs.get('retention_policy', None)
        if 'retention_policy' in kwargs:
            del kwargs['retention_policy']

        if type(measurement) is list:
            self.measurements.extend(measurement)
        else:
            self.measurements.append(measurement)

        if self.autocommit_every is not None:
            if len(self.measurements) >= self.autocommit_every:
                self.commit()

    def commit(self):
        """ Write out all cached measurements at once. """
        retention_policy = self.retention_policy
        if self.temporary_retention_policy is not None:
            retention_policy = self.temporary_retention_policy

        self.connection.write(self.measurements,
                              retention_policy=retention_policy)
        self.measurements = []
        self.temporary_retention_policy = None
