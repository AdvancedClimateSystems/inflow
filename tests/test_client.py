import pytest
from inflow import Client


def test_client_init():
    """ Should be able to pass a http connection URI. """
    client = Client('http://user:pass@localhost:8086/databasename')

    assert client.connection.auth == ('user', 'pass')
    assert client.connection.uri == 'http://localhost:8086'
    assert client.connection.db == 'databasename'


def test_client_init_no_auth():
    """ Should be able to parse connection uri without auth. """
    client = Client('http://localhost:8086/databasename')
    assert client.connection.auth is None


def test_client_init_bad_scheme():
    """ Currently we only support the http and https schemes. """
    with pytest.raises(ValueError):
        Client('udp://localhost:8086/databasename')


def test_client_init_no_database_name():
    """ A database name should be specified. """
    with pytest.raises(ValueError):
        Client('https://localhost:8086/')


def test_client_init_bad_uri():
    """ Should throw a ValueError when the given uri is not valid. """
    with pytest.raises(ValueError):
        Client('invalid')
