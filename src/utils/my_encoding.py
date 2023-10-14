"""

Módulo para resolver o erro de encode da coluna Name do dataset Listings.csv

Suspeita do erro:

1. Criação da Mensagem Original em Windows-1252
   |
   | (Salvar)
   V
2. Arquivo Original no Banco em Windows-1252
   |
   | (Conversão Incorreta para UTF-8)
   V
3. Arquivo Confuso (UTF-8)
   |
   | (Compartilhamento/Transmissão)
   V
4. Você Recebe o Arquivo (UTF-8), mas apresenta problemas de codificação


Solução:

Vamos desconverter a coluna Name para Windows-1252 e depois converter para UTF-8 da forma correta

5. Leitura usando o encode UTF-8
   |
   |
   V
6. Faz um decode usando o Windows-1252 somente da coluna name
   |
   |
   V
7. Salva o arquivo com encode UTF-8

"""

import pandas as pd


def fix_encoding(problem_string):
    """
    Função para corrigir a codificação de uma string
    """
    if isinstance(
        problem_string, str
    ):  # Checar se é uma string, foi necessário por ter valores nulos
        return problem_string.encode("Windows-1252", errors="ignore").decode(
            "utf-8", errors="ignore"
        )
    else:
        return problem_string


if __name__ == "__main__":
    df = pd.read_csv("data/Listings.csv", encoding="utf-8", encoding_errors="ignore")
    df["name"] = df["name"].apply(fix_encoding)
    df.to_csv("data/Listings_new.csv", encoding="utf-8", index=False)
