from typing import List, Tuple
from datetime import datetime
import pandas as pd
import cProfile
import pstats

def get_username(user):
  return user['username']

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    result = []
    
    # Leer el archivo JSON línea por línea
    df = pd.read_json(file_path, lines=True)
    
    # Eliminar columnas innecesarias
    df = df[['date', 'user']] 
    
    # Obtener username
    df['username'] = df['user'].apply(get_username)

    # Calcular las 10 fechas con más tweets
    top_10_dates = pd.Series([date.date() for date in df['date']]).value_counts().index[:10]

    # Encontrar el usuario con más publicaciones para cada una de las 10 fechas principales en el chunk actual
    for date in top_10_dates:
        # Filtrar el DataFrame por fecha
        tweets_for_date = df[df['date'].dt.date == date]
        # Encontrar el usuario con más publicaciones para esta fecha
        top_user_for_date = tweets_for_date['username'].value_counts().idxmax()
        result.append((date, top_user_for_date))
     
    return result

# Ejecuta la función dentro del perfilador y guarda los resultados
profiler = cProfile.Profile()
profiler.enable()
file_path = "gs://challenge-de/farmers-protest-tweets-2021-2-4.json"
q1_time(file_path)
profiler.disable()

# Genera estadísticas a partir del perfil
stats = pstats.Stats(profiler)
# Imprime el resumen con el número total de llamadas y el tiempo total de ejecución
print(stats.total_calls, "function calls in", stats.total_tt, "seconds")
