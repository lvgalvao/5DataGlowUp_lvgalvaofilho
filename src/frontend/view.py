import pandas as pd
from autoviz import AutoViz_Class

# Corrigindo o nome do arquivo
filename = "data/Listings.csv"

# Instanciando o AutoViz Class
AV = AutoViz_Class()

# Lendo os dados
df = pd.read_csv(filename)

# Executando AutoViz
dft = AV.AutoViz(
    filename="",
    sep=",",
    depVar="",
    dfte=df,
    header=0,
    verbose=1,
    lowess=False,
    chart_format="server",
    max_rows_analyzed=150000,
    max_cols_analyzed=30,
)
