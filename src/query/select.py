import duckdb

# Caminho para o seu arquivo CSV
file_path = "data/Listings.csv"

# Criando uma conexão em memória com duckdb
con = duckdb.connect(database=":memory:", read_only=False)

# Executando uma consulta SQL diretamente no arquivo CSV
result = con.execute(f"SELECT * FROM read_csv_auto('{file_path}')")

# Buscando os resultados como um Pandas DataFrame (opcional)
df = result.fetchdf()

# Se desejar visualizar os resultados no console
print(df.head())
