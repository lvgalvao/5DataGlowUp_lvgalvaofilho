import os
import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import json
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import plotly.express as px

# Carregar variáveis de ambiente
load_dotenv()

# Configurar cliente do boto3
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")


def main():
    st.title("Análise de Listagens no S3")

    try:
        # Listando os arquivos no bucket S3
        objects = s3.list_objects_v2(Bucket=BUCKET_NAME)["Contents"]

        # Se não há objetos, uma exceção KeyError seria lançada
        if not objects:
            st.write("Nenhum objeto no bucket.")
            return

    except NoCredentialsError:
        st.error("Credenciais da AWS não encontradas.")
        return
    except ClientError as e:
        st.error(f"Erro ao acessar o bucket S3: {e}")
        return

    # Lista para armazenar os últimos 5 JSONs ordenados por última modificação
    latest_jsons = sorted(objects, key=lambda x: x["LastModified"], reverse=True)[:5]

    # Lista para armazenar os conteúdos dos últimos 5 JSONs
    latest_json_contents = []

    for file in latest_jsons:
        file_key = file["Key"]

        try:
            # Baixando o arquivo do S3
            s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
            data = s3_object["Body"].read()
            json_content = json.loads(data)

            # Adicionar o JSON à lista de conteúdos
            latest_json_contents.append((file_key, json_content))

        except ClientError as e:
            st.error(f"Erro ao recuperar o arquivo {file_key}: {e}")
            continue
        except json.JSONDecodeError:
            st.error(f"Não foi possível decodificar o arquivo {file_key} como JSON.")
            continue

    # Exibir os últimos 5 JSONs
    st.subheader("Últimos 5 JSONs (ordenados por última modificação no S3)")
    for i, (file_key, json_content) in enumerate(latest_json_contents, 1):
        with st.expander(
            f"JSON {i} - Última modificação: {latest_jsons[i-1]['LastModified']}"
        ):
            st.text(f"Nome do arquivo: {file_key}")
            st.json(json_content)

    # Lista para armazenar os conteúdos de todos os JSONs
    all_json_contents = []

    for file in objects:
        file_key = file["Key"]

        try:
            # Baixando o arquivo do S3
            s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
            data = s3_object["Body"].read()
            json_content = json.loads(data)

            # Adicionar o JSON à lista de conteúdos
            all_json_contents.append(json_content)

        except ClientError as e:
            st.error(f"Erro ao recuperar o arquivo {file_key}: {e}")
            continue
        except json.JSONDecodeError:
            st.error(f"Não foi possível decodificar o arquivo {file_key} como JSON.")
            continue

    # Convertendo para DataFrame do pandas para facilitar a análise
    df = pd.DataFrame(all_json_contents)

    # Média de preço
    avg_price = df["price"].mean()
    st.subheader(f"Preço médio: ${avg_price:.2f}")

    # Preço mínimo e máximo
    min_price = df["price"].min()
    max_price = df["price"].max()
    st.subheader(f"Preço mínimo: ${min_price:.2f}")
    st.subheader(f"Preço máximo: ${max_price:.2f}")

    # Quantidade de listagens
    num_listings = len(df)
    st.subheader(f"Número total de listagens: {num_listings}")

    # Mapa com as listagens
    st.subheader("Mapa de Listagens")
    st.map(df)

    # Histograma dos preços usando Plotly
    st.subheader("Distribuição dos Preços")
    fig = px.histogram(
        df,
        x="price",
        nbins=100,
        labels={"price": "Preço"},
        color_discrete_sequence=["#09f"],
    )
    fig.update_layout(
        xaxis_title_text="Preço",
        yaxis_title_text="Número de Listagens",
        title_text="Histograma de Preços",
        paper_bgcolor="#282c34",  # Define o fundo preto
        font=dict(color="white"),  # Define a cor do texto como branco
        bargap=0.01,  # Espaçamento entre barras
    )
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
