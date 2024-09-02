## Autor: Murilo Gebra

# Keygen em python
## Primeiros passos:
Primeiro, podemos observar a primeira função chamada "menu_trial", essa função nos da um simples menu de interação 
para decidirmos dentre a, b, c, d. Sendo que na opção b é necessário ter a versão completa da aplicação.
```python
    print("___Arcane Calculator___\n\n\
Menu:\n\
(a) Estimate Astral Projection Mana Burn\n\
(b) [LOCKED] Estimate Astral Slingshot Approach Vector\n\
(c) Enter License Key\n\
(d) Exit Arcane Calculator")
```

## Fazendo a engenharia reversa
Agora, é hora de estudarmos o código que gera a nossa key para sair do modelo trial, essa parte do código é a função
"check_key".
```python
def check_key(key, username_trial):

    global key_full_template_trial

    if len(key) != len(key_full_template_trial):
        return False
    else:
        # Check static base key part --v
        i = 0
        for c in key_part_static1_trial:
            if key[i] != c:
                return False

            i += 1

        # TODO : test performance on toolbox container
        # Check dynamic part --v
        if key[i] != hashlib.sha256(username_trial).hexdigest()[4]:
            return False
        else:
            i += 1
        if key[i] != hashlib.sha256(username_trial).hexdigest()[5]:
            return False
        else:
            i += 1
        if key[i] != hashlib.sha256(username_trial).hexdigest()[3]:
            return False
        else:
            i += 1
        if key[i] != hashlib.sha256(username_trial).hexdigest()[6]:
            return False
        else:
            i += 1
        if key[i] != hashlib.sha256(username_trial).hexdigest()[2]:
            return False
        else:
            i += 1
        if key[i] != hashlib.sha256(username_trial).hexdigest()[7]:
            return False
        else:
            i += 1
        if key[i] != hashlib.sha256(username_trial).hexdigest()[1]:
            return False
        else:
            i += 1
        if key[i] != hashlib.sha256(username_trial).hexdigest()[8]:
            return False

        return True
```

Podemos verificar que a nossa key, na verdade, é composta pela key e pelo username_trial.

```python
key_part_static1_trial = "picoCTF{1n_7h3_|<3y_of_"
key_part_dynamic1_trial = "xxxxxxxx"
key_part_static2_trial = "}"
key_full_template_trial = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial
```

A primeira verificação de check_key é o tamanho da sua key inserida deve ser igual ao tamanho da `key_full_template_trial`,
depois é verificado se os `len(key_full_template_trial)` primeiros elesmentos são igual entre a key inserida e a esperada,
após o `for` há uma verificação em seguência de if/elses, como esse à seguir:
```python
        if key[i] != hashlib.sha256(username_trial).hexdigest()[4]:
            return False
        else:
            i += 1
```

## Gerando a key
`hashlib.sha256(username_trial)` cria um objeto hash com uma string codificada em bytes, `.hexdigest()[4]` transforma
o hash em hexadecimal (string) e pega o 5º elemento desse hash e compara com o key[i] elemento. Como a função retorna falso
caso a chave seja diferente da esperada, todos os caracteres devem ser iguais, portanto, para gerar a key, podemos fazer um
script em python que faz as operações contrárias ao código, desse modo obtemos a `key`.
```python
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
```
Sendo assim, nosso pequeno script para gerar a key seria assim. É possível melhorar esse código para solucionar o problema sozinho
utilizando a biblioteca `pwntools`, o código completo com a automação está disponível em `script.py`.
