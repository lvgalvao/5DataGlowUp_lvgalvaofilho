# extract.py

import os
import shutil
import zipfile
from datetime import datetime
from typing import List

import gdown
import pandas as pd


def ensure_dir(list_of_rectory: List[str]):
    """
    Cria os diretórios caso eles não existam.
    """
    for directory in list_of_rectory:
        if not os.path.exists(directory):
            os.makedirs(directory)


def download_file_from_google_drive_to_landing(file_id, landing_zone):
    """
    Faz o download dos nossos arquivos no Google Drive
    """
    gdown.download(id=file_id, output=landing_zone, quiet=False)
    return None


def find_zip_file(landing_directory):
    """
    Procura por um arquivo .zip no diretório fornecido.
    """
    for file_name in os.listdir(landing_directory):
        if file_name.endswith(".zip"):
            return os.path.join(landing_directory, file_name)
    raise ValueError("Nenhum arquivo .zip encontrado no diretório fornecido.")


def extract_zip_to_bronze(zip_filepath, bronze_zone):
    """
    Remove do zip e move para a camada bronze
    """
    with zipfile.ZipFile(zip_filepath, "r") as zip_ref:
        for member in zip_ref.namelist():
            filename = os.path.basename(member)
            # Pula diretórios
            if not filename:
                continue

            # Copia o arquivo
            source = zip_ref.open(member)
            target = open(os.path.join(bronze_zone, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)

        # Lista dos arquivos que você quer deletar após a extração
        files_to_delete = [
            "Listings_data_dictionary.csv",
            "Reviews_data_dictionary.csv",
        ]

        # Percorre todos os arquivos extraídos
        for file in zip_ref.namelist():
            # Se o arquivo extraído estiver na lista de arquivos para deletar
            if any(to_delete in file for to_delete in files_to_delete):
                # Constrói o caminho do arquivo
                file_path = os.path.join(bronze_zone, os.path.basename(file))

                # Deleta o arquivo
                try:
                    os.remove(file_path)
                    # print(f"{file} deletado com sucesso.")
                except Exception as e:
                    print(f"Não foi possível deletar {file}. Erro: {str(e)}")


def extract_full(file_id, landing_zone, bronze_zone):
    """
    Pipeline que chama todas os métodos de extração.
    """
    ensure_dir([landing_zone, bronze_zone])
    download_file_from_google_drive_to_landing(file_id, landing_zone)
    file_to_unzip = find_zip_file(landing_zone)
    extract_zip_to_bronze(file_to_unzip, bronze_zone)

    return None


if __name__ == "__main__":
    file_id = (
        "13ZMy2pNSStlQ6ESLtjD4Ye5I_QJ2DO8L"  # Substitua pelo seu Google Drive file ID
    )
    landing_zone = "data/landing/"
    bronze_zone = "data/bronze/"

    extract_full(file_id, landing_zone, bronze_zone)
