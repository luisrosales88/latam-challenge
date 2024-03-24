from typing import List, Tuple
import re
from collections import Counter
import pandas as pd
from google.cloud import storage
import json

# Función para extraer emojis de un tweet
def extract_emojis(tweet):
    # Expresión regular para encontrar emojis en un tweet
    emoji_regex = re.compile(r':\w+:|[\U0001F1E0-\U0001F1FF]|[\U0001F300-\U0001F5FF]|[\U0001F600-\U0001F64F]|[\U0001F680-\U0001F6FF]|[\U0001F700-\U0001F77F]|[\U0001F780-\U0001F7FF]|[\U0001F800-\U0001F8FF]|[\U0001F900-\U0001F9FF]|[\U0001FA00-\U0001FA6F]|[\U0001FA70-\U0001FAFF]|[\U00002702-\U000027B0]', flags=re.UNICODE)
    return emoji_regex.findall(tweet)

# Función principal para contar los emojis más utilizados en los tweets
@profile
def q2_memory(file_path: str) -> List[Tuple[str, int]]:

    # Inicializar cliente de Google Cloud Storage
    client = storage.Client()

    # Obtener el nombre del bucket y del blob del archivo
    bucket_name, blob_name = file_path.replace("gs://", "").split("/", 1)

    # Obtener el bucket
    bucket = client.bucket(bucket_name)

    # Obtener el blob
    blob = bucket.blob(blob_name)

    # Descargar el archivo a un archivo temporal
    with open("/tmp/temp.json", "wb") as f:
        blob.download_to_file(f)

    # Contador para contar la frecuencia de cada emoji
    emoji_counts = Counter()
    with open("/tmp/temp.json", 'r', encoding='utf-8') as file:
        for line in file:
            tweet = json.loads(line)
            # Extraer emojis del contenido del tweet
            emojis = extract_emojis(tweet['content'].lower())
            # Actualizar el contador de emojis
            emoji_counts.update(emojis)
    
    # Obtener los 10 emojis más utilizados
    most_used_emojis = emoji_counts.most_common(10)
    return most_used_emojis

if __name__ == '__main__':
    # Ruta del archivo JSON en Google Cloud Storage
    file_path = "gs://challenge-de/farmers-protest-tweets-2021-2-4.json"
    # Llamar a la función principal e imprimir los resultados
    print(q2_memory(file_path))