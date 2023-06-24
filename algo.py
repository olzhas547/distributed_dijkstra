import math
from queue import PriorityQueue
import random
import threading

import pandas as pd

def distributed_dijkstra(graph: dict, start: str, goal: str) -> (dict, float):
    '''
    

    Parameters
    ----------
    graph : dict
        DESCRIPTION. Graph on which we use Dijkstra's algorithm.
    start : str
        DESCRIPTION. Starting point.
    goal : str
        DESCRIPTION. Ending point.

    Returns
    -------
    parent : dict
        DESCRIPTION. Reversed trace of Dijkstra's algorithm.
    weights[goal] : float
        DESCRIPTION. Distance between start and goal.

    '''
    visited = set()
    weights = {start: 0}
    parent = {start: None}
    queue = PriorityQueue()

    queue.put((0, start))
    while queue:
        while not queue.empty():
            _, vertex = queue.get()
            if vertex not in visited:
                break
        else:
            break
        visited.add(vertex)
        if vertex == goal:
            break
        
        def worker():
            nonlocal visited, vertex, weights, queue
            for neighbor, distance in graph[vertex]:
                if neighbor in visited:
                    continue
                old_weight = weights.get(neighbor, float('inf'))
                new_weight = weights[vertex] + distance
                if new_weight < old_weight:
                    queue.put((new_weight, neighbor))
                    weights[neighbor] = new_weight
                    parent[neighbor] = vertex
        threads = [
            threading.Thread(target=worker) for _ in range(4)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    return parent, weights[goal]

def init_weights(updates: str | None = None) -> (dict, str):
    '''
    Read map from excel and generate traffic jams and road closure.

    Parameters.
    ----------
    updates : str | None, optional
        DESCRIPTION. The default is None.
        Seed of traffic jams and road closures.

    Returns
    -------
    graph_dict : dict
        DESCRIPTION. Graph in dictionary representation.
    updates : str
        DESCRIPTION. Seed of traffic jams and road closures.

    '''
    graph = pd.read_excel('./graph.xlsx')
    
    # Generate seed
    # 0: road is closed
    # 1: big traffic jam
    # 2: low traffic jam
    # 3: default traffic jam
    if not updates:
        updates = ''.join([str(round(3*random.random())) for i in range(100)])
    names = graph[0].to_list()
    for i, column in enumerate(names):
        for j, row in enumerate(names):
            match float(updates[10*i+j]):
                case 0 if graph.at[i, row] != 0:
                    graph.at[i, row] = math.inf
                case 1:
                    graph.at[i, row] = graph.at[i, row] * 4
                case 2:
                    graph.at[i, row] = graph.at[i, row] * 2
                case 3:
                    graph.at[i, row] = graph.at[i, row] * 1.5
    
    graph_dict = {}
    for node in names:
        res = pd.Series(graph[node].values,index=graph[0]).to_dict()
        result = {(i, res[i]*1.0) for i in res if res[i] != math.inf}
        graph_dict[node] = result
    return graph_dict, updates

def path(parent: dict, goal: str) -> list:
    '''
    

    Parameters
    ----------
    parent : dict
        DESCRIPTION. Reversed trace of Dijkstra's algorithm.
    goal : str
        DESCRIPTION. Ending point of path.

    Returns
    -------
    path[::-1] : list
        DESCRIPTION. Shortest path.

    '''
    if goal not in parent:
        return None
    vertex = goal
    path = []
    while vertex is not None:
        path.append(vertex)
        vertex = parent[vertex]
    return path[::-1]