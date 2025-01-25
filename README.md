# Airbnb Rio Data Pipeline

## Descrição

Este projeto implementa um pipeline de dados no Azure, usando Python, Terraform e Blob Storage, para analisar tendências de hospedagem no Airbnb do Rio de Janeiro. O objetivo é explorar dados em múltiplas camadas (Raw, Bronze, Silver e Gold), gerar insights sobre preços, avaliações e sazonalidade, além de demonstrar habilidades em análise de dados, inteligência artificial e integração com a nuvem. Além disso, para garantir a segurança dos dados, foi criado um backup na nuvem utilizando o Microsoft Fabric e o OneLake, que assegura a continuidade e acessibilidade dos dados para estudos futuros.

## Tecnologias Utilizadas

- **Python**: Ingestão, transformação e análise de dados.
- **Azure Blob Storage**: Armazenamento de camadas de dados (Raw, Bronze, Silver, Gold).
- **Terraform**: Provisionamento da infraestrutura no Azure.
- **Power BI**: Visualização interativa de insights.
- **Azure Functions** (opcional): Integração de modelos preditivos como APIs.

## Estrutura do Projeto

```
AirbnbRioDataPipeline/
├── terraform/                # Scripts Terraform para provisionar recursos no Azure
├── scripts/                  # Scripts Python para ETL e ingestão
│   ├── ingest_function/      # Código de Azure Functions (opcional)
│   ├── manual_ingest.py      # Script para ingestão manual de dados
│   ├── download_bronze_file.py  # Download de dados da camada Bronze
│   ├── download_silver_file.py  # Download de dados da camada Silver
│   ├── download_gold_data.py    # Download de dados da camada Gold
│   ├── transform_bronze.py   # Transformação da camada Raw para Bronze
│   ├── transform_silver.py   # Transformação da camada Bronze para Silver
│   ├── transform_gold.py     # Transformação da camada Silver para Gold
│   ├── validate_blob_access.py  # Validação de acesso ao Blob Storage
│   ├── preview_bronze_data.py   # Pré-visualização de dados Bronze
│   ├── preview_silver_data.py   # Pré-visualização de dados Silver
│   ├── preview_gold_data.py     # Pré-visualização de dados Gold
│   ├── database.py           # Gerenciamento do banco SQLite (opcional)
├── data/                     # Dados brutos, intermediários e processados (Pasta no .gitignore)
│   ├── raw/                  # Dados originais (Raw)
│   ├── bronze/               # Dados tratados inicialmente (Bronze)
│   ├── silver/               # Dados limpos e estruturados (Silver)
│   ├── gold/                 # Dados finais com métricas (Gold)
├── visualizations/           # Dashboards e relatórios do Power BI (Pasta no .gitignore)
│   ├── airbnb_rio_data_pipeline.pbix  # Arquivo do Power BI
├── README.md                 # Documentação do projeto
├── .gitignore                # Arquivos ignorados no Git
└── LICENSE                   # Licença do projeto
```

## Funcionalidades

- **Backup na Nuvem**: Dados do pipeline armazenados em um **Lakehouse** no **OneLake** para segurança e acessibilidade futura.
- Ingestão de dados brutos do Airbnb (camada Raw), preservando os dados originais.
- Tratamento inicial e padronização mínima dos dados (camada Bronze).
- Limpeza e estruturação de dados para análises (camada Silver).
- Agregações para insights e visualizações (camada Gold).
- Dashboards interativos no Power BI.
- Modelo preditivo (AI) para prever preços de hospedagem (em andamento).

## Arquitetura

A arquitetura do projeto segue um fluxo típico de Engenharia de Dados com múltiplas etapas de validação, transformação e visualização. O processo é implementado através de scripts Python, utilizando recursos provisionados no Azure com Terraform, e finaliza com dashboards no Power BI. 

### Fluxo do Pipeline de Dados

