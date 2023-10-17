# Projeto de Exploração de Dados e DataViz

## Sobre o Projeto

Este projeto foi desenvolvido com o objetivo de realizar uma Análise Exploratória de Dados (EDA) e criar visualizações de dados (DataViz) para o conjunto de dados fornecido. Utilizamos ferramentas como [Pandas Profiling](https://lvgalvao.github.io/5DataGlowUp_lvgalvaofilho/reports/pandas_profiling_report.html) e [Sweetviz](https://lvgalvao.github.io/5DataGlowUp_lvgalvaofilho/reports/sweetviz_report.html) para gerar relatórios de EDA automáticos, permitindo insights rápidos e diretos dos dados brutos, além de apresentar visualizações interativas.

Adicionalmente, criamos uma pipeline de processamento de dados robusta que ajuda na limpeza e preparação dos dados, corrigindo problemas de codificação e adicionando métricas de qualidade. Esta pipeline é parte do módulo UTILS, que fornece scripts e funções auxiliares para tratamento de dados.

O repositório serve como um meio de documentar e compartilhar o código, os resultados da análise e o conhecimento adquirido durante o desenvolvimento do projeto.

## Documentação do projeto

![Mkdocs](static/mkdocs.png)
![Mkdocs_02](static/mkdocs_2.png)
[Mkdocs](https://lvgalvao.github.io/5DataGlowUp_lvgalvaofilho/)

## EDA com Pandas Profile

![Pandas_01](static/pandas_profile_1.png)
![Pandas_02](static/pandas_profile.png)
[Pandas Profiling](https://lvgalvao.github.io/5DataGlowUp_lvgalvaofilho/reports/pandas_profiling_report.html)

## EDA com Sweetviz

![Sweet](static/sweet_profile.png)
[Sweetviz Profiling](https://lvgalvao.github.io/5DataGlowUp_lvgalvaofilho/reports/pandas_profiling_report.html)

## Pipeline de Processamento de Dados

Desenvolvemos uma pipeline automatizada para o processamento dos arquivos CSV encontrados no dataset. Essa pipeline realiza várias tarefas, incluindo a correção de problemas de codificação nos dados e a adição de novas colunas com métricas de qualidade para análise posterior.

Para executar a pipeline, você deve usar os seguintes comandos:

### 1. Clonar o Repositório

Clone o repositório para o seu ambiente local usando o Git.

```sh
git clone git@github.com:lvgalvao/5DataGlowUp_lvgalvaofilho.git
cd 5DataGlowUp_lvgalvaofilho
```

### 2. Instalar as Dependências

Utilize o Poetry para instalar as dependências do projeto.

```sh
poetry install
```

### 3. Rodando a pipeline

```sh
poetry run task process
```

🎉 **Pronto!** Agora você tem os dados tratados