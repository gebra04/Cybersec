## Autor: Murilo Gebra
## Exploit Manual
Primeiramente devemos desativar o `ASLR`, pois sem ele a alocação de memória deixa de ser randômica. 
Desse modo, conseguimos identificar o endereço de memória utilizado no programa.

![image](https://github.com/HawkSecUnifei/resources-hawksec/assets/96196354/e4e82497-13af-47fd-b115-dae5dc82c5a1)

Depois disso utilizamos o comando `readelf` para encontrar o `offset` da função `system`, usamos o `-s` para procurar por símbolos (como funções).

![image](https://github.com/HawkSecUnifei/resources-hawksec/assets/96196354/e751d7b6-37f3-4f2f-83ba-d7b91cff17ae)

`0X4c830` é nosso endereço de memória. Agora precisamos obter o endereço do `shell`, usamos `strings` para conseguir isso:

![image](https://github.com/HawkSecUnifei/resources-hawksec/assets/96196354/674bb5c7-bce0-42fa-aeba-18b134a7f0be)

`-a` é usado para procurar pelo arquivo inteiro e `-t x` para mostrar o offset em hexadecimal.
`0X1b5fc8`.
	
Depois de coletar todas essas informações que precisamos basta criar um `script` em python para fazer o `estouro de buffer` de erros e ter acesso à função shell. Segue código comentado:

![image](https://github.com/HawkSecUnifei/resources-hawksec/assets/96196354/8db3a682-bc37-4c90-994a-1a0a6b8f3717)

## Exploit Automatizado
Essencialmente o problema é esse, agora podemos otimizar o nosso tempo automatizando nosso código:

![image](https://github.com/HawkSecUnifei/resources-hawksec/assets/96196354/2b075a65-16c2-43e3-ab14-1cd0375aedab)

Agora partindo para `64 bits`, a única diferença é que você precisará usar `pop rdi; ret` para fazer o exploit em `rdi`.
Use `ROPgadget --binary vuln-64 | grep rdi`  para obter o endereço.

![image](https://github.com/HawkSecUnifei/resources-hawksec/assets/96196354/c8d0c9e4-9317-462e-b5ef-b57de2722393)

No meu caso obtive `0x00000000004011cb` ou `0x4011cb`

![image](https://github.com/HawkSecUnifei/resources-hawksec/assets/96196354/509972f8-56b5-4a2f-8cff-8402fd621dd0)

e o código automatizado de 64 segue na mesma linha da automação de 32 bits:

![image](https://github.com/HawkSecUnifei/resources-hawksec/assets/96196354/7233802e-cdea-4aba-a703-c531aaa72e4b)
