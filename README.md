# Algoritmo de Busqueda A* en un grafo de Rutas

Este proyecto implementa el algoritmo de busqueda A* para encontrar la ruta mas optima entre dos ubicaciones en un grafo
que representa una red de rutas.
El grafo se crea a partir de coordenadas Geograficas(latitud, longitud) de ubicaciones y las distancias entre ellas se
calculan utilizando la formula de la distancia haversine.

## Requisitos
- Python 3
- Bibliotecas de Python: pandas, networkx, matplotlib

## Como usar

1. Asegurate de tener Pyrhon 3 instalado en tu sistema.
2. Instala las Bibliotecas necesarias con 'pip install pandas networkx matplotlib'.
3. Ejecuta el script principal 'maps.py'.
4. Proporciona el nombre de inicio y destino en el grafo cuando se te solicite.

El programa buscara la ruta mas optima utilizando el algoritmo A* y la dibujara en un mapa.

## Estructura del Proyecto

- 'maps.py': El script principal que contiene las funciones de busqueda A* y la logica del programa.
- 'Coordenadas_Maps_UNSA.xlsx': Un archivo Excel que contiene las coordenadas geograficas de las ubicaciones.
- 'Aristas_Maps_UNSA.xlsx': Un archivo Excel que contiene las conexiones entre ubicaciones en el grafo.

## Creditos

- Desarrolado por Giomar Muñoz