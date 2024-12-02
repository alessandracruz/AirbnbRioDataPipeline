import os
import pandas as pd
from azure.storage.blob import BlobServiceClient

def download_blob_to_dataframe(connection_string, container_name, blob_name):
    """
    Faz o download de um blob do Azure Storage e carrega como um DataFrame do Pandas.
    Args:
        connection_string (str): String de conexão do Azure Storage.
        container_name (str): Nome do container.
        blob_name (str): Nome do blob.
    Returns:
        pd.DataFrame: Dados carregados em um DataFrame.
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        download_stream = blob_client.download_blob()
        data = pd.read_csv(download_stream)
        print(f"Arquivo '{blob_name}' carregado com sucesso.")
        return data
    except Exception as e:
        print(f"Erro ao baixar o arquivo '{blob_name}': {e}")
        return None

def upload_dataframe_to_blob(dataframe, connection_string, container_name, blob_name):
    """
    Envia um DataFrame como um arquivo CSV para o Azure Storage.
    Args:
        dataframe (pd.DataFrame): Dados a serem enviados.
        connection_string (str): String de conexão do Azure Storage.
        container_name (str): Nome do container de destino.
        blob_name (str): Nome do blob de destino.
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(dataframe.to_csv(index=False), overwrite=True)
        print(f"Arquivo '{blob_name}' enviado com sucesso para o container '{container_name}'.")
    except Exception as e:
        print(f"Erro ao enviar o arquivo '{blob_name}': {e}")

if __name__ == "__main__":
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        print("Erro: A variável de ambiente AZURE_STORAGE_CONNECTION_STRING não está configurada.")
    else:
        raw_files = ["listings.csv", "calendar.csv"]
        raw_container = "dataraw"
        bronze_container = "databronze"

        for file_name in raw_files:
            df = download_blob_to_dataframe(connection_string, raw_container, file_name)
            if df is not None:
                upload_dataframe_to_blob(df, connection_string, bronze_container, file_name)
