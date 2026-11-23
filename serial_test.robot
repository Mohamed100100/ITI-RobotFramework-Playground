*** Settings ***
Library           SerialLibrary.py
Suite Setup       Open Connection
Suite Teardown    Close Connection

*** Test Cases ***
Hello Command Works
    Command Should Return    hello    Hello from device!
