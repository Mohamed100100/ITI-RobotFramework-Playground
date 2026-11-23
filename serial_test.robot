*** Settings ***
Library           SerialLibrary.py
Suite Setup       Open Connection    ${PORT}
Suite Teardown    Close Connection

*** Variables ***
${PORT}           /dev/ttyACM0

*** Test Cases ***
Hello Command Works
    Command Should Return    hello    Hello from device!
