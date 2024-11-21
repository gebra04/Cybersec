# Guia de Wireshark para CTFs

Este guia é uma cheat table para uso do Wireshark em competições de CTFs. Ele aborda tópicos comuns, comandos úteis, filtros essenciais e dicas para análise de tráfego de rede.

---

## Tópicos Comuns em CTFs com Wireshark

### 1. Recuperação de Credenciais
- **Protocolos comuns**: HTTP, FTP, TELNET.
- **Dicas**:
  - Para submissões de formulário em HTTP:  
    ```wireshark
    http.request.method == "POST"
    ```
  - No FTP, procure por comandos `USER` e `PASS` nos pacotes.

### 2. Análise de Streams de Dados
- **Seguir Fluxo TCP**:
  - Acesse: `Analyze > Follow > TCP Stream`.
  - Reconstrua conversas completas.
- **Exportar Objetos HTTP**:
  - Acesse: `File > Export Objects > HTTP`.
  - Baixe arquivos transferidos.

### 3. Extração de Arquivos ou Dados Binários
- Localize transferências em protocolos como FTP, HTTP ou SMB.
- Use:  
File > Export Objects
para salvar os arquivos capturados.

### 4. Análise de Malwares
- Identifique conexões com domínios maliciosos (DGA).
- Use:  
Statistics > Protocol Hierarchy
para encontrar tráfego incomum.

### 5. Criptografia e TLS
- Identifique pacotes TLS com:
```wireshark
ssl.handshake
```
Analise tráfego em portas HTTPS (443).
Dicas para Configuração Inicial
1. Filtros Essenciais

    Por Protocolo:

http || dns || ftp

Por Endereço IP:

ip.src == X.X.X.X || ip.dst == X.X.X.X

Por Palavra-Chave:

    frame contains "senha"

2. Colorização de Pacotes

    Configure regras de cor para facilitar a identificação de pacotes importantes:
        Acesse:

        View > Coloring Rules

      Adicione cores para diferentes protocolos ou palavras-chave.

3. Reduzindo o Ruído

    Para excluir pacotes irrelevantes e focar no tráfego necessário:

    !arp && !icmp

Comandos Essenciais no Wireshark
1. Exportação de Dados

    Para exportar pacotes capturados:
        Vá até:

        File > Export Packet Dissections

      Escolha formatos como .txt ou .csv.

2. Busca de Pacotes

    Use o atalho:

    Ctrl + F

    No menu, selecione critérios de busca como:
        String: Para localizar palavras específicas.
        Hex Value: Para encontrar valores hexadecimais no tráfego.

3. Análise Estatística

    Resumo do Tráfego:
        Acesse:

    Statistics > Summary

Gráficos de I/O:

  Acesse:

        Statistics > IO Graphs

  Use gráficos para detectar anomalias ou picos de tráfego.

Atalhos Importantes

Pausar Captura:

Ctrl + E

Salvar Captura:

Ctrl + S

Seguir Fluxo TCP:

Ctrl + Alt + T

Resetar Filtros:

Ctrl + R

Lembretes para CTFs
1. Tempo é Essencial

    Use filtros de forma eficiente para reduzir o escopo da análise e economizar tempo.

2. Destaque para DNS

    Muitas pistas podem estar escondidas em consultas DNS. Utilize:

    dns && ip.src == <IP>

3. Erros Comuns

    Certifique-se de estar usando o formato correto de arquivo de captura:

    .pcap ou .pcapng

    Verifique se os filtros estão bem configurados.

4. Importância de Salvar

    Salve regularmente suas capturas:

    File > Save As

Conclusão

Com este guia, sua equipe terá as ferramentas necessárias para abordar desafios de Wireshark em CTFs. Pratique frequentemente e adapte as técnicas conforme necessário!

Você disse:
como faço enumeração no texto em arquivos .md
O ChatGPT disse:
ChatGPT

No formato .md (Markdown), você pode fazer enumerações de duas formas principais: ordenadas e não ordenadas.
1. Enumeração Ordenada

Use números seguidos por um ponto (.):

1. Item 1
2. Item 2
3. Item 3

Resultado renderizado:

    Item 1
    Item 2
    Item 3

2. Enumeração Não Ordenada

Use traços (-), asteriscos (*) ou sinais de mais (+):

- Item 1
- Item 2
- Item 3

Resultado renderizado:

    Item 1
    Item 2
    Item 3

Ou com asteriscos:

* Item 1
* Item 2
* Item 3

Resultado renderizado:

    Item 1
    Item 2
    Item 3

Subitens

Você pode criar subitens adicionando dois ou mais espaços antes do marcador:

1. Item 1
   - Subitem 1.1
   - Subitem 1.2
2. Item 2
   * Subitem 2.1
   * Subitem 2.2

Resultado renderizado:

    Item 1
        Subitem 1.1
        Subitem 1.2
    Item 2
        Subitem 2.1
        Subitem 2.2

Dica Extra

Os números em uma enumeração ordenada não precisam ser consecutivos, mas o renderizador gerará automaticamente a sequência:

1. Primeiro
1. Segundo
1. Terceiro

Renderizado como:

    Primeiro
    Segundo
    Terceiro
