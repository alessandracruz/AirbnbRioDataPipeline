"""
preview_silver_data.py:
Exibe uma prévia dos arquivos transformados na camada Silver.
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
        return data
    except Exception as e:
        print(f"Erro ao carregar o arquivo '{blob_name}': {e}")
        return None

def preview_silver_data(connection_string, container_name, nrows=10):
    """
    Exibe uma prévia de todos os arquivos no container da camada Silver.
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        print(f"Pré-visualizando arquivos no container '{container_name}':\n")
        for blob in container_client.list_blobs():
            blob_name = blob.name
            print(f"Prévia do arquivo: {blob_name}")
            df = download_blob_to_dataframe(connection_string, container_name, blob_name)
            if df is not None:
                print(df.head(nrows)) 
                print(f"\nTotal de linhas: {len(df)}\n{'-' * 50}\n")
    except Exception as e:
        print(f"Erro ao pré-visualizar dados: {e}")

if __name__ == "__main__":
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        print("Erro: A variável de ambiente AZURE_STORAGE_CONNECTION_STRING não está configurada.")
    else:
        silver_container = "datasilver"
        preview_silver_data(connection_string, silver_container)
