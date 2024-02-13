import os
import sys
import base64
import binascii
import pathlib
import pytest
import invoice_spamer as invoice_spamer
import starkbank
from unittest.mock import patch, MagicMock
from starkcore import User
from dotenv import load_dotenv

# Load .env file
env_path = pathlib.Path('./../.env').resolve()
load_dotenv(dotenv_path=env_path)

def test_check_environment_with_keys(monkeypatch):
    monkeypatch.setenv('STARK_PROJECT_ID', 'test_project')
    monkeypatch.setenv('STARK_PRIVATE_KEY', base64.b64encode(b'secret_key').decode())
    invoice_spamer.check_environment()

def test_check_environment_no_project(monkeypatch):
    monkeypatch.delenv('STARK_PROJECT_ID', raising=False)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        invoice_spamer.check_environment()
    assert pytest_wrapped_e.value.code == 9

def test_check_environment_no_project(monkeypatch):
    monkeypatch.setenv('STARK_PROJECT_ID', 'test_project')
    monkeypatch.delenv('STARK_PRIVATE_KEY', raising=False)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        invoice_spamer.check_environment()
    assert pytest_wrapped_e.value.code == 1

def test_malformed_private_key(monkeypatch):
    monkeypatch.setenv('STARK_PROJECT_ID', 'test_project')
    monkeypatch.setenv('STARK_PRIVATE_KEY', 'not_base64')

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        invoice_spamer.check_environment()
    assert pytest_wrapped_e.value.code == 10

def test_connect_stark():
    assert isinstance(invoice_spamer.connect_stark(),User)

@patch('invoice_spamer.starkbank.invoice.create')
def test_generate_invoice(mock_invoice_create):
    mock_invoice = MagicMock()
    mock_invoice_create.return_value = [mock_invoice]

    iterations = 1
    invoice_spamer.generate_invoices(iterations)

    mock_invoice_create.assert_called_once()
    assert len(mock_invoice_create.call_args[0][0]) == iterations + 1
