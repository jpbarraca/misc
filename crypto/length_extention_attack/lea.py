# Author: João Paulo Barraca
# PoC of the Length Extension Attack applied to SHA256

### The attack
# Set the internal SHA2 state machine to the output of the previous hash
# Update the state with M2. 
# Basically: 
# with:
#    d  = H(SECRET || M1 || PADDING) 
#    dd = H(M2, state=d)
#    and H(SECRET || M1 || PADDING || M2) == dd
# it results in H((SECRET || M1 || PADDING_M1) || M2 || PADDING_M2)

from sha256 import sha256
import os
import binascii
import struct

SECRET = os.urandom(8)
secret_len = len(SECRET)

m1 = b'Original known text'
m2 = b'Injected data'

print(f"Original Computation: H(SECRET || M1)")
s = sha256(m=SECRET + m1)
h1 = binascii.hexlify(s.hexdigest())
print("Result: ", h1.decode('latin'))

#
print("\nInjecting extent: H(m2) with state=previous hash, counter=64 (1 block)")

# Convert the previous hash to a list of longs
state = []
for x in range(0, len(h1), 8):
    state.append(int(h1[x:x+8], 16))

print("State: ", state)
print("M2: ", m2)
s = sha256(m=m2, s=state, l=64*(1+(len(m1)+secret_len)//64)) 
h2 = binascii.hexlify(s.hexdigest())
print("Result: ", h2.decode('latin'))


print("\nRemote computation: H(SECRET || m1 || padding || m2)")
# (key + message + padding) % 512 == 0
# len(SECRET) + len(m1) + padding
# Padding is a 1 followed by a number of zeros: 0x8000000000...00 until block is 512 bits an then the size in bits encoded as 8 bytes

padding = b'\x80' + b'\0' * (64 - (len(SECRET) + len(m1) + 1 + 8) % 64) + struct.pack('!Q',(len(m1) + secret_len)*8)
print("Padding Length: ", len(padding), "Total: ", secret_len + len(m1) + len(padding))

# Set the initial state to the value of the previous digest
payload = m1 + padding + m2
print("Payload: ", payload)
s = sha256(SECRET + payload)
h3 = binascii.hexlify(s.hexdigest())
print("Result: ", h3.decode('latin'))

print("\nHashes match? ", h2 == h3)
