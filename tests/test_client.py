import json
import pytest
from datetime import datetime
from inflow import Client, Measurement

try:
    from unittest.mock import Mock
except:
    from mock import Mock


@pytest.fixture
def client():
    return Client('https://user:pass@localhost:8086/testdb')


@pytest.fixture
def post(monkeypatch):
    post = Mock()
    response_mock = Mock()
    response_mock.json.return_value = json.loads("""{
        "results": [{
            "series": []
        }]
    }""")
    post.return_value = response_mock
    monkeypatch.setattr('inflow.connection.post', post)
    return post


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

    def test_no_port(self):
        """ Should be able to not provide a port. """
        client = Client('http://localhost/databasename')
        assert client.connection.uri == 'http://localhost'

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
    def test_simple_measurement(self, client, post):
        client.write('temperature', value=21.3, timestamp=1476107241)
        post.assert_called_with(
            'https://localhost:8086/write?precision=s&db=testdb',
            auth=('user', 'pass'),
            data='temperature value=21.3 1476107241'
        )

    def test_explicit_retention_policy(self, post):
        client = Client('https://user:pass@localhost:8086/testdb',
                        retention_policy='rp_four_weeks')
        client.write('temperature', value=21.3, timestamp=1476107241)
        post.assert_called_with(
            'https://localhost:8086/write?precision=s&db=testdb&rp=rp_four_weeks',
            auth=('user', 'pass'),
            data='temperature value=21.3 1476107241'
        )

    def test_sorted_tags(self, client, post):
        client.write('temperature', tags={'b': 'tag', 'a': 'tag'}, value=21.3,
                     timestamp=1476107241)

        post.assert_called_with(
            'https://localhost:8086/write?precision=s&db=testdb',
            auth=('user', 'pass'),
            data='temperature,a=tag,b=tag value=21.3 1476107241'
        )

    def test_escaped_tags(self, client, post):
        client.write('temperature', tags={'a,=b ': 'a,=b '}, value=21.3,
                     timestamp=1476107241)

        post.assert_called_with(
            'https://localhost:8086/write?precision=s&db=testdb',
            auth=('user', 'pass'),
            data='temperature,a\\,\\=b\\ =a\\,\\=b\\  value=21.3 1476107241'
        )

    def test_escaped_measurements(self, client, post):
        client.write('temp er,ature', value=21.3, timestamp=1476107241)

        post.assert_called_with(
            'https://localhost:8086/write?precision=s&db=testdb',
            auth=('user', 'pass'),
            data='temp\\ er\\,ature value=21.3 1476107241'
        )

    def test_escaped_string_values(self, client, post):
        client.write('temperature', value='well, a pretty nice "temperature"',
                     timestamp=1476107241)

        post.assert_called_with(
            'https://localhost:8086/write?precision=s&db=testdb',
            auth=('user', 'pass'),
            data='temperature value="well, a pretty nice \\"temperature\\"" 1476107241'
        )

    def test_measurement_instance(self, client, post):
        client.write(Measurement(
            'temperature',
            value=21.3,
            timestamp=1476107241
        ))

        post.assert_called_with(
            'https://localhost:8086/write?precision=s&db=testdb',
            auth=('user', 'pass'),
            data='temperature value=21.3 1476107241'
        )

    def test_measurement_no_timestamp(self):
        measurement = Measurement(
            'temperature',
            value=21.3
        )

        assert measurement.timestamp

    def test_measurement_datetime(self, client, post):
        client.write(Measurement(
            'temperature',
            value=21.3,
            timestamp=datetime.fromtimestamp(1476107241)
        ))

        post.assert_called_with(
            'https://localhost:8086/write?precision=s&db=testdb',
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
            'https://localhost:8086/write?precision=s&db=testdb',
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
            'https://localhost:8086/write?precision=s&db=testdb',
            auth=('user', 'pass'),
            data='temperature value=21.3 1476107241\n'
                 'temperature value=21.9 1476107319'
        )

    def test_measurement_bad_input(self, client):
        with pytest.raises(ValueError):
            client.write(1234)


