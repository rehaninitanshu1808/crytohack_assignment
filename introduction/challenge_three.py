import base64

hex_str = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"

# Step 1: Convert hex to bytes
byte_data = bytes.fromhex(hex_str)

# Step 2: Encode bytes to Base64
base64_encoded = base64.b64encode(byte_data).decode('utf-8')

print(base64_encoded)