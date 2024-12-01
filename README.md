
# Airbnb Rio Data Pipeline

## Descrição

Este projeto implementa um pipeline de dados no Azure, usando Python, Terraform e Blob Storage, para analisar tendências de hospedagem no Airbnb do Rio de Janeiro. O objetivo é explorar dados em múltiplas camadas (Raw, Bronze, Silver e Gold), gerar insights sobre preços, avaliações e sazonalidade, além de demonstrar habilidades em análise de dados, inteligência artificial e integração com a nuvem.

## Tecnologias Utilizadas

- **Python**: Ingestão, transformação e análise de dados.
- **Azure Blob Storage**: Armazenamento de camadas de dados (Raw, Bronze, Silver, Gold).
- **Terraform**: Provisionamento da infraestrutura no Azure.
- **Power BI**: Visualização interativa de insights.
- **Azure Functions** (opcional): Integração de modelos preditivos como APIs.

## Estrutura do Projeto

```plaintext
AirbnbRioDataPipeline/
├── terraform/           # Scripts Terraform para provisionar recursos no Azure
├── scripts/                 # Scripts Python para ETL e ingestão
│   ├── ingest_function/     # Código de Azure Functions (opcional)
│   ├── manual_ingest.py     # Script para ingestão manual de dados
│   ├── transform_silver.py  # Transformação da camada Bronze para Silver
│   ├── transform_gold.py    # Transformação da camada Silver para Gold
│   ├── database.py          # Gerenciamento do banco SQLite (opcional)
├── data/                    # Dados brutos, intermediários e processados
│   ├── raw/                 # Dados originais (Raw)
│   ├── bronze/              # Dados tratados inicialmente (Bronze)
│   ├── silver/              # Dados limpos e estruturados (Silver)
│   ├── gold/                # Dados finais com métricas (Gold)
├── README.md                # Documentação do projeto
├── .gitignore               # Arquivos ignorados no Git
└── LICENSE                  # Licença do projeto
```

## Funcionalidades

- Ingestão de dados brutos do Airbnb (camada Raw), preservando os dados originais.
- Tratamento inicial e padronização mínima dos dados (camada Bronze).
- Limpeza e estruturação de dados para análises (camada Silver).
- Agregações para insights e visualizações (camada Gold).
- Dashboards interativos no Power BI.
- Modelo preditivo para prever preços de hospedagem (opcional).

## Como Reproduzir

### Pré-requisitos

- Conta no Azure com créditos ativos.
- Python 3.9+ e bibliotecas necessárias:
  - `pandas`, `azure-storage-blob`, `matplotlib`.
- Terraform instalado na máquina local.
- Power BI Desktop para visualização.

### Passo a Passo

1. Clone este repositório:

   ```
   bash
   
   git clone git@github.com:alessandracruz/AirbnbRioDataPipeline.git
   ```

2. Configure o Azure Blob Storage:

   - Utilize os arquivos em `terraform/` para criar a infraestrutura.

3. Execute os scripts de ingestão:

   ```
   bash
   
   python scripts/ingest_raw.py
   ```

4. Limpe e transforme os dados:

   ```
   bash
   
   python scripts/transform_silver.py
   python scripts/transform_gold.py
   ```

5. Visualize no Power BI:

   - Conecte o Power BI ao Blob Storage e crie dashboards interativos.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.

## Contribuições

Contribuições são bem-vindas! Abra uma issue ou envie um pull request com melhorias ou novas funcionalidades.

## Contato

Se tiver dúvidas ou sugestões, entre em contato:

- **Nome**: Alessandra Cruz
- **E-mail**: [[alessandraccruz@pm.me](mailto:alessandraccruz@pm.me)]
- **GitHub**: [https://github.com/alessandracruz]