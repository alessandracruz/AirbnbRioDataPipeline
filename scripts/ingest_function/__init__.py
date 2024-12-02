"""
Azure Function - Demonstração de Ingestão Automática
Usa um Timer Trigger para monitorar e enviar arquivos RAW automaticamente.
"""

import os
import datetime
from azure.storage.blob import BlobServiceClient
import logging

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
        
        logging.info(f"Arquivo '{blob_name}' enviado para o container '{CONTAINER_NAME}'.")
    except Exception as e:
        logging.error(f"Erro ao fazer upload do arquivo '{blob_name}': {e}")

def main(mytimer: dict):
    """
    Timer Trigger que executa a ingestão automática.
    Args:
        mytimer (dict): Timer Trigger configurado no `function.json`.
    """
    utc_timestamp = datetime.datetime.utcnow().isoformat()
    logging.info(f"Azure Function executada às {utc_timestamp}")

    # Ingestão Automática
    if not os.path.exists(LOCAL_RAW_DIR):
        logging.warning(f"O diretório '{LOCAL_RAW_DIR}' não existe.")
        return

    for file_name in os.listdir(LOCAL_RAW_DIR):
        file_path = os.path.join(LOCAL_RAW_DIR, file_name)
        if os.path.isfile(file_path):
            upload_file_to_blob(file_path, file_name)


