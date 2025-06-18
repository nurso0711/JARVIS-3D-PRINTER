import pytest
from jarvis_printer.web.app import create_app


class DummySerial:
    def __init__(self):
        self.written = []
        self._readline = b'ok\n'

    def write(self, data):
        self.written.append(data)

    def flush(self):
        pass

    def readline(self):
        return self._readline

    def close(self):
        pass


@pytest.fixture
def app(monkeypatch):
    dummy = DummySerial()
    monkeypatch.setattr('serial.Serial', lambda *a, **k: dummy)
    app = create_app()
    return app


def test_connect_and_command(app):
    client = app.test_client()
    res = client.post('/connect')
    assert res.get_json()['status'] == 'connected'
    res = client.post('/command', json={'command': 'M105'})
    assert res.get_json()['response'] == 'ok'
