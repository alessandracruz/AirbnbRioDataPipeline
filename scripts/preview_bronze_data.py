"""
preview_bronze_data.py:
Exibe uma prévia dos arquivos da camada Bronze.
"""

import os
import pandas as pd

def preview_csv(file_path, nrows=10):
    """
    Exibe as primeiras linhas de um arquivo CSV.
    Args:
        file_path (str): Caminho do arquivo CSV.
        nrows (int): Número de linhas a serem exibidas.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"\nPrévia do arquivo: {os.path.basename(file_path)}")
        print(df.head(nrows))
        print(f"\n{len(df)} linhas no total.")
    except Exception as e:
        print(f"Erro ao carregar o arquivo '{file_path}': {e}")

if __name__ == "__main__":
    directory = "./data/bronze/"
    nrows = 25 

    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            preview_csv(os.path.join(directory, file_name), nrows)
