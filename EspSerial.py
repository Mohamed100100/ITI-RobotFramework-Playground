import time
import serial


class EspSerial:
    ROBOT_LIBRARY_SCOPE = "SUITE"

    def __init__(self):
        self.port = None

    def open_connection(self, device, baudrate=115200):
        self.port = serial.Serial(
            port=device,
            baudrate=int(baudrate),
            timeout=0.1,
        )
        time.sleep(1)

    def command_should_return(self, command, expected, timeout=5):
        self.port.reset_input_buffer()
        self.port.write((command + "\r").encode("utf-8"))
        self.port.flush()

        received = bytearray()
        deadline = time.monotonic() + float(timeout)

        while time.monotonic() < deadline:
            received.extend(self.port.read(256))
            text = received.decode("utf-8", errors="replace")

            if expected in text:
                return text

        raise AssertionError(
            f"Expected {expected!r}, but received:\n"
            f"{received.decode('utf-8', errors='replace')}"
        )

    def close_connection(self):
        if self.port is not None:
            self.port.close()
            self.port = None
