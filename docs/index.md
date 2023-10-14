# Bem-Vindo ao Projeto de Dataviz

Este projeto foi desenvolvido com o intuito de contribuir para a comunidade de dados, oferecendo recursos e insights úteis através da exploração de dados e visualização de dados (DataViz). A ideia central é empregar técnicas e ferramentas de engenharia de dados e análise exploratória de dados (EDA) para revelar padrões, anomalias e estruturas nas informações coletadas, possibilitando uma compreensão mais aprofundada e orientada por dados.

## Objetivo do Projeto

A exploração de dados e a visualização de dados são etapas cruciais em qualquer projeto de ciência de dados ou análise de dados, proporcionando uma compreensão profunda e insights valiosos dos dados em mãos. Este projeto visa:

- Explorar conjuntos de dados de maneira abrangente.
- Identificar padrões e irregularidades nos dados.
- Gerar visualizações de dados informativas e intuitivas.
- Contribuir com a comunidade, oferecendo recursos e insights valiosos.

## Dataset Listings

Abaixo está a descrição detalhada para cada campo no arquivo CSV que contém informações sobre listagens.

| Campo                       | Tipo de Dado | Descrição                                   |
| --------------------------- | ------------ | ------------------------------------------- |
| listing_id                  | Integer      | ID único da listagem                        |
| name                        | String       | Nome/Descrição da listagem                  |
| host_id                     | Integer      | ID único do anfitrião                       |
| host_since                  | Date         | Data desde quando o usuário é um anfitrião  |
| host_location               | String       | Localização do anfitrião                    |
| host_response_time          | String       | Tempo de resposta do anfitrião              |
| host_response_rate          | Float        | Taxa de resposta do anfitrião               |
| host_acceptance_rate        | Float        | Taxa de aceitação do anfitrião              |
| host_is_superhost           | Boolean      | Se o anfitrião é um "superhost"             |
| host_total_listings_count   | Float        | Total de listagens do anfitrião             |
| host_has_profile_pic        | Boolean      | Se o anfitrião tem foto de perfil           |
| host_identity_verified      | Boolean      | Se a identidade do anfitrião foi verificada |
| neighbourhood               | String       | Bairro da listagem                          |
| district                    | String       | Distrito da listagem                        |
| city                        | String       | Cidade da listagem                          |
| latitude                    | Float        | Latitude da listagem                        |
| longitude                   | Float        | Longitude da listagem                       |
| property_type               | String       | Tipo de propriedade                         |
| room_type                   | String       | Tipo de quarto                              |
| accommodates                | Integer      | Número de acomodações                       |
| bedrooms                    | Float        | Número de quartos                           |
| amenities                   | List         | Lista de comodidades                        |
| price                       | Integer      | Preço da listagem                           |
| minimum_nights              | Integer      | Noites mínimas para reserva                 |
| maximum_nights              | Integer      | Noites máximas para reserva                 |
| review_scores_rating        | Float        | Pontuação geral de avaliações               |
| review_scores_accuracy      | Float        | Pontuação de precisão nas avaliações        |
| review_scores_cleanliness   | Float        | Pontuação de limpeza nas avaliações         |
| review_scores_checkin       | Float        | Pontuação de check-in nas avaliações        |
| review_scores_communication | Float        | Pontuação de comunicação nas avaliações     |
| review_scores_location      | Float        | Pontuação de localização nas avaliações     |
| review_scores_value         | Float        | Pontuação de valor nas avaliações           |
| instant_bookable            | Boolean      | Se a listagem é instantaneamente reservável |

**Nota:** A descrição foi feita de maneira simplificada e pode requerer ajustes conforme a necessidade do projeto e os detalhes específicos do seu dataset.


## Uso do Pandas Profiling para EDA Automática

A biblioteca [Pandas Profiling](https://github.com/pandas-profiling/pandas-profiling) é uma ferramenta essencial utilizada neste projeto para realizar uma Análise Exploratória de Dados (EDA) de forma rápida e automática. A ferramenta gera relatórios de dados abrangentes, que oferecem uma visão instantânea e profunda sobre a distribuição, frequência e tipos de dados presentes no conjunto de dados analisado.

Com o Pandas Profiling, fomos capazes de:

- Rapidamente gerar um EDA inicial e identificar aspectos críticos dos dados.
- Visualizar distribuições e correlações de variáveis de uma maneira intuitiva.
- Identificar e lidar com valores ausentes e duplicados.
- Gerar relatórios HTML interativos que podem ser compartilhados e visualizados facilmente por outras partes interessadas.

Os relatórios gerados a partir desta biblioteca servem como um ponto de partida robusto para uma análise de dados mais aprofundada e são um recurso inestimável para a exploração inicial de qualquer conjunto de dados.

---

Sinta-se à vontade para explorar os relatórios e visualizações neste site e compartilhar seus insights e feedback. Juntos, podemos aprimorar a prática da ciência de dados e criar uma comunidade mais inform
