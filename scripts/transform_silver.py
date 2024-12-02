"""
transform_silver.py:
Transforma os dados da camada Bronze para Silver, incluindo traduções e ajustes finais.
"""
import os
import pandas as pd
from azure.storage.blob import BlobServiceClient

def download_blob_to_dataframe(connection_string, container_name, blob_name):
    """
    Faz o download de um blob e retorna como um DataFrame do Pandas.
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        download_stream = blob_client.download_blob()
        data = pd.read_csv(download_stream)
        print(f"Arquivo '{blob_name}' carregado com sucesso.")
        return data
    except Exception as e:
        print(f"Erro ao carregar o arquivo '{blob_name}': {e}")
        return None

def save_dataframe_to_blob(dataframe, connection_string, container_name, blob_name):
    """
    Salva um DataFrame no Azure Blob Storage como CSV.
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(dataframe.to_csv(index=False), overwrite=True)
        print(f"Arquivo '{blob_name}' salvo no container '{container_name}' com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar o arquivo '{blob_name}': {e}")

def transform_listings(df):
    """
    Aplica transformações nos dados de 'listings.csv'.
    """
    df.rename(columns={
        "id": "id_anuncio",
        "listing_url": "url_anuncio",
        "price": "preco",
        "availability_365": "disponibilidade_365",
        "name": "nome",
        "host_name": "nome_anfitriao",
        "neighbourhood": "bairro",
        "neighbourhood_group": "regiao_bairro",
        "room_type": "tipo_acomodacao",
        "review_scores_rating": "avaliacao"
        # Adicione mais traduções conforme necessário
    }, inplace=True)

    if "preco" in df.columns:
        df["preco"] = df["preco"].replace('[\$,]', '', regex=True).astype(float).apply(lambda x: f"R$ {x * 5.00:.2f}")

    df.drop_duplicates(inplace=True)

    return df

def transform_calendar(df):
    """
    Aplica transformações nos dados de 'calendar.csv'.
    """
    df.rename(columns={
        "listing_id": "id_anuncio",
        "date": "data",
        "available": "disponivel",
        "price": "preco",
        "adjusted_price": "preco_ajustado",
        "minimum_nights": "minimo_noites",
        "maximum_nights": "maximo_noites",
    }, inplace=True)

    if "preco" in df.columns:
        df["preco"] = df["preco"].replace('[\$,]', '', regex=True).astype(float).apply(lambda x: f"R$ {x * 5.00:.2f}")
    if "preco_ajustado" in df.columns:
        df["preco_ajustado"] = df["preco_ajustado"].replace('[\$,]', '', regex=True).astype(float).apply(lambda x: f"R$ {x * 5.00:.2f}")

    df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d")

    df.drop_duplicates(inplace=True)

    return df

if __name__ == "__main__":
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        print("Erro: A variável de ambiente AZURE_STORAGE_CONNECTION_STRING não está configurada.")
    else:
        bronze_container = "databronze"
        silver_container = "datasilver"

        listings_blob = "listings.csv"
        listings_df = download_blob_to_dataframe(connection_string, bronze_container, listings_blob)
        if listings_df is not None:
            transformed_listings = transform_listings(listings_df)
            save_dataframe_to_blob(transformed_listings, connection_string, silver_container, listings_blob)

        calendar_blob = "calendar.csv"
        calendar_df = download_blob_to_dataframe(connection_string, bronze_container, calendar_blob)
        if calendar_df is not None:
            transformed_calendar = transform_calendar(calendar_df)
            save_dataframe_to_blob(transformed_calendar, connection_string, silver_container, calendar_blob)
