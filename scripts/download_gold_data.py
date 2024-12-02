"""
download_gold_data.py:
Script para baixar os arquivos da camada Gold do Azure Blob Storage.
"""
import os
from azure.storage.blob import BlobServiceClient

def download_blobs(connection_string, container_name, local_folder):
    """
    Faz o download de todos os arquivos de um container para um diretório local.
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        blobs = container_client.list_blobs()
        for blob in blobs:
            blob_client = container_client.get_blob_client(blob)
            local_file_path = os.path.join(local_folder, blob.name)

            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            with open(local_file_path, "wb") as file:
                file.write(blob_client.download_blob().readall())
                print(f"Arquivo '{blob.name}' baixado para '{local_file_path}'.")
    except Exception as e:
        print(f"Erro ao baixar arquivos do container '{container_name}': {e}")

if __name__ == "__main__":
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        print("Erro: A variável de ambiente AZURE_STORAGE_CONNECTION_STRING não está configurada.")
    else:
        gold_container = "datagold"
        local_folder = "data/gold" 
        download_blobs(connection_string, gold_container, local_folder)
