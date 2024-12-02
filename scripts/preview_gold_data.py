"""
preview_gold_data.py:
Script para visualizar os dados agregados na camada Gold.
"""
import os
from azure.storage.blob import BlobServiceClient
import pandas as pd

def list_and_preview_blobs(connection_string, container_name):
    """
    Lista e visualiza arquivos no Azure Blob Storage.
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        blobs = container_client.list_blobs()
        for blob in blobs:
            print(f"\nPrévia do arquivo: {blob.name}")
            blob_client = container_client.get_blob_client(blob)
            download_stream = blob_client.download_blob()
            data = pd.read_csv(download_stream)
            print(data.head(10))  # Mostra as primeiras 10 linhas
            print(f"\nTotal de linhas: {len(data)}")
            print("-" * 50)
    except Exception as e:
        print(f"Erro ao acessar o container '{container_name}': {e}")

if __name__ == "__main__":
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        print("Erro: A variável de ambiente AZURE_STORAGE_CONNECTION_STRING não está configurada.")
    else:
        gold_container = "datagold"
        list_and_preview_blobs(connection_string, gold_container)
