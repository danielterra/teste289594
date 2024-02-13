import os
import sys
import base64
import starkbank

from dotenv import load_dotenv
load_dotenv()

# Name of the environment variable
env_var_name = "PRIVATE_KEY"

print(os.environ.get(env_var_name))
#check if .env has private key
if env_var_name in os.environ:
    print(f"{env_var_name} is already set on .env file")
    sys.exit()

#check if keys exists
try:
    with open("./starkbank_keys/private-key.pem", "r") as keys_file:
        private_key = keys_file.read().encode("utf-8")
        print("Private Key found")
except FileNotFoundError:
    print("Creating a new key pair...")
    private_key, public_key = starkbank.key.create("./starkbank_keys")

# Encode the string to Base64
encoded_bytes = base64.b64encode(private_key)
encoded_string = encoded_bytes.decode("utf-8")

# Path to the .env file
env_file_path = "./.env"

# Write the encoded string to the .env file
with open(env_file_path, "a") as env_file:
    env_file.write(f"\n{env_var_name}:{encoded_string}\n")
    print("Private key was set in the .env file as a base64 string")