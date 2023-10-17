# pipeline/main.py
import os
import sys

# Importe a função do seu script de extração
from extract import \
    extract_full  # Certifique-se de que o caminho do import está correto
from loguru import logger
from transformation import transformation_full


def main():
    """
    Função principal que coordena a execução das etapas de extração e transformação.
    """

    # Configuração do Loguru
    log_file_path = "logs/pipeline.log"  # Ajuste este caminho conforme necessário

    logger.remove()  # Remova os manipuladores padrão

    # Adicione seus próprios manipuladores com um novo formato de data/hora
    logger_format = "<green>{time:YYYY-MM-DDTHH:mm:ss}</green> <level>{message}</level>"  # Ajuste o formato aqui

    logger.add(sys.stderr, colorize=True, format=logger_format)
    logger.add(
        log_file_path,
        rotation="1 week",
        retention="1 month",
        level="INFO",
        format=logger_format,
    )

    # Parâmetros
    file_id = (
        "13ZMy2pNSStlQ6ESLtjD4Ye5I_QJ2DO8L"  # Substitua pelo seu Google Drive file ID
    )
    landing_zone = "data/landing/"
    bronze_zone = "data/bronze/"
    silver_zone = "data/silver/"

    # Verifique se os diretórios necessários existem ou crie-os
    for directory in [landing_zone, bronze_zone, silver_zone]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    logger.info("Iniciando a extração de dados...")

    try:
        # Executar a etapa de extração
        extract_full(file_id, landing_zone, bronze_zone)
        logger.info("Extração de dados concluída com sucesso.")
    except Exception as e:
        logger.error(f"Erro ocorrido durante a extração de dados: {e}")

    logger.info("Iniciando a transformação de dados...")

    try:
        # Executar a etapa de transformação e receber as mensagens de status
        transformation_messages = transformation_full(bronze_zone, silver_zone)

        # Registrar cada mensagem no log
        for message in transformation_messages:
            logger.info(message)

        logger.info("Transformação de dados concluída com sucesso.")
    except Exception as e:
        logger.error(f"Erro ocorrido durante a transformação de dados: {e}")

    logger.info("Pipeline concluído.")


if __name__ == "__main__":
    main()