![Airbnb Rio Data Pipeline Flow](https://github.com/alessandracruz/Imagens/blob/main/Airbnb%20Rio%20Data%20Pipeline%20Flow.png)

O pipeline segue os seguintes passos:

1. **Validação dos Dados (validate_blob_access.py)**:
   - Garantia de que os arquivos estão disponíveis no Blob Storage.

2. **Transformação Bronze (transform_bronze.py)**:
   - Padronização inicial dos dados, aplicando regras mínimas de qualidade.

3. **Transformação Silver (transform_silver.py)**:
   - Limpeza e estruturação dos dados para análises aprofundadas.

4. **Transformação Gold (transform_gold.py)**:
   - Agregação e cálculo de métricas para visualização.

5. **Provisionamento da Infraestrutura (Terraform)**:
   - Criação e gerenciamento dos recursos necessários na nuvem Azure.

6. **Visualização de Dados (Power BI)**:
   - Criação de dashboards interativos para análise e apresentação de insights.


------

## Backup e Continuidade

Para evitar custos adicionais com a infraestrutura do Azure, os Resource Groups utilizados foram excluídos. Contudo, os dados foram previamente salvos no **Microsoft Fabric**, garantindo que possam ser recuperados e reutilizados no futuro.

### Passos realizados:

1. Os dados foram organizados nas camadas **Raw**, **Bronze**, **Silver**, e **Gold** e salvos localmente.
2. Em seguida, foram carregados para um **Lakehouse** no **Microsoft Fabric**, integrado ao **OneLake**, mantendo a estrutura de pastas original.
3. Essa abordagem permite recriar os Resource Groups futuramente utilizando os scripts do Terraform.

### Gerenciamento dos Resource Groups com Terraform

Para destruir o Resource Group e evitar custos adicionais, utilize o seguinte comando:

```
terraform destroy
```

> **Observação:** Certifique-se de estar no diretório que contém o arquivo `main.tf` antes de executar este comando.

Se for necessário recriar os recursos futuramente, basta utilizar o comando abaixo:

```
terraform apply
```

> **Importante:** Antes de recriar os recursos, valide que os arquivos `.tfstate` e `.tfstate.backup` ainda estão presentes. Eles são essenciais para o Terraform reconhecer o estado anterior da infraestrutura.

Essa estratégia garante que o pipeline possa ser retomado facilmente no futuro, mantendo a integridade dos dados e da infraestrutura.

------

## Como Reproduzir

### Pré-requisitos

- Conta no Azure com créditos ativos.
- Python 3.9+ e bibliotecas necessárias:
  - `pandas`, `azure-storage-blob`.
- Terraform instalado na máquina local.
- Power BI Desktop para visualização.

### Passo a Passo

1. Clone este repositório:

   ```
   git clone git@github.com:alessandracruz/AirbnbRioDataPipeline.git
   ```

2. Configure o Azure Blob Storage:

   - Utilize os arquivos em `terraform/` para criar a infraestrutura.

3. Execute os scripts de ingestão:

   ```
   python scripts/manual_ingest.py
   ```

4. Limpe e transforme os dados:

   ```
   python scripts/transform_bronze.py
   python scripts/transform_silver.py
   python scripts/transform_gold.py
   ```

5. Visualize no Power BI:

   - As visualizações de Power BI não estão incluídas neste repositório como uma boa prática.   A sugestão é que cada pessoa crie suas próprias visualizações a partir dos dados fornecidos nas camadas Raw, Bronze, Silver ou Gold, de acordo com o objetivo de análise desejado.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.

## Contribuições

Contribuições são bem-vindas! Abra uma issue ou envie um pull request com melhorias ou novas funcionalidades.

## Contato

Se tiver dúvidas ou sugestões, entre em contato:

- **Nome**: Alessandra Cruz
- **E-mail**: [alessandraccruz@pm.me](mailto:alessandraccruz@pm.me)
- **GitHub**: https://github.com/alessandracruz