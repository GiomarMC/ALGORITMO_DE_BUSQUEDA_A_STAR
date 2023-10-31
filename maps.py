import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2

#FUNCION PARA DETERMINAR LA HEURISTICA DE ALGORITMO DE BUSQUEDA A*
def heuristica(Graph, node, destination):
    lat1, lon1 = Graph.nodes[node]['latitude'], Graph.nodes[node]['longitude']
    lat2, lon2 = Graph.nodes[destination]['latitude'], Graph.nodes[destination]['longitude']

    heuristica = haversine_distance(lat1, lon1, lat2, lon2)
    return heuristica

#FUNCION DE BUSQUEDA DEL ALGORITMO A*
def a_star(Graph, start, end):
    came_from = {}
    open_set = set([start])
    closed_set = set()
    g_score =  {node: float('inf') for node in Graph.nodes()}
    g_score[start] = 0
    f_score = {node: float('inf') for node in Graph.nodes()}
    f_score[start] = heuristica(Graph, start, end)

    while open_set:
        current = min(open_set, key=lambda node: f_score[node])

        if current == end:
            path = []
            while current is not None:
                path.insert(0, current)
                current = came_from.get(current)
            return path
        
        open_set.remove(current)
        closed_set.add(current)

        for neighbor in Graph.neighbors(current):
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + Graph[current][neighbor]['weight']

            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristica(Graph, neighbor, end)

    return None

#FUNCION PARA DETERMINAR LA DISTANCIA ENTRE DOS PUNTOS UBICADOS EN UNA ESFERA(TIERRA)
def haversine_distance(latitud1, longitud1, latitud2, longitud2):
    radio = 6371.0

    latitud1 = radians(latitud1)
    longitud1 = radians(longitud1)
    latitud2 = radians(latitud2)
    longitud2 = radians(longitud2)

    diferencia_lat = latitud2 - latitud1
    diferencia_lon = longitud2 - longitud1

    a = sin(diferencia_lat/2)**2 + cos(latitud1) * cos(latitud2) * sin(diferencia_lon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radio * c

    return round(distance*1000, 2)

#FUNCION QUE DIBUJA EL GRAFO CON SUS RESPECTIVAS ETIQUETAS Y CAMINO TRAZADO
def dibujar_grafo(Graph, short_path):
    pos = {node: (Graph.nodes[node]["longitude"], Graph.nodes[node]["latitude"]) for node in Graph.nodes()}

    edge_labels = {(u,v): data['weight'] for u,v, data in Graph.edges(data = True)}

    nx.draw(Graph, pos, with_labels = True, node_size = 5, node_color = "red", font_size = 7)
    #nx.draw_networkx_edge_labels(Graph, pos, edge_labels= edge_labels, font_size = 5)

    plt.savefig("Mapa_Ingenierias_UNSA")

    short_path_edges = [(short_path[i], short_path[i + 1]) for i in range(len(short_path) - 1)]
    edge_color = ["blue" if (u, v) in short_path_edges or (v, u) in short_path_edges else "black" for u, v in Graph.edges()]

    nx.draw_networkx_edges(Graph, pos, edgelist = short_path_edges, edge_color = "blue", width = 2)
    
    labels = {node: node for node in Graph.nodes()}
    nx.draw_networkx_labels(Graph, pos, labels = labels, font_size = 7)

    plt.savefig("Mapa_Camino_Trazado_UNSA")

#FUNCION PARA AÑADIR NODOS AL GRAFO A TRAVEZ DE UN DATAFRAME
def addNodes(Grafo, index, dataframe):
    for i in range(0,index):
        nombre = str(dataframe.iloc[i,0])
        latitud = dataframe.iloc[i,1]
        longitud = dataframe.iloc[i,2]

        Grafo.add_node(nombre, latitude = latitud, longitude = longitud)

#FUNCION PARA AÑADIR ARISTAS AL GRAFO A TRAVEZ DE UN DATAFRAME
def addEdges(Grafo, index, dataframe):
    for index, row in dataframe.iterrows():
        node_1 = str(row['Nodo_1'])
        node_2 = str(row['Nodo_2'])

        latitud_1, longitud_1 = Grafo.nodes[node_1]['latitude'], Grafo.nodes[node_1]['longitude']
        latitud_2, longitud_2 = Grafo.nodes[node_2]['latitude'], Grafo.nodes[node_2]['longitude']

        distance = haversine_distance(latitud_1, longitud_1, latitud_2, longitud_2)

        Grafo.add_edge(node_1,node_2, weight = distance)

        dataframe.at[index, 'Distancia'] = distance

def distancia_total(Graph, path):
    distancia_total = 0

    for i in range(len(path) - 1):
        node1 = path[i]
        node2 = path[i + 1]

        distancia = Graph[node1][node2]['weight']

        distancia_total += distancia

    return distancia_total


#DATAFRAMES UTILIZADOS PARA LA CREACION DEL GRAFO
df_nodes = pd.read_excel("Coordenadas_Maps_UNSA.xlsx")
df_edges = pd.read_excel("Aristas_Maps_UNSA.xlsx")
print(df_nodes)
print(df_edges)

Maps = nx.Graph()

addNodes(Maps, len(df_nodes.index), df_nodes)
addEdges(Maps, len(df_edges.index), df_edges)

#SE GUARDAN LOS CAMBIOS DE LAS ARISTAS EN UN NUEVO DATAFRAME CON SUS RESPECTIVOS PESOS(DISTANCIA)
df_edges.to_excel("Aristas_Distancias_Maps_UNSA.xlsx", index = False)

for node in Maps.nodes():
    print(f"Nombre del Nodo: {node}")

Nodo_inicio = str(input("Ingresa el nodo de inicio: "))
Nodo_destino = str(input("Ingresa el nodo destino: "))

Camino_corto = a_star(Maps, Nodo_inicio, Nodo_destino)

if Camino_corto:
    print("Ruta mas corta: ", Camino_corto)
    print("La distancia total a recorrer es de: ", round(distancia_total(Maps, Camino_corto),2), "metros")
    dibujar_grafo(Maps, Camino_corto)
else:
    print("No se encontro una ruta.")
    dibujar_grafo(Maps, [])

for u,v, data in Maps.edges(data = True):
    weight = data['weight']
    print(f"distancia entre {u} y {v}: {weight} metros")