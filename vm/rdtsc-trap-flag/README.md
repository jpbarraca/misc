## PoC for VM detection using RDTSC and the Trap Flag

As reported in https://unit42.paloaltonetworks.com/single-bit-trap-flag-intel-cpu/

Unit 42 has discovered a specific single bit (Trap Flag) in the Intel CPU register that can be abused by malware to evade sandbox detection in general purposes. Malware can detect whether it is executing in a physical or virtual machine (VM) by monitoring the response of the CPU after setting this single bit.

