## Autor: Murilo Gebra
https://microcorruption.com/map

Para começar vamos dar uma estudada na `main`:
  -----------------------------------------------------------------------------
```asm
  4438 <main>
  4438:  3150 9cff      add	#0xff9c, sp
  443c:  3f40 a844      mov	#0x44a8 "Enter the password to continue", r15
  4440:  b012 5845      call	#0x4558 <puts>
  4444:  0f41           mov	sp, r15
  4446:  b012 7a44      call	#0x447a <get_password>
  444a:  0f41           mov	sp, r15
  444c:  b012 8444      call	#0x4484 <check_password>
  4450:  0f93           tst	r15
  4452:  0520           jnz	$+0xc <main+0x26>
  4454:  3f40 c744      mov	#0x44c7 "Invalid password; try again.", r15
  4458:  b012 5845      call	#0x4558 <puts>
  445c:  063c           jmp	$+0xe <main+0x32>
  445e:  3f40 e444      mov	#0x44e4 "Access Granted!", r15
  4462:  b012 5845      call	#0x4558 <puts>
  4466:  b012 9c44      call	#0x449c <unlock_door>
  446a:  0f43           clr	r15
  446c:  3150 6400      add	#0x64, sp
```
  ------------------------------------------------------------------------------
Depois disso, podemos notar a presença de dois `jump's` precisamos descobrir para onde eles vão e se precisamos que
sejam realizados ou não. Vamos começar testando `445c: jmp` pegando o endereço da main (0x4438) somado à 0x32 obtemos `446a`
onde `r15` é zerado e o código acaba, logo não queremos que isso aconteça, para evitar isso é necessário que `4452: jnz` execute,
calculando onde jnz para obtemos: 0x4448 + 0x26 = `445e`, exatamente onde queríamos, após `jmp`.

Agora vamos dar uma olhada na função `check_password`:
--------------------------------------------------------------------------
```asm
  4484 <check_password>
  4484:  6e4f           mov.b	@r15, r14
  4486:  1f53           inc	r15
  4488:  1c53           inc	r12
  448a:  0e93           tst	r14
  448c:  fb23           jnz	$-0x8 <check_password+0x0>
  448e:  3c90 0900      cmp	#0x9, r12
  4492:  0224           jz	$+0x6 <check_password+0x14>
  4494:  0f43           clr	r15
  4496:  3041           ret
  4498:  1f43           mov	#0x1, r15
  449a:  3041           ret
```
--------------------------------------------------------------------------
Essa função passa o primeiro byte do que aponta `r15` para `r14`, incrementa `r15`, e usa `r12` como indice, fazendo um `while`
loop enquanto `r14` for diferente de 0. Se ele continuar a verificação ao ponto de incrementar `r12` 9 vezes nossa comparação
`448e` será verdadeira e o pulo para `0x4484 + 0x14 = 0x4498` será realizado, assim `r15` receberá 1 como valor.

Voltando para a função main:
--------------------------------------------------------------------------
```
  444c:  b012 8444      call	#0x4484 <check_password>
  4450:  0f93           tst	r15
  4452:  0520           jnz	$+0xc <main+0x26>
```
--------------------------------------------------------------------------
Com `r15` sendo `1` a comparação `tst t15` será diferente de zero, assim realizando o pulo e concluindo o desafio.
O que podemos concluir é que como o código só verifica o número de entradas podemos digitar quaisquer 8 digitos,
deve-se deixar o último byte como sinal de parada do input. Então digitando 12345678 passamos do `Tutorial`
