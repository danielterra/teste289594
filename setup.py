import starkbank
private_key, public_key = starkbank.key.create("./starkbank_keys")

print(private_key)
print(public_key)