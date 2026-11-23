*** Settings ***
Library           EspSerial.py
Suite Setup       Open Connection    ${PORT}
Suite Teardown    Close Connection

*** Variables ***
${PORT}           /dev/ttyACM0

*** Test Cases ***
ESP32 Hello Command Works
    Command Should Return    hello    Hello from ESP32-S3!
