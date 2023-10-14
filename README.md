# Projeto de Exploração de Dados e DataViz

## Sobre o Projeto

Este projeto visa realizar uma Análise Exploratória de Dados (EDA) e apresentar visualizações de dados (DataViz) para o dataset fornecido. Utilizamos o [Pandas Profiling](https://lvgalvao.github.io/5DataGlowUp_lvgalvaofilho/reports/pandas_profiling_report.html) e o [Sweetviz](https://lvgalvao.github.io/5DataGlowUp_lvgalvaofilho/reports/sweetviz_report.html) para gerar uma EDA automática, fornecendo insights valiosos diretamente dos dados brutos e apresentando visualizações interativas para explorar.

Além disso, o projeto inclui um módulo de utilitários (UTILS) que contém um script de correção, criado para tratar questões específicas encontradas durante a EDA, como problemas de codificação nos dados. 

Através deste repositório, buscamos não só armazenar o código e os resultados desta análise mas também oferecer uma documentação robusta e um guia para a execução dos scripts, facilitando a colaboração e o compartilhamento de conhecimento.

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
## Passos para Execução

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

### 3. Adicionar o Dataset

Salve o arquivo `Listings.csv` na pasta `Data`, que deve estar localizada na raiz do diretório do projeto. Caso a pasta não exista, crie-a.

```sh
mkdir Data  # Criar a pasta se ela não existir
```

**Nota:** Devido ao tamanho do arquivo, ele não está disponível diretamente no GitHub. Assegure-se de mover o arquivo `Listings.csv` para a pasta `Data`.

### 4. Realizando EDA

Após realizar a correção de codificação, a EDA pode ser visualizada acessando a documentação do MkDocs no diretório `docs` 

Para rodar são 2 arquivos na pasta `src/eda`

🎉 **Pronto!** Agora você tem um ambiente de desenvolvimento configurado e pronto para explorar os dados!

## Módulo UTILS

O módulo UTILS foi desenvolvido para auxiliar na correção e tratamento de dados, oferecendo scripts úteis que otimizam a preparação dos dados para análise.

## Contribuições

Contribuições são sempre bem-vindas! Sinta-se à vontade para abrir uma Issue ou criar um Pull Request.