import networkx as nx
import sys
import matplotlib.pyplot as plt
import random
import numpy as np
from numpy import linalg as LA

def createGraph(filename):
    graphFile = open(filename)
    edges = graphFile.read().splitlines()
    vertices = range(int(edges[0].split(' ')[0]))
    edges = map( lambda x: (int(x.split(' ')[0]),int(x.split(' ')[1])) , edges[1:] )
    g = nx.Graph()
    g.add_nodes_from(vertices)
    g.add_edges_from(edges)
    return g

graph = createGraph("static.network")

print("graph created")
print(nx.number_of_nodes(graph))

def immunize_k_random(graph, k):
    nodes = nx.number_of_nodes(graph)
    rand_nodes = random.sample(range(0, nodes), k)
    new_graph = graph.copy()
    print(new_graph.number_of_nodes())
    new_graph.remove_nodes_from(rand_nodes)
    print(new_graph.number_of_nodes())
    
    return new_graph

def immunize_k_highest_degree(graph, k):
    degrees = graph.degree()
    sorted_degrees = sorted(degrees, key=degrees.get)
    highest_degrees = sorted_degrees[-k:]
    new_graph = graph.copy()
    print(new_graph.number_of_nodes())
    new_graph.remove_nodes_from(highest_degrees)
    print(new_graph.number_of_nodes())
    
    return new_graph

def immunize_k(graph, k):
    degrees = graph.degree()
    sorted_degrees = sorted(degrees, key=degrees.get)
    highest_degrees = sorted_degrees[-k:]
    new_graph = graph.copy()
    print(new_graph.number_of_nodes())
    
    for vertex in reversed(highest_degrees):
        new_graph.remove_node(vertex)
        degrees = new_graph.degree()
        sorted_degrees = sorted(degrees, key=degrees.get)
        highest_degrees = sorted_degrees[-k:]
    
    print(new_graph.number_of_nodes())
    
    return new_graph

def immunize_k_eigenvalues(graph, k):
    print("in function")
    A = nx.adjacency_matrix(graph).todense()
    w, v = LA.eig(A)
    lrgst_ev_index = np.argmax(w)
    print(lrgst_ev_index)
    largest_vector = v[:,lrgst_ev_index]
    print(largest_vector)
    nodes = np.argsort(largest_vector)
    nodes = nodes[-k:]
    
    new_graph = graph.copy()
    print(new_graph.number_of_nodes())
    new_graph.remove_nodes_from(nodes)
    print(new_graph.number_of_nodes())
    
    print("done")
    return new_graph

def get_strength(lambda1, beta, delta):
    return lambda1*(beta/delta)

immunized_graph = immunize_k_random(graph, 200)
eg_val = nx.adjacency_spectrum(immunized_graph)
lambda1 = max(eg_val)
print("hi")
print("Strength is: "+str(get_strength(lambda1,0.2,0.7)))

#immunized_graph = immunize_k_highest_degree(graph, 200)   
#immunized_graph = immunize_k(graph, 200)   
#immunize_k_eigenvalues(graph, 200)
