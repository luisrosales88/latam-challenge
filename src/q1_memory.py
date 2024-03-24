from typing import List, Tuple
from datetime import datetime
import pandas as pd

# Función para obtener username del tweet
def get_username(user):
    return user['username']

@profile
def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    result = []
    date_user_counts = {}  # Diccionario para almacenar el número de publicaciones de cada usuario en cada fecha

    # Leer el archivo JSON línea por línea y procesarlo en chunks
    chunk_size = 10000  # Tamaño del chunk ajustable
    reader = pd.read_json(file_path, lines=True, chunksize=chunk_size)
    
    for chunk in reader:
        # Eliminar columnas innecesarias
        chunk = chunk[['date', 'user']]
        # Obtener username
        chunk['username'] = chunk['user'].apply(get_username)

        # Calcular el número de publicaciones de cada usuario en cada fecha en el chunk actual
        user_counts_chunk = chunk.groupby([chunk['date'].dt.date, 'username']).size()

        # Actualizar el número de publicaciones de cada usuario en cada fecha acumulado
        for (date, username), count in user_counts_chunk.items():
            if date not in date_user_counts:
                date_user_counts[date] = {}
            if username not in date_user_counts[date]:
                date_user_counts[date][username] = 0
            date_user_counts[date][username] += count

    # Encontrar las 10 fechas con más tweets en todos los chunks
    top_10_dates = sorted(date_user_counts, key=lambda x: sum(date_user_counts[x].values()), reverse=True)[:10]

    # Encontrar el usuario con más publicaciones para cada una de las 10 fechas principales
    for date in top_10_dates:
        # Seleccionar las ocurrencias de usuario para la fecha actual
        user_counts_for_date = date_user_counts[date]
        # Encontrar el usuario con más publicaciones para esta fecha
        top_user_for_date = max(user_counts_for_date, key=user_counts_for_date.get)
        result.append((date, top_user_for_date))

    return result

if __name__ == '__main__':
    file_path = "gs://challenge-de/farmers-protest-tweets-2021-2-4.json"
    print(q1_memory(file_path))