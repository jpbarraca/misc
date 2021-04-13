# Length Extention Attack

Implements a PoC of a Length Extention Attack to SHA256
The SHA256 implementation shows what data is actually processed by the digest

This works because:
for a digest `d` produced as `d  = H(SECRET || M1 || PADDING)`, `d` represents the state of the
digest after processing `SECRET || M1 || PADDING`.

Therefore, if we consider a new digest `dd = H(M2, state=d)`, where the previous digest is provided
as the initial state of the hash, this is equivalent to calculating
`H(SECRET || M1 || PADDING || M2)`

To run it: `python3 lea.py`

Output will be something like:
```
Original Computation: H(SECRET || M1)
  SHA256: Using original start state
  SHA256: Update:  f2e2c0401c7abbb14f726967696e616c206b6e6f776e2074657874
  SHA256: Update:  800000000000000000000000000000000000000000000000000000000000000000000000d8
Result:  256902775772f1bdc7a95cb224bb7567b867e44f4a462ebf0e501f95dc0096fb

Injecting extent: H(m2) with state=previous hash, counter=64 (1 block)
State:  [627638903, 1467150781, 3349765298, 616265063, 3093816399, 1246113471, 240131989, 3691026171]
M2:  b'Injected data'
  SHA256: Setting start state
  SHA256: Update:  496e6a65637465642064617461
  SHA256: Update:  800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000268
Result:  c74b0a0cbeba81ece703b68b5b3476f9ce25241c7767523ea68f42aa24f6f652

Remote computation: H(SECRET || m1 || padding || m2)
Padding Length:  37 Total:  64
Payload:  b'Original known text\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd8Injected data'
  SHA256: Using original start state
  SHA256: Update:  f2e2c0401c7abbb14f726967696e616c206b6e6f776e2074657874800000000000000000000000000000000000000000000000000000000000000000000000d8496e6a65637465642064617461
  SHA256: Update:  800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000268
Result:  c74b0a0cbeba81ece703b68b5b3476f9ce25241c7767523ea68f42aa24f6f652

Hashes match?  True
```
