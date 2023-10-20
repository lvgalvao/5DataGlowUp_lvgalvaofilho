import os
import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv
from io import BytesIO
import pandas as pd
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


# Função para listar os arquivos no bucket S3
st.cache_data(show_spinner=False)


def listar_arquivos_s3():
    return s3.list_objects_v2(Bucket=BUCKET_NAME)["Contents"]


# Função para baixar e carregar arquivo Parquet do S3
st.cache_data(hash_funcs={boto3.client: id}, show_spinner=False)


def carregar_parquet_s3(file_key):
    s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    data = s3_object["Body"].read()  # Isso é um conjunto de bytes, não uma string
    return pd.read_parquet(BytesIO(data))  # Polars lê diretamente do objeto de bytesz


def main():
    st.title("Análise de Listagens no S3")

    try:
        # Listando os arquivos no bucket S3
        objects = listar_arquivos_s3()

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

    # Filtrar arquivos Parquet
    parquet_files = [file for file in objects if file["Key"].endswith(".parquet")]

    if not parquet_files:
        st.write("Nenhum arquivo Parquet encontrado.")
        return

    # Supondo que estamos trabalhando apenas com o arquivo Parquet mais recente
    latest_parquet = sorted(
        parquet_files, key=lambda x: x["LastModified"], reverse=True
    )[0]
    file_key = latest_parquet["Key"]

    try:
        # Carregando e lendo o arquivo Parquet
        df = carregar_parquet_s3(file_key)

        # ---- Sidebar com Filtros ----

        st.sidebar.title("Filtros")

        # Filtro para a cidade
        unique_cities = sorted(df["city"].unique())
        selected_cities = st.sidebar.multiselect("Cidade", unique_cities, unique_cities)

        # Filtro para a faixa de preço
        min_price, max_price = df["price"].min(), df["price"].max()
        price_range = st.sidebar.slider(
            "Faixa de Preço",
            int(min_price),
            int(max_price),
            (int(min_price), int(max_price)),
        )

        # Aplicando os filtros ao dataframe
        filtered_df = df[
            (df["city"].isin(selected_cities))
            & (df["price"] >= price_range[0])
            & (df["price"] <= price_range[1])
        ]

        # ---- Análises e Visualizações ----

        # Média de preço
        avg_price = filtered_df["price"].mean()
        st.subheader(f"Preço médio: ${avg_price:.2f}")

        # Preço mínimo e máximo
        min_price = filtered_df["price"].min()
        max_price = filtered_df["price"].max()
        st.subheader(f"Preço mínimo: ${min_price:.2f}")
        st.subheader(f"Preço máximo: ${max_price:.2f}")

        # Quantidade de listagens
        num_listings = len(filtered_df)
        st.subheader(f"Número total de listagens: {num_listings}")

        # Preço mediano
        median_price = filtered_df["price"].median()
        st.subheader(f"Preço mediano: ${median_price:.2f}")

        # Preço mediano por tipo de propriedade
        median_price_property_type = (
            filtered_df.groupby("property_type")["price"]
            .median()
            .sort_values(ascending=False)
        )
        st.subheader("Preço mediano por tipo de propriedade")
        st.write(median_price_property_type)

        # Preço mediano por cidade
        median_price_city = (
            filtered_df.groupby("city")["price"].median().sort_values(ascending=False)
        )
        st.subheader("Preço mediano por cidade")
        st.write(median_price_city)

        # Mapa com as listagens
        st.subheader("Mapa de Listagens")
        st.map(filtered_df)

        # Histograma dos preços usando Plotly
        st.subheader("Distribuição dos Preços")
        fig = px.histogram(
            filtered_df,
            x="price",
            nbins=100,
            labels={"price": "Preço"},
            color_discrete_sequence=["#09f"],
        )
        fig.update_layout(
            xaxis_title_text="Preço",
            yaxis_title_text="Número de Listagens",
            title_text="Histograma de Preços",
            paper_bgcolor="#282c34",
            font=dict(color="white"),
            bargap=0.01,
        )
        st.plotly_chart(fig)

    except ClientError as e:
        st.error(f"Erro ao recuperar o arquivo {file_key}: {e}")
    except (
        Exception
    ) as e:  # Captura outros possíveis erros durante a leitura do Parquet
        st.error(f"Erro ao ler o arquivo Parquet: {e}")


if __name__ == "__main__":
    main()
