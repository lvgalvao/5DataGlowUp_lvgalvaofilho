# Solução de Erro de Codificação no Dataset `Listings.csv`

## Problema: Erro de Codificação na Coluna "Name"

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

### 📜 Exemplo de Código:

```python
import pandas as pd

# Função para corrigir a codificação de uma string
def fix_encoding(problem_string):
    if isinstance(problem_string, str):
        return problem_string.encode('Windows-1252', errors='ignore').decode('utf-8', errors='ignore')
    else:
        return problem_string

# Lendo o arquivo com codificação UTF-8
df = pd.read_csv('data/Listings.csv', encoding='utf-8', encoding_errors='ignore')

# Aplicando a correção de codificação na coluna 'Name'
df['Name'] = df['Name'].apply(fix_encoding)

# Salvando o arquivo corrigido com codificação UTF-8
df.to_csv('data/Listings_new.csv', encoding='utf-8', index=False)
```

## Passos para Execução

### 1. Clonar o Repositório

Primeiramente, clone o repositório para o seu ambiente local usando o Git.

```sh
git clone git@github.com:lvgalvao/5DataGlowUp_lvgalvaofilho.git
cd 5DataGlowUp_lvgalvaofilho
```

### 2. Instalar as Dependências

Utilize o Poetry para instalar as dependências do projeto.

```sh
poetry install
```

### 3. Adicionar o Dataset

Salve o arquivo `Listings.csv` na pasta `Data`, que deve estar localizada na raiz do diretório do projeto. Se a pasta não existir, crie-a.

Como é um arquivo com mais de 100mb, não subi aqui no Github

```sh
mkdir Data  # Criar a pasta se ela não existir
```

Mova o arquivo `Listings.csv` para a pasta `Data`.

### 4. Executar o Script Principal

Finalmente, execute o script principal para aplicar a correção de codificação.

```sh
poetry run python3 src/my_encoding.py
```

🎉 **Pronto!** O script deve ser executado e o arquivo corrigido deve ser salvo de acordo com as instruções do código, gerando um Listings_new.csv correto.