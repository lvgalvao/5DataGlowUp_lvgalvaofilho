import pandas as pd
from ydata_profiling import ProfileReport

# Carregando os dados
df = pd.read_csv('data/Listings.csv')

# Criando o relatório
profile = ProfileReport(df, title='Pandas Profiling Report', explorative=True)

# Salvando o relatório
profile.to_file("pandas_profiling_report.html")
