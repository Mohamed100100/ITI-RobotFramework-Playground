# Robot Framework Testbench

Simple Robot Framework project that tests an ESP32-S3 Mini running the
Zephyr testbench firmware. It talks to the board over the serial port
(USB Serial/JTAG) using a small Python library.

## What is this?

- The board runs Zephyr firmware exposing a **shell** (commands: `ping`,
  `hello`, `gpio`, `adc`, `pwm`, `spi`).
- This repo contains **Robot Framework tests** that send those commands and
  check the answers.
- No hardware logic here — just tests + a serial helper library.

## Folder layout

```
.
├── config/testbench.yaml         # port, baudrate, timeout, prompt
├── libraries/TestbenchLibrary.py # serial helper (used by tests/)
├── resources/common.resource     # shared keywords
├── tests/                        # test suites
├── EspSerial.py                  # simple serial helper (tutorial example)
├── shell_test.robot              # smallest possible test
└── requirements.txt
```

## Requirements

- Python 3.10+
- A board flashed with the testbench firmware
- USB cable to the ESP32-S3 Mini (port `/dev/ttyACM0`)

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configure

Edit `config/testbench.yaml`:

```yaml
testbench:
  port: /dev/ttyACM0
  baudrate: 115200
  timeout: 2.0
  prompt: "tb:~$"
```

## Run

```bash
# all tests
robot tests/

# one group
robot tests/gpio/

# with a report folder
robot --outputdir results/ tests/

# open report (Linux)
xdg-open results/report.html
```

## Simple example (hello)

The smallest possible test is in `shell_test.robot` + `EspSerial.py`:

1. Flash the firmware (which provides the `hello` command).
2. Close any serial monitor.
3. Run:

```bash
robot shell_test.robot
```

Expected: `ESP32 Hello Command Works` passes and the report shows `Hello from ESP32-S3!`.

## Write your own test

1. Add a new `.robot` file under `tests/`.
2. Import the shared resource:

```robot
*** Settings ***
Resource    ../resources/common.resource
Suite Setup       Connect
Suite Teardown    Disconnect

*** Test Cases ***
My Test
    ${resp}=    Send Command    ping
    Should Contain    ${resp}    PONG
```

3. Use `Send Command`, `Expect Ok`, `Expect Val` keywords.
4. Run with `robot tests/`.

## Troubleshooting

| Problem | Fix |
|---|---|
| `Permission denied: /dev/ttyACM0` | `sudo usermod -a -G dialout $USER`, then re-login |
| No reply / timeout | Check cable, reflash firmware, wait 2s after connect |
| `ERR 1` | Unknown command — check spelling/case |
| `ERR 2` | Bad arguments |

## Related

- Firmware repo: https://github.com/Mohamed100100/ITI-Zephyr-Testbench-ESP32S3
EOF
echo done