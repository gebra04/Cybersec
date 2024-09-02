import hashlib
from pwn import *

p = process(['python3', 'keygenme-trial.py'])

# Variáveis e strings para hashing
username_trial = "PRITCHARD"
bUsername_trial = username_trial.encode()  # Codificar a string em bytes

key_part_static1_trial = "picoCTF{1n_7h3_|<3y_of_"
key_part_dynamic1_trial = "xxxxxxxx"
key_part_static2_trial = "}"
key_full_template_trial = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial

# Geração da chave com base no hash
key = "picoCTF{1n_7h3_|<3y_of_"
key += hashlib.sha256(bUsername_trial).hexdigest()[4]
key += hashlib.sha256(bUsername_trial).hexdigest()[5]
key += hashlib.sha256(bUsername_trial).hexdigest()[3]
key += hashlib.sha256(bUsername_trial).hexdigest()[6]
key += hashlib.sha256(bUsername_trial).hexdigest()[2]
key += hashlib.sha256(bUsername_trial).hexdigest()[7]
key += hashlib.sha256(bUsername_trial).hexdigest()[1]
key += hashlib.sha256(bUsername_trial).hexdigest()[8]
key += '}'

p.sendline(b'c')

p.recvuntil(b"key:")

p.sendline(key)

p.interactive()

print()
print(key)
