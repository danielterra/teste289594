# Issues 8 to 12 Invoices every 3 hours to random people for 24 hours

import os
import sys
import starkbank
import base64
import binascii
import random
import names
from datetime import datetime
from dotenv import load_dotenv
from cpf_generator import CPF

#load from 
load_dotenv()

def check_environment():
    print("trying to find the project_id and private_key on env...")

    if "PROJECT_ID" in os.environ:
        project_id = os.environ.get("PROJECT_ID")
    else:
        print("ERROR S8: PROJECT_ID not found in .env")
        sys.exit(9)

    if "PRIVATE_KEY" in os.environ:
        encoded_private_key = os.environ.get("PRIVATE_KEY")
        try:
            private_key = base64.b64decode(encoded_private_key).decode("utf-8")
        except binascii.Error as exception:
            print("ERROR S10: the private key is not in base64 format")
            sys.exit(10)
    else:
        print("ERROR S1: private key was not found on .env file")
        sys.exit(1)

def connect_stark():
    project_id = os.environ.get("PROJECT_ID")
    encoded_private_key = os.environ.get("PRIVATE_KEY")
    private_key = base64.b64decode(encoded_private_key).decode("utf-8")
    print("trying to connect to starkbank with the found credentials...")
    try:
        user = starkbank.Project(
            environment="sandbox",
            id=project_id,
            private_key=private_key
        )
    except starkbank.error.InputErrors as exception:
        for error in exception.errors:
            print(f"ERROR S2 {error.code}: {error.message}")
            sys.exit(2)
    except starkbank.error.InternalServerError as exception:
        for error in exception.errors:
            print(f"ERROR S3 {error.code}: {error.message}")
            sys.exit(3)
    except starkbank.error.UnknownError as exception:
        for error in exception.errors:
            print(f"ERROR S4 {error.code}: {error.message}")
            sys.exit(4)
    
    return user

def generate_invoices(iterations:int):
    invoices=[]
    for i in range(iterations):
        invoices.append(
            starkbank.Invoice(
                amount=random.randint(1000, 100000),
                name=names.get_full_name(),
                tax_id=CPF.generate().format(),
            )
        )

    try:
        created_invoices = starkbank.invoice.create(invoices)
    except starkbank.error.InputErrors as exception:
        for error in exception.errors:
            print(f"ERROR S5 {error.code}: {error.message}")
            sys.exit(5)
    except starkbank.error.InternalServerError as exception:
        for error in exception.errors:
            print(f"ERROR S6 {error.code}: {error.message}")
            sys.exit(6)
    except starkbank.error.UnknownError as exception:
        for error in exception.errors:
            print(f"ERROR S7 {error.code}: {error.message}")
            sys.exit(7)

    for invoice in created_invoices:
        print("\n\n\nInvoice created")
        print(invoice)

if __name__ == "__main__":
    check_environment()
    # set the user for the next calls
    starkbank.user = connect_stark()
    generate_invoices(8)