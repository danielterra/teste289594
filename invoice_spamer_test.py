import os
import sys
import base64
import binascii
import pathlib
import pytest
import invoice_spamer as invoice_spamer
import starkbank
from dotenv import load_dotenv

# Load .env file
env_path = pathlib.Path('./../.env').resolve()
load_dotenv(dotenv_path=env_path)

def test_check_environment_with_keys(monkeypatch):
    monkeypatch.setenv('PROJECT_ID', 'test_project')
    monkeypatch.setenv('PRIVATE_KEY', base64.b64encode(b'secret_key').decode())
    invoice_spamer.check_environment()

def test_check_environment_no_project(monkeypatch):
    monkeypatch.delenv('PROJECT_ID', raising=False)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        invoice_spamer.check_environment()
    assert pytest_wrapped_e.value.code == 9

def test_check_environment_no_project(monkeypatch):
    monkeypatch.setenv('PROJECT_ID', 'test_project')
    monkeypatch.delenv('PRIVATE_KEY', raising=False)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        invoice_spamer.check_environment()
    assert pytest_wrapped_e.value.code == 1

def test_malformed_private_key(monkeypatch):
    monkeypatch.setenv('PROJECT_ID', 'test_project')
    monkeypatch.setenv('PRIVATE_KEY', 'not_base64')

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        invoice_spamer.check_environment()
    assert pytest_wrapped_e.value.code == 10

def test_connect_stark():
    assert invoice_spamer.connect_stark() == starkbank.User