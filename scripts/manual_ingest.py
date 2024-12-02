"""
manual_ingest.py:
Script para fazer a ingestão manual de arquivos para o Blob Storage no Azure.

Passos:
1. Carregar arquivos do diretório local (camada RAW).
2. Enviar os arquivos para o container 'dataraw' no Azure Blob Storage.
"""

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

STORAGE_ACCOUNT_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING") 
CONTAINER_NAME = "dataraw"
LOCAL_RAW_DIR = "./data/raw" 

def upload_file_to_blob(file_path, blob_name):
    """
    Faz upload de um arquivo local para o Azure Blob Storage.
    Args:
        file_path (str): Caminho do arquivo local.
        blob_name (str): Nome do arquivo no Blob Storage.
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(STORAGE_ACCOUNT_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
        
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        
        print(f"Arquivo '{blob_name}' enviado para o container '{CONTAINER_NAME}'.")
    except Exception as e:
        print(f"Erro ao fazer upload do arquivo '{blob_name}': {e}")

def main():
    """
    Faz o upload de todos os arquivos da pasta RAW para o Blob Storage.
    """
    if not os.path.exists(LOCAL_RAW_DIR):
        print(f"O diretório '{LOCAL_RAW_DIR}' não existe.")
        return

    for file_name in os.listdir(LOCAL_RAW_DIR):
        file_path = os.path.join(LOCAL_RAW_DIR, file_name)
        if os.path.isfile(file_path):
            upload_file_to_blob(file_path, file_name)

if __name__ == "__main__":
    main()
