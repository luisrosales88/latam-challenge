from typing import List, Tuple
from google.cloud import storage
import json

@profile
def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    # Inicializar un diccionario para almacenar la frecuencia de los nombres de usuario
    username_count = {}

    # Inicializar el cliente de Google Cloud Storage
    client = storage.Client()

    # Obtener el nombre del bucket y el nombre del objeto
    bucket_name, blob_name = file_path.replace("gs://", "").split("/", 1)

    # Obtener el bucket
    bucket = client.bucket(bucket_name)

    # Obtener el blob
    blob = bucket.blob(blob_name)

    # Leer el archivo línea por línea
    with blob.open("r") as file:
        for line in file:
            tweet = json.loads(line)
            mentioned_users = tweet.get('mentionedUsers')  # Obtener la lista de usuarios mencionados
            if mentioned_users is not None:
                for user in mentioned_users:
                    username = user.get('username')
                    if username:  # Verificar si se proporciona un nombre de usuario
                        # Incrementar el contador para este nombre de usuario
                        username_count[username] = username_count.get(username, 0) + 1

    # Ordenar el diccionario por la frecuencia de menciones en orden descendente
    sorted_username_count = sorted(username_count.items(), key=lambda x: x[1], reverse=True)

    # Tomar los top 10 usuarios más mencionados
    top_10_users = sorted_username_count[:10]

    return top_10_users

if __name__ == '__main__':
    file_path = "gs://challenge-de/farmers-protest-tweets-2021-2-4.json"
    print(q3_memory(file_path))