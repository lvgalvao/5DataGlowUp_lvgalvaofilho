import pandas as pd
import sweetviz as sv

# Carregando os dados
df = pd.read_csv("data/Listings.csv")

# Criando o relatório
report = sv.analyze(df)

# Salvando o relatório
report.show_html("sweetviz_report.html")