class TestSession:
    def test_write_to_session(self, client, post):
        session = client.session()

        session.write('temperature', value=23.1, timestamp=1475848864)
        session.write('temperature', value=25.0, timestamp=1475849823)

        session.commit()

        post.assert_called_with(
            'https://localhost:8086/write?precision=s&db=testdb',
            auth=('user', 'pass'),
            data='temperature value=23.1 1475848864\n'
                 'temperature value=25.0 1475849823'
        )

    def test_session_as_context_manager(self, client, post):
        with client.session() as session:
            session.write('temperature', value=23.1, timestamp=1475848864)
            session.write('temperature', value=25.0, timestamp=1475849823)

        post.assert_called_with(
            'https://localhost:8086/write?precision=s&db=testdb',
            auth=('user', 'pass'),
            data='temperature value=23.1 1475848864\n'
                 'temperature value=25.0 1475849823'
        )

    def test_session_autocommit_every(self, client, post):
        session = client.session(autocommit_every=5)

        session.write('temperature', value=23.1, timestamp=1475848864)
        session.write('temperature', value=25.0, timestamp=1475849823)
        session.write('temperature', value=22.9, timestamp=1475849825)
        session.write('temperature', value=28.2, timestamp=1475849912)

        post.assert_not_called()

        # This next write call will trigger the autocommit.
        session.write('temperature', value=25.1, timestamp=1475849999)

        post.assert_called_with(
            'https://localhost:8086/write?precision=s&db=testdb',
            auth=('user', 'pass'),
            data='temperature value=23.1 1475848864\n'
                 'temperature value=25.0 1475849823\n'
                 'temperature value=22.9 1475849825\n'
                 'temperature value=28.2 1475849912\n'
                 'temperature value=25.1 1475849999'
        )

    def test_session_autocommit_every_list(self, client, post):
        session = client.session(autocommit_every=5)

        temperature = {'name': 'temperature'}

        session.write(temperature, [
            {'name': 'temperature', 'value': 23.1, 'timestamp': 1475848864},
            {'name': 'temperature', 'value': 25.0, 'timestamp': 1475849823},
            {'name': 'temperature', 'value': 22.9, 'timestamp': 1475849825},
            {'name': 'temperature', 'value': 28.2, 'timestamp': 1475849912},
            {'name': 'temperature', 'value': 25.1, 'timestamp': 1475849999},
            {'name': 'temperature', 'value': 29.3, 'timestamp': 1475859999}
        ])

        post.assert_called_with(
            'https://localhost:8086/write?precision=s&db=testdb',
            auth=('user', 'pass'),
            data='temperature value=23.1 1475848864\n'
                 'temperature value=25.0 1475849823\n'
                 'temperature value=22.9 1475849825\n'
                 'temperature value=28.2 1475849912\n'
                 'temperature value=25.1 1475849999\n'
                 'temperature value=29.3 1475859999'
        )


@pytest.fixture
def get(monkeypatch):
    get = Mock()
    response_mock = Mock()
    response_mock.json.return_value = json.loads("""{
        "results": [{
            "series": [{
                "name": "temperatures",
                "columns": ["time", "value", "location"],
                "values": [
                    ["2016-01-01T00:01:00Z", 20.1, "groningen"],
                    ["2016-01-01T00:02:00Z", 23.0, "groningen"]
                ]
            }]
        }]
    }""")
    get.return_value = response_mock
    monkeypatch.setattr('inflow.connection.get', get)
    return get


class TestQuery:
    def test_get_measurements(self, client, get):
        """ Should be able to parse resulting measurements into a nice list of
        dicts.

        InfluxDB returns this:

            {
                "results": [{
                    "series": [{
                        "name": "temperatures",
                        "columns": ["time", "value", "location"],
                        "values": [
                            ["2016-01-01T00:01:00Z", 20.1, "groningen"],
                            ["2016-01-01T00:02:00Z", 23.0, "groningen"],
                        ]
                    }]
                }]
            }

        And it should become:

            [
                {
                    "name": "temperatures",
                    "values": [
                        {
                            "time": "2016-01-01T00:01:00Z",
                            "value": 20.1,
                            "location": "groningen"
                        },
                        {
                            "time": "2016-01-01T00:02:00Z",
                            "value": 23.0,
                            "location": "groningen"
                        }
                    ]
                }
            ]
        """
        rv = client.query('SELECT * FROM "temperatures"')
        assert rv[0]['name'] == 'temperatures'
        assert rv[0]['values'][0] == {
            "time": "2016-01-01T00:01:00Z",
            "value": 20.1,
            "location": "groningen"
        }

    @pytest.mark.parametrize('query', [
        'SELECT * FROM "temperatures"',
        'SHOW FIELD KEYS from "temperatures"'
    ])
    def test_should_call_get(self, client, query, get, post):
        """ Should use GET for these queries. """
        client.query(query)
        assert get.called

    @pytest.mark.parametrize('query', [
        'SELECT mean(value) as value INTO "temperature_averages" FROM "temperatures"',
        'ALTER RETENTION POLICY "rp_four_weeks" DEFAULT',
        'CREATE DATABASE "new_db"',
        'DELETE FROM "temperatures"',
        'DROP DATABASE "new_db"',
        'GRANT ALL TO "user"',
        'KILL QUERY 36',
        'REVOKE ALL PRIVILEGES FROM "user"'
    ])
    def test_should_call_post(self, client, query, post, get):
        """ Should use POST for these queries. """
        client.query(query)
        assert post.called

    def test_should_use_epoch_on_query(self, client, get):
        client.query('SELECT * FROM "temperature"', epoch='s')

        # If get is not called, get.call_args is None
        assert get.call_args is not None

        url = get.call_args[0][0]
        assert 'epoch=s' in url

    def test_should_throw_on_invalid_epoch(self, client, get):
        with pytest.raises(ValueError):
            client.query('SELECT * FROM "temperature"', epoch='not an epoch')

    def test_should_quote_query(self, client, get):
        client.query('SELECT * FROM "temperatures"')

        # If get is not called, get.call_args is None
        assert get.call_args is not None

        url = get.call_args[0][0]
        assert 'SELECT+%2A+FROM+%22temperatures%22' in url
