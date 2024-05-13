## Autor: Murilo Gebra

https://microcorruption.com/map

Para começar vamos dar uma estudada na `main`:
--------------------------------------------------
```asm
  4438 <main>
  4438:  3150 9cff      add	#0xff9c, sp.
  443c:  b012 7e44      call	#0x447e <create_password>
  4440:  3f40 e444      mov	#0x44e4 "Enter the password to continue", r15
  4444:  b012 9445      call	#0x4594 <puts>
  4448:  0f41           mov	sp, r15
  444a:  b012 b244      call	#0x44b2 <get_password>
  444e:  0f41           mov	sp, r15
  4450:  b012 bc44      call	#0x44bc <check_password>
  4454:  0f93           tst	r15
  4456:  0520           jnz	$+0xc <main+0x2a>
  4458:  3f40 0345      mov	#0x4503 "Invalid password; try again.", r15
  445c:  b012 9445      call	#0x4594 <puts>
  4460:  063c           jmp	$+0xe <main+0x36>
  4462:  3f40 2045      mov	#0x4520 "Access Granted!", r15
  4466:  b012 9445      call	#0x4594 <puts>
  446a:  b012 d644      call	#0x44d6 <unlock_door>
  446e:  0f43           clr	r15
  4470:  3150 6400      add	#0x64, sp
```

Nosso objetivo é chegar em `4462 mov	#0x4520 "Access Granted!", r15` para isso precisamos que a operação de `jnz 4456` seja realizada, assim `r15` deve ser diferente de 0. Já que a última função chamada antes da verificação de `r15` é `check_password` vamos verificar como e se ela modifica `r15`.

```asm
  44bc <check_password>
  44bc:  0e43           clr	r14
  44be:  0d4f           mov	r15, r13
  44c0:  0d5e           add	r14, r13
  44c2:  ee9d 0024      cmp.b	@r13, 0x2400(r14)
  44c6:  0520           jnz	$+0xc <check_password+0x16>
  44c8:  1e53           inc	r14
  44ca:  3e92           cmp	#0x8, r14
  44cc:  f823           jnz	$-0xe <check_password+0x2>
  44ce:  1f43           mov	#0x1, r15
  44d0:  3041           ret
  44d2:  0f43           clr	r15
  44d4:  3041           ret
```

Como podemos ver, a função pode zera `r15`, portanto devemos evitar isso. Avaliando os `jump's` podemos verificar que o primeiro deles se a comparação entre os bytes for falsa ele pula diretamente para `44d2` onde `r15` é zerado, já o segundo `jump` ele retorna para o inicio da função, criando assim um `loop while` para verificar os n bytes da senha solicitada enquanto os bytes corresponderem. Depois disso, se `r14 = 0x8`, ou seja, passar por 8 iterações, o sistema entende que a senha digitada está correta e não realiza o jump `44ca` para o inicio da função novamente, então `r15` recebe `0x1` e retorna para a main.

```
  4450:  b012 bc44      call	#0x44bc <check_password>
  4454:  0f93           tst	r15
  4456:  0520           jnz	$+0xc <main+0x2a>
```

Nesse trecho como `r15` é diferente de 0, o teste dará falso e o jump em `4456` será realizado, pulando diretamente para:
`4462` e em seguida desbloqueando a porta.

```
  0000: 0000 4400 0000 0000 0000 0000 0000 0000   ..D.............
  0010: 3041 0000 0000 0000 0000 0000 0000 0000   0A..............
  0020: 0000 0000 0000 0000 0000 0000 0000 0000   ................
  0030: *  
  0150: 0000 0000 0000 0000 0000 0000 085a 0000   .............Z..
  0160: 0000 0000 0000 0000 0000 0000 0000 0000   ................
  0170: *  
  2400: 3b2c 2a58 593a 7c00 0000 0000 0000 0000   ;,*XY:|.........
  2410: 0000 0000 0000 0000 0000 0000 0000 0000   ................
  2420: *  
  4380: 0000 0000 0000 0000 0000 0000 4445 4445   ............DEDE
  4390: 0300 4445 0000 de44 7f00 6e44 3b2c 2a58   ..DE...D.nD;,*X
  43a0: 593a 7c00 0000 0000 0000 0000 0000 0000   Y:|.............
  43b0: 0000 0000 0000 0000 0000 0000 0000 0000   ................
```
Agora vamos descobrir qual input precisamos colocar para passarmos pela porta.
A função `check_password` verifica os primeiros 8 bytes após 2400, ou seja, verifica de 2400 até 2407, sendo o último o critério de parada, então, na memória verificamos que o valor entre esses endereços é `3b2c 2a58 593a 7c00` copiamos o valor e inserimos como hexadecimal no input e passamos pela porta.
