import pytest
from inflow import Client, Measurement

try:
    from unittest.mock import Mock
except:
    from mock import Mock


class TestInit:
    def test_connection(self):
        """ Should be able to pass a http connection URI. """
        client = Client('http://user:pass@localhost:8086/databasename')

        assert client.connection.auth == ('user', 'pass')
        assert client.connection.uri == 'http://localhost:8086'
        assert client.connection.db == 'databasename'

    def test_no_auth(self):
        """ Should be able to parse connection uri without auth. """
        client = Client('http://localhost:8086/databasename')
        assert client.connection.auth is None

    def test_bad_scheme(self):
        """ Currently we only support the http and https schemes. """
        with pytest.raises(ValueError):
            Client('udp://localhost:8086/databasename')

    def test_no_database_name(self):
        """ A database name should be specified. """
        with pytest.raises(ValueError):
            Client('https://localhost:8086/')

    def test_bad_uri(self):
        """ Should throw a ValueError when the given uri is not valid. """
        with pytest.raises(ValueError):
            Client('invalid')


class TestWrite:
    @pytest.fixture
    def client(self):
        return Client('https://user:pass@localhost:8086/testdb')

    @pytest.fixture
    def post(self, monkeypatch):
        post = Mock()
        monkeypatch.setattr('inflow.client.post', post)
        return post

    def test_simple_measurement(self, client, post):
        client.write('temperature', value=21.3, timestamp=1476107241)
        post.assert_called_with(
            'https://localhost:8086/write?db=testdb',
            auth=('user', 'pass'),
            data='temperature value=21.3 1476107241'
        )

    def test_measurement_instance(self, client, post):
        client.write(Measurement(
            'temperature',
            value=21.3,
            timestamp=1476107241
        ))

        post.assert_called_with(
            'https://localhost:8086/write?db=testdb',
            auth=('user', 'pass'),
            data='temperature value=21.3 1476107241'
        )

    def test_measurement_list(self, client, post):
        client.write([
            Measurement(
                'temperature',
                value=32.1,
                timestamp=1476107241
            ),
            Measurement(
                'temperature',
                value=21.9,
                timestamp=1476107319
            )
        ])

        post.assert_called_with(
            'https://localhost:8086/write?db=testdb',
            auth=('user', 'pass'),
            data='temperature value=32.1 1476107241\n'
                 'temperature value=21.9 1476107319'
        )

    def test_measurement_template(self, client, post):
        temperature = {'name': 'temperature'}

        client.write(temperature, [
            {'value': 21.3, 'timestamp': 1476107241},
            {'value': 21.9, 'timestamp': 1476107319}
        ])

        post.assert_called_with(
            'https://localhost:8086/write?db=testdb',
            auth=('user', 'pass'),
            data='temperature value=21.3 1476107241\n'
                 'temperature value=21.9 1476107319'
        )

class TestSession:
    # TODO: write session tests
    pass
