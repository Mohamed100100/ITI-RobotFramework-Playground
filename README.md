# Robot Framework — Simple Guide

A minimal, general introduction to **Robot Framework**: what it is, how it
works, and how to run your first test. The serial/ESP32 example is only an
illustration — the same ideas apply to any system you can drive from Python.

## What is Robot Framework?

Robot Framework is a generic test automation framework. You write tests in a
simple, readable keyword syntax; the actual work is done by **libraries**
(written in Python, Java, ...). Robot Framework runs on your computer and
calls those libraries.

Key points:
- **Robot Framework runs the tests** (on your laptop/CI).
- **Libraries do the work** (open serial ports, click buttons, call APIs).
- **Rebot** is a separate tool that only regenerates/combines reports from
  saved results — it does not run tests.

## How it works

```
robot test.robot
        |
        v
  [Robot Framework]  --imports-->  [Python library]  --talks to-->  [system under test]
        |
        v
   report.html / log.html / output.xml
```

Flow for one test file:

1. Import libraries → discover their keywords.
2. Run `Suite Setup` (once for the whole suite).
3. Run each test case (keywords in order).
4. Run `Suite Teardown`.

If suite setup fails, the tests are skipped, but teardown still runs.

## Keyword matching

Robot Framework matches a keyword name to a Python method by ignoring
spaces, underscores, and case:

- `Open Connection`  ->  `open_connection`
- `Command Should Return`  ->  `command_should_return`

So a method `def command_should_return(self, ...)` becomes the keyword
`Command Should Return`.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install robotframework pyserial pyyaml
```

## A minimal example

Files: `SerialLibrary.py` (library) + `serial_test.robot` (test).

`serial_test.robot`:

```robot
*** Settings ***
Library           SerialLibrary.py
Suite Setup       Open Connection
Suite Teardown    Close Connection

*** Test Cases ***
Hello Command Works
    Command Should Return    hello    Hello from device!
```

Run:

```bash
robot serial_test.robot
```

Robot Framework will:
1. Import `SerialLibrary.py` and discover its keywords.
2. Run `Open Connection    /dev/ttyACM0`.
3. Run `Command Should Return    hello    Hello from device!`.
4. Run `Close Connection`.

## Line-by-line: what each test line does

```robot
*** Settings ***
Library           SerialLibrary.py
Suite Setup       Open Connection
Suite Teardown    Close Connection

*** Test Cases ***
Hello Command Works
    Command Should Return    hello    Hello from device!
```

| Test line | What Robot does | Python call |
|---|---|---|
| `Library SerialLibrary.py` | Imports the library; discovers its methods as keywords | `SerialLibrary()` constructor (reads `config.yaml`) |
| `Suite Setup Open Connection` | Runs once before all tests | `open_connection()` (no args → uses config port/baud) |
| `Suite Teardown Close Connection` | Runs once after all tests | `close_connection()` |
| `Hello Command Works` | Test case name | — |
| `Command Should Return    hello    Hello from device!` | Calls keyword with 2 args | `command_should_return("hello", "Hello from device!")` |

Inside `command_should_return`:
1. Clears input buffer.
2. Writes `"hello\r"` to the serial port.
3. Reads until `"Hello from device!"` appears or timeout.
4. Returns the text, or raises `AssertionError`.

So each test line maps directly to one Python method call.

## Results

After a run you get:

```
output.xml   # machine-readable results
log.html     # detailed log
report.html  # pass/fail summary
```

Open `report.html` in a browser.

## Re-run / combine reports with Rebot

Rebot does NOT run tests; it only processes saved results:

```bash
# regenerate reports
rebot --outputdir regenerated output.xml

# combine two runs
rebot --outputdir combined run1/output.xml run2/output.xml
```

## Write your own library

A library is just a Python class. Each method becomes a keyword:

```python
class MyLib:
    def do_something(self, arg):
        ...
        return result
```

```robot
*** Settings ***
Library    MyLib.py

*** Test Cases ***
My Test
    ${r}=    Do Something    value
    Should Be Equal    ${r}    expected
```

## Tips

- Use at least two spaces between columns in `.robot` files.
- `Suite Setup` runs once per suite; use `Test Setup` for per-test setup.
- If suite setup fails, tests are skipped but teardown still runs.
- Close other serial monitors before running serial tests.

## References

- Robot Framework user guide: https://robotframework.org/robotframework/
- pySerial: https://pyserial.readthedocs.io/
EOF
echo done