#load from 
import base64
import binascii
import os
import sys
import starkbank
from dotenv import load_dotenv

load_dotenv()

def check_environment():
    print("trying to find the project_id and private_key on env...")

    if "STARK_PROJECT_ID" in os.environ:
        project_id = os.environ.get("STARK_PROJECT_ID")
    else:
        print("ERROR S8: PROJECT_ID not found in .env")
        sys.exit(9)

    if "STARK_PRIVATE_KEY" in os.environ:
        encoded_private_key = os.environ.get("STARK_PRIVATE_KEY")
        try:
            private_key = base64.b64decode(encoded_private_key).decode("utf-8")
        except binascii.Error as exception:
            print("ERROR S10: the private key is not in base64 format")
            sys.exit(10)
    else:
        print("ERROR S1: private key was not found on .env file")
        sys.exit(1)

def connect_stark():
    project_id = os.environ.get("STARK_PROJECT_ID")
    encoded_private_key = os.environ.get("STARK_PRIVATE_KEY")
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