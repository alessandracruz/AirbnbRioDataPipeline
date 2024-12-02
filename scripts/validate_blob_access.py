import os
from azure.storage.blob import ContainerClient

def list_blobs_in_container(connection_string, container_name):
    """
    Lista todos os blobs no container especificado.
    Args:
        connection_string (str): String de conexão do Azure Storage.
        container_name (str): Nome do container a ser listado.
    """
    try:
        container_client = ContainerClient.from_connection_string(connection_string, container_name)
        blobs = container_client.list_blobs()
        print(f"Arquivos no container '{container_name}':")
        for blob in blobs:
            print(f"- {blob.name}")
    except Exception as e:
        print(f"Erro ao acessar o container '{container_name}': {e}")

if __name__ == "__main__":
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        print("Erro: A variável de ambiente AZURE_STORAGE_CONNECTION_STRING não está configurada.")
    else:
        container_name = "dataraw"
        list_blobs_in_container(connection_string, container_name)
