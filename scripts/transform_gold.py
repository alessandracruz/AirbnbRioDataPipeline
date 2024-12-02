"""
transform_gold.py:
Agrega e processa os dados da camada Silver para gerar a camada Gold.
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

def process_gold_data(calendar_df, listings_df):
    listings_df["preco_num"] = listings_df["preco"].str.replace("R$", "").str.replace(",", "").astype(float)

    price_by_region_type = listings_df.groupby(["bairro", "tipo_acomodacao"]).agg(
        preco_medio=("preco_num", lambda x: round(x.mean(), 2)),
        total_listings=("id_anuncio", "count")
    ).reset_index()

    price_by_region_type["preco_medio"] = price_by_region_type["preco_medio"].apply(lambda x: f"R$ {x}")

    calendar_df["data"] = pd.to_datetime(calendar_df["data"])
    calendar_df["mes"] = calendar_df["data"].dt.to_period("M")
    occupancy_rate = calendar_df.groupby(["mes", "id_anuncio"]).agg(
        ocupacao=("disponivel", lambda x: round((x == "t").mean() * 100, 1))
    ).reset_index()

    popularity_by_type = listings_df.groupby("tipo_acomodacao").agg(
        total_listings=("id_anuncio", "count"),
        avaliacao_media=("avaliacao", lambda x: x.dropna().mean())  # Ignorar valores nulos
    ).reset_index()

    return price_by_region_type, occupancy_rate, popularity_by_type

if __name__ == "__main__":
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        print("Erro: A variável de ambiente AZURE_STORAGE_CONNECTION_STRING não está configurada.")
    else:
        silver_container = "datasilver"
        gold_container = "datagold"

        calendar_blob = "calendar.csv"
        listings_blob = "listings.csv"

        calendar_df = download_blob_to_dataframe(connection_string, silver_container, calendar_blob)
        listings_df = download_blob_to_dataframe(connection_string, silver_container, listings_blob)

        if calendar_df is not None and listings_df is not None:
            price_by_region_type, occupancy_rate, popularity_by_type = process_gold_data(calendar_df, listings_df)

            save_dataframe_to_blob(price_by_region_type, connection_string, gold_container, "price_by_region_type.csv")
            save_dataframe_to_blob(occupancy_rate, connection_string, gold_container, "occupancy_rate.csv")
            save_dataframe_to_blob(popularity_by_type, connection_string, gold_container, "popularity_by_type.csv")
