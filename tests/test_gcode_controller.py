from unittest import mock
from jarvis_printer.printer.gcode_controller import PrinterController


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


def test_send_command():
    dummy = DummySerial()
    with mock.patch('serial.Serial', return_value=dummy):
        ctrl = PrinterController('/dev/null')
        ctrl.connect()
        resp = ctrl.send_command('M105')
        assert dummy.written[0] == b'M105\n'
        assert resp == 'ok'
        ctrl.disconnect()
