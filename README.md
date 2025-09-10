# LAB02: Análise de Qualidade de Sistemas Java

## Visão Geral

Este repositório contém o código e a documentação para o Laboratório 02 do curso de Engenharia de Software, focado na experimentação de software. O objetivo principal é analisar as características de qualidade de repositórios Java populares no GitHub, correlacionando-as com características do processo de desenvolvimento. Utilizaremos a ferramenta CK (CodeKeeper) para análise estática de código e métricas de qualidade.

## Questões de Pesquisa

Este laboratório busca responder às seguintes questões de pesquisa:

*   **RQ 01:** Qual a relação entre a popularidade dos repositórios e suas características de qualidade?
*   **RQ 02:** Qual a relação entre a maturidade dos repositórios e suas características de qualidade?
*   **RQ 03:** Qual a relação entre a atividade dos repositórios e suas características de qualidade?
*   **RQ 04:** Qual a relação entre o tamanho dos repositórios e suas características de qualidade?

## Métricas

As seguintes métricas serão utilizadas para responder às questões de pesquisa:

**Métricas de Processo:**

*   **Popularidade:** Número de estrelas no GitHub.
*   **Tamanho:** Linhas de código (LOC) e linhas de comentários.
*   **Atividade:** Número de releases.
*   **Maturidade:** Idade (em anos) do repositório.

**Métricas de Qualidade (calculadas com CK):**

*   **CBO (Coupling Between Objects):** Mede o acoplamento entre objetos.
*   **DIT (Depth Inheritance Tree):** Mede a profundidade da árvore de herança.
*   **LCOM (Lack of Cohesion of Methods):** Mede a falta de coesão entre métodos.

## Metodologia

1.  **Seleção de Repositórios:** Coletaremos os 1.000 repositórios Java mais populares do GitHub.
2.  **Coleta e Análise de Dados:**
    *   Utilizaremos as APIs REST ou GraphQL do GitHub para coletar informações de popularidade, atividade e maturidade.
    *   Utilizaremos a ferramenta CK para medir as métricas de qualidade.
    *   É importante sumarizar os dados obtidos, pois a ferramenta CK gera múltiplos arquivos .csv.

## Processo de Desenvolvimento

O processo de desenvolvimento será dividido em duas etapas principais:

*   **Lab02S01:** Criação de uma lista dos 1.000 repositórios Java, desenvolvimento de um script para automatizar o clone dos repositórios e a coleta das métricas, e geração de um arquivo .csv com os resultados das medições de um repositório de teste.
*   **Lab02S02:** Geração de um arquivo .csv contendo os resultados de todas as medições dos 1.000 repositórios, formulação de hipóteses, análise e visualização dos dados, e elaboração do relatório final.

## Setup

*   **Linguagem:** Python (detalhes sobre as bibliotecas utilizadas serão adicionados posteriormente)
*   **API:** GitHub GraphQL API
*   **Ferramenta de Análise Estática:** CK (CodeKeeper)
*   **Ferramentas:** (A lista de ferramentas específicas será adicionada conforme o desenvolvimento)

## Bônus

Para aprofundar a análise, será realizado um teste estatístico (por exemplo, teste de correlação de Spearman ou de Pearson) para avaliar a significância das correlações encontradas entre as métricas. Gráficos de correlação serão gerados para visualizar o comportamento dos dados.

## Contributing

Este projeto é desenvolvido por [Gabriel Ramos Ferreira](https://github.com/gramos22) e [João Pedro Braga](https://github.com/joaopedro-braga). Contribuições são bem-vindas, mas por favor, entre em contato conosco antes de propor mudanças significativas.

## Referências

*   [Link para o cronograma do laboratório](https://github.com/joaopauloaramuni/laboratorio-de-experimentacao-de-software/tree/main/CRONOGRAMA)
