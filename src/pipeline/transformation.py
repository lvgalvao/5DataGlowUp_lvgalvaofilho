import os
import time
from datetime import datetime
from typing import List

import pandas as pd
from tqdm import tqdm


def ensure_dir(list_of_rectory: List[str]):
    """
    Cria os diretórios caso eles não existam.
    """
    for directory in list_of_rectory:
        if not os.path.exists(directory):
            os.makedirs(directory)


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


def add_quality_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona colunas de qualidade ao dataframe fornecido.
    """
    df["_source"] = "Google Drive"
    df["_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # formatando a data
    return df


def process_files(load_path: str, save_path: str) -> List[str]:
    """
    Processa os arquivos dentro do diretório fornecido e salva no diretório de destino.

    Retorna uma lista de mensagens indicando quais arquivos foram processados.
    """
    process_messages = []  # Lista para armazenar mensagens de processamento

    # Obtendo uma lista de arquivos .csv
    csv_files = [f for f in os.listdir(load_path) if f.endswith(".csv")]

    with tqdm(total=100, desc="Processando arquivos", unit="percent") as pbar:
        pbar.update(
            10
        )  # Isso aqui é só uma gambiarra mesmo, não tem nada a ver com o progresso real
        pbar.refresh()
        time.sleep(2)
        pbar.update(10)
        pbar.refresh()
        time.sleep(2)
        for index, filename in enumerate(csv_files):
            try:  # Tentando processar cada arquivo
                file_path = os.path.join(load_path, filename)
                df = pd.read_csv(
                    file_path,
                    encoding="utf-8",
                    encoding_errors="ignore",
                    low_memory=False,
                )

                # Se o arquivo for "Listings.csv", aplique a correção de codificação na coluna 'name'
                if "Listings.csv" in filename:
                    df["name"] = df["name"].apply(fix_encoding)

                # Adicionar colunas de qualidade, independentemente do arquivo
                df = add_quality_columns(df)

                # Salvar o DataFrame processado no novo diretório, mantendo o mesmo nome de arquivo
                save_file_path = os.path.join(save_path, filename)
                df.to_csv(save_file_path, encoding="utf-8", index=False)

                # Construindo a mensagem de sucesso
                message = f"Arquivo '{filename}' foi processado e salvo em '{save_file_path}'."
                process_messages.append(message)

                # Simula o processamento ao longo do tempo com um aumento de progresso
                if index == 0:  # ou qualquer outra condição que você escolher
                    pbar.update(30)  # isso atualiza a barra de progresso para 50%

                # algum outro marco pode ser colocado aqui para mais atualizações da barra de progresso, se necessário

            except Exception as e:
                # Em caso de erro durante o processamento, adicione a mensagem de erro à lista
                process_messages.append(
                    f"Erro ao processar o arquivo '{filename}': {e}"
                )

        pbar.update(50)  # atualizando o progresso restante para alcançar 100% no final

    return process_messages  # Retornando as mensagens de processamento


def transformation_full(load_path: str, save_path: str) -> List[str]:
    """
    Função completa para o processo de transformação dos arquivos CSV.

    Retorna uma lista de mensagens sobre os arquivos processados.
    """
    ensure_dir([load_path, save_path])  # Assegura que os diretórios existam
    return process_files(
        load_path, save_path
    )  # Processa os arquivos e retorna as mensagens


if __name__ == "__main__":
    directory_path = "data/bronze"  # substitua pelo seu diretório
    save_path = "data/silver"  # substitua pelo seu diretório
    transformation_full(directory_path, save_path)
