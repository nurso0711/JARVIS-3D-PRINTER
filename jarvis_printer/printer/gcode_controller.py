import serial

class PrinterController:
    """Simple controller for communicating with a 3D printer using G-code."""

    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = None

    def connect(self) -> None:
        """Open a serial connection to the printer."""
        if not self.ser:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)

    def disconnect(self) -> None:
        """Close the connection to the printer."""
        if self.ser:
            self.ser.close()
            self.ser = None

    def send_command(self, command: str) -> str:
        """Send a single G-code command and return the printer's response."""
        if not self.ser:
            raise RuntimeError("Printer not connected")
        self.ser.write((command + "\n").encode())
        self.ser.flush()
        return self.ser.readline().decode().strip()
