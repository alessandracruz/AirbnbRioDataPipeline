"""
download_bronze_file.py:
Faz o download de todos os arquivos da camada Bronze para validação.
"""

import os
from azure.storage.blob import BlobServiceClient

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

def download_all_files_from_bronze(container_name, download_directory):
    """
    Faz o download de todos os arquivos do container da camada Bronze.
    Args:
        container_name (str): Nome do container.
        download_directory (str): Diretório local para salvar os arquivos.
    """
    try:
        container_client = blob_service_client.get_container_client(container_name)

        os.makedirs(download_directory, exist_ok=True)
        print(f"Baixando arquivos do container '{container_name}' para '{download_directory}'...\n")
        for blob in container_client.list_blobs():
            blob_name = blob.name
            blob_path = os.path.join(download_directory, blob_name)

            print(f"Baixando arquivo: {blob_name}...")
            blob_client = container_client.get_blob_client(blob_name)
            with open(blob_path, "wb") as file:
                file.write(blob_client.download_blob().readall())
            print(f"'{blob_name}' baixado com sucesso para '{blob_path}'.\n")
    except Exception as e:
        print(f"Erro ao baixar arquivos do container '{container_name}': {e}")

if __name__ == "__main__":
    container_name = "databronze"  
    download_directory = "./data/bronze/"  

    download_all_files_from_bronze(container_name, download_directory)
