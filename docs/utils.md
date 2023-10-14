# Solução de Erro de Codificação no Dataset `Listings.csv`

## Problema: Erro de Codificação na Coluna "Name"

## Solução: Desenvolvimento do Módulo `my_encoding.py`

### ::: src.utils.my_encoding

### 🕵️‍♂️ Origem Suspeita do Erro:

Não tem como descobrir a origem do erro,
Mas minha suspeita é essa sequência de eventos que provavelmente levou ao erro de codificação:

1. **Criação da Mensagem Original:** Os dados foram originalmente criados em uma codificação Windows-1252.
    
    🔄 (Salvar)
    
2. **Arquivo Original:** Os dados foram armazenados no banco de dados em Windows-1252.
    
    🔄 (Conversão Incorreta para UTF-8)
    
3. **Arquivo Confuso:** Os dados foram convertidos (incorretamente) para UTF-8, criando problemas de codificação.
    
    🔄 (Compartilhamento/Transmissão)
    
4. **Recebimento do Arquivo:** Você recebeu o arquivo em UTF-8, mas ele ainda apresenta problemas de codificação.
    

### 🛠️ Solução Proposta:

A estratégia é "desconverter" e depois "reconverter" a coluna "Name" para garantir que ela esteja na codificação correta, UTF-8.

1. **Leitura do Arquivo:**
    
    * Utilize a codificação UTF-8 para ler o arquivo.
    
    
2. **Correção da Coluna "Name":**
    
    * Faça um decode usando o Windows-1252 apenas para a coluna "Name".
    
    
3. **Salvamento do Arquivo Corrigido:**
    
    * Salve o arquivo com a codificação UTF-8.
