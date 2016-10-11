__all__ = ['dict_to_comma_separated_string']


def dict_to_comma_separated_string(data):
    """ Turns a dict into a comma separated string.

    This:

        {
            'key': 'value',
            'another': 10.0
        }

    Becomes:

        'key=value,another=10.0'
    """
    return ','.join(['{}={}'.format(k, v)
                     for k, v in data.items()])
