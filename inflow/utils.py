import six

__all__ = ['to_comma_separated_string', 'escape']


def to_comma_separated_string(data):
    """ Turns list of key value pairs into a comma separated string.

    This:

        [
            ('key', 'value'),
            ('another', 10.0)
        ]

    Becomes:

        'key=value,another=10.0'
    """
    return ','.join(['{}={}'.format(k, v)
                     for k, v in data])


def escape(characters, string):
    """ Escapes the given list of characters in the given string.

    If a non-string is given to be escaped, we return the non-string without
    escaping.
    """
    if not isinstance(string, six.string_types):
        return string

    for char in characters:
        string = string.replace(char, '\\' + char)
    return string
