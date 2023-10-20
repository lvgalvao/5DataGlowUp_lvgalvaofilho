import os
import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv
from io import BytesIO
import pandas as pd
import plotly.express as px
import base64
import plotly.figure_factory as ff
import json
import streamlit.components.v1 as components



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


def load_json_s3(s3, bucket_name, file_key):
    """
    Esta função baixa e lê um arquivo JSON do S3,
    retornando um DataFrame do Pandas.
    """
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    data = json.loads(obj["Body"].read())
    df = pd.json_normalize(data)  # Transforma o JSON em um dataframe
    return df


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


def main():
    # Para imagens na internet, você pode usar o link direto para a imagem.

    st.title(f"Análise Airbnb - Só os TOP :moneybag: :moneybag: :moneybag:")

    st.subheader("Não sei pq vocês tiraram o de 600k, aqui é tudo 10k +")

    st.subheader("Como o stakeholder vai pedir, toma aqui o EXCEL logo")

    st.subheader("  ")
    st.subheader("  ")

    try:
        # Obtendo lista de arquivos no bucket
        objects = s3.list_objects_v2(Bucket=BUCKET_NAME)["Contents"]

        # Filtrar arquivos JSON
        json_objects = [obj for obj in objects if obj["Key"].endswith(".json")]

        # DataFrame vazio para armazenar dados dos arquivos JSON
        json_df = pd.DataFrame()

        # Iterar sobre cada arquivo JSON, baixar, converter para DataFrame e concatenar
        for obj in json_objects:
            df = load_json_s3(s3, BUCKET_NAME, obj["Key"])
            json_df = pd.concat([json_df, df], ignore_index=True)

    except Exception as e:
        st.error(f"Erro ao carregar ou processar arquivos JSON do S3: {e}")
        return

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
        df_p = carregar_parquet_s3(file_key)

        # ---- Sidebar com Filtros ----

        df = pd.concat([df_p, json_df], ignore_index=True)

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

        # Criar colunas para as métricas
        col4, col5, col6 = st.columns(3)

        csv = convert_df(df)

        with col5:
            st.download_button(
                "Botão de Download do Excel",
                csv,
                "file.csv",
                "text/csv",
                key="download-csv",
            )

        st.subheader("  ")
        st.subheader("  ")
        # ---- Métricas ----

        # Calcular métricas
        avg_price = filtered_df["price"].mean()
        median_price = filtered_df["price"].median()
        max_price = filtered_df["price"].max()

        # Criar colunas para as métricas
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="Preço Médio", value=f"${avg_price:,.2f}")
        with col2:
            st.metric(label="Preço Mediano", value=f"${median_price:,.2f}")
        with col3:
            st.metric(label="Preço Máximo", value=f"${max_price:,.2f}")

        # ---- Análise de preço ----

        # Preço mediano por cidade como um gráfico de barras
        median_price_city = (
            filtered_df.groupby("city")["price"].median().sort_values(ascending=False)
        )

        # Criando um DataFrame a partir dos dados agregados para facilitar a plotagem
        median_price_df = pd.DataFrame(median_price_city).reset_index()

        # Criando o gráfico de barras com Plotly
        fig = px.bar(
            median_price_df,
            x="city",
            y="price",
            text="price",  # Isso adicionará o valor da barra em cima de cada barra
            labels={"price": "Preço Mediano", "city": "Cidade"},  # renomeia as labels
            color_discrete_sequence=["#636EFA"]
            * len(median_price_df),  # define uma única cor para todas as barras
            title="Um gráfico de barra para mostrar um preço médio por cidade",
        )
        fig.update_traces(
            texttemplate="%{text:.2s}", textposition="outside"
        )  # Formatar o texto
        fig.update_layout(
            yaxis=dict(title="Preço Mediano"),
            xaxis=dict(title="Cidade"),
            showlegend=False,  # Esconde a legenda
        )

        st.plotly_chart(fig)

        st.subheader("  ")
        st.subheader("  ")

        fig = px.histogram(
            filtered_df,
            x="price",
            nbins=50,
            title="Um histograma para mostrar frequência",
        )
        fig.update_xaxes(title="Preço")
        fig.update_yaxes(title="Quantidade de casas para alugar")
        fig.update_layout(
            showlegend=False
        )  # Você pode remover a legenda se não estiver usando cores diferentes para as barras

        st.plotly_chart(fig)

        # ---- Análise de Reviews ----

        # Histograma das Avaliações Gerais
        fig = px.histogram(
            filtered_df,
            x="review_scores_rating",
            nbins=20,
            title="Outro histograma para fingir que sei estatística",
        )
        st.plotly_chart(fig)

        st.subheader("  ")
        st.subheader("  ")

        # Aqui, estamos apenas selecionando algumas colunas para fins de demonstração. Você pode escolher diferentes colunas baseadas em seu dataset.
        heatmap_data = filtered_df[
            ["price", "review_scores_rating", "bedrooms", "accommodates"]
        ].dropna()

        # Calculando correlações
        correlations = heatmap_data.corr()

        # Criando o mapa de calor
        st.subheader("Esse aqui é impressiona até o Téo")
        fig = ff.create_annotated_heatmap(
            z=correlations.values,
            x=list(correlations.columns),
            y=list(correlations.index),
            annotation_text=correlations.round(2).values,
            showscale=True,
            colorscale="Viridis",
        )

        st.plotly_chart(fig)

        st.subheader("  ")
        st.subheader("  ")

        st.subheader("Um gráfico 3D muito bonito - que gira!")
        fig = px.scatter_3d(
            filtered_df,
            x="latitude",
            y="longitude",
            z="price",
            color="price",  # isso vai colorir os pontos com base no preço
            title="Preço das listagens em relação à localização",
            labels={
                "latitude": "Latitude",
                "longitude": "Longitude",
                "price": "Preço",
            },  # renomeia os labels dos eixos
            opacity=0.5,  # você pode ajustar a opacidade dos pontos
        )
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))

        st.plotly_chart(fig)

        st.subheader("  ")
        st.subheader("  ")
        st.subheader("  ")
        st.subheader("  ")

        # Mapa com as listagens
        st.subheader("Um gráfico de mapa, pq sempre fica bonito né?")
        st.map(filtered_df)

        st.subheader("  ")
        st.subheader("  ")

        # Adicionando um toque de humor e leveza ao texto
        st.markdown(
            """
            ### 😅 Ok... Dataviz não é minha praia...
            Mas cara, dê uma olhada na magia do streaming acontecendo! ✨
            """
        )

        st.markdown(
            """
            🔥 Sim, todos os dados que você vê aqui são servidos em *real-time*! 🔥
            """
        )

        st.markdown(
            """
            🚀 **Desafio Aceito?** Vamos testar?
            """
        )

        # Quantidade de listagens
        num_listings = len(filtered_df)
        st.markdown(
            f"""🎉 Aqui está o número total de reservas atuais: **{num_listings}**. """)
        
        st.markdown("Fique de olho nisso... algo especial está prestes a acontecer! 🌟")

        st.markdown(
            """
            🌈 Temos uma API que faz POST usando a FastAPI, tem um vídeo ensinando como usar
            """
        )

            # HTML para renderizar o vídeo
        video_embed_code = """
        <div style="position: relative; padding-bottom: 62.5%; height: 0;">
            <iframe src="https://www.loom.com/embed/d93390c5513547e59e3f8f00e33712a3?sid=89a6857f-eb7e-449a-a6fb-8cd532341e7f" 
                    frameborder="0" 
                    webkitallowfullscreen 
                    mozallowfullscreen 
                    allowfullscreen 
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
        </div>
        """

        # Renderizando o vídeo no Streamlit
        components.html(video_embed_code, height=450)  # Você pode ajustar a altura conforme necessário

        st.link_button(url="https://fivedataglowup.onrender.com/", label="Link para a API")

        st.markdown(
            """
            👀 E ai testou? Viu que o número realmente foi alterado?
            Abaixo, você pode olhar o conteúdo dos últimos 5 arquivos que foram lançados no nosso banco - e checar o seu!
            """
        )
        # Lista para armazenar os últimos 5 JSONs ordenados por última modificação
        latest_jsons = sorted(
            [
                obj for obj in objects if obj["Key"].endswith(".json")
            ],  # Filtrando para incluir apenas JSONs
            key=lambda x: x["LastModified"],
            reverse=True,
        )[:5]

        # Lista para armazenar os conteúdos dos últimos 5 JSONs
        latest_json_contents = []

        for file in latest_jsons:
            file_key = file[
                "Key"
            ]  # Aqui estava o erro. Você precisa do nome do arquivo, não de um booleano.

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
                st.error(
                    f"Não foi possível decodificar o arquivo {file_key} como JSON."
                )
                continue

        # Exibir os últimos 5 JSONs
        st.subheader("Últimos 5 JSONs (ordenados por última modificação no S3)")
        for i, (file_key, json_content) in enumerate(latest_json_contents, 1):
            with st.expander(
                f"JSON {i} - Última modificação: {latest_jsons[i-1]['LastModified']}"
            ):
                st.text(f"Nome do arquivo: {file_key}")
                st.json(
                    json_content
                )  # Esta função exibe dados no formato JSON de maneira formatada.
        
        st.markdown(
            """
            ## Legal né? Mas você reparou em uma coisa?...
            Apesar do FastAPI ter toda uma validação de schema e de datatype
            """)

        st.subheader("  ")

        st.markdown(
            """
            ## Não validamos REGRAS DE NEGÓCIO!
            """)

        st.subheader("  ")

        st.markdown(
            """
            Como assim? Olha lá em cima
            """)
        
        st.subheader("  ")

        st.markdown(
            """
            Tem uma cidade chamada STRING, valores MENORES que 10k e um ponto no MEIO DO MAR!
            """)
        
        st.subheader("  ")

        st.markdown(
            """
            Ou seja.... se isso aqui fosse uma aplicação teria muitos problema de integridade de dados.
            """)
        
        st.subheader("  ")

        st.markdown(
            """
            E é ai que entra uma série de estratégias de valição de dados!
            """)
        
        st.subheader("  ")

        st.markdown(
            """
            Se você quer aprender mais sobre e for de vitória, tenho um convite para você!
            """)
        
        st.subheader("  ")

        st.markdown(
            """
            ## No dia 28 de outubro, vou fazer um workshop de dataquality para Dashboards!
            """)
        
        st.subheader("  ")
        st.subheader("  ")

        st.image("https://i.postimg.cc/rwVtZm22/eu.jpg", use_column_width=True, width=50)

        st.subheader("  ")

        st.markdown(
            """
            Legal né? Vai lá no evento, ta cheio de cara fera e eu kkk
            """)
        
        st.subheader("  ")

        st.link_button(url="https://www.sympla.com.br/evento/data-saturday-1065-vitoria-2023/2172362?referrer=www.google.com", label="Link para o evento")
        
        st.markdown(
            """
            ## Se você não for de vitória, curte e comenta aqui no post para me ajudar a divulgar o evento! :D
            """)


    except ClientError as e:
        st.error(f"Erro ao recuperar o arquivo {file_key}: {e}")
    except (
        Exception
    ) as e:  # Captura outros possíveis erros durante a leitura do Parquet
        st.error(f"Erro ao ler o arquivo Parquet: {e}")

    
        # Mapa com as listagens
        st.subheader("Um meme")
        image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQOad1ujU6HSAeVv-_2LcO2wUklgmXen5LATg&usqp=CAU"
        st.image(image_url, use_column_width=True)


if __name__ == "__main__":
    main()
