from Crypto.Util.number import long_to_bytes

# Given integer
num = 11515195063862318899931685488813747395775516287289682636499965282714637259206269

# Convert the integer to bytes
message_bytes = long_to_bytes(num)

# Decode bytes to string
message = message_bytes.decode('utf-8')
print(message)