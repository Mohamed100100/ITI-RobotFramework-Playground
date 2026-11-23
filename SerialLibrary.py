import time
import serial
import yaml


class SerialLibrary:
    ROBOT_LIBRARY_SCOPE = "SUITE"

    def __init__(self, config_path="config.yaml"):
        with open(config_path) as f:
            cfg = yaml.safe_load(f)["testbench"]
        self.port_name = cfg["port"]
        self.baudrate = int(cfg["baudrate"])
        self.timeout = float(cfg["timeout"])
        self.port = None

    def open_connection(self, device=None, baudrate=None):
        if device is None:
            device = self.port_name
        if baudrate is None:
            baudrate = self.baudrate
        self.port = serial.Serial(
            port=device,
            baudrate=int(baudrate),
            timeout=0.1,
        )
        time.sleep(1)

    def command_should_return(self, command, expected, timeout=None):
        if timeout is None:
            timeout = self.timeout
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
            "Expected " + repr(expected) + ", but received:\n"
            + received.decode("utf-8", errors="replace")
        )

    def close_connection(self):
        if self.port is not None:
            self.port.close()
            self.port = None
