import networkx as nx
import sys
import matplotlib.pyplot as plt
import random

def createGraph(filename):
    graphFile = open(filename)
    edges = graphFile.read().splitlines()
    vertices = range(int(edges[0].split(' ')[0]))
    edges = map( lambda x: (int(x.split(' ')[0]),int(x.split(' ')[1])) , edges[1:] )
    g = nx.Graph()
    g.add_nodes_from(vertices)
    g.add_edges_from(edges)
    return g

def getSimulationResults(graph,transmit,heal,noOfSim):
    results = list()
    #infectedNodes = set(random.sample(xrange(graph.number_of_nodes()),graph.number_of_nodes()/10))
    infectedNodes = set(random.sample(graph.nodes(),graph.number_of_nodes()/10))
    for simno in xrange(noOfSim):
        healedNodes = set()
        tempInfected = set()
        for infectedNode in infectedNodes:
            for neighborNode in graph.neighbors(infectedNode):
                infectProb = random.random()
                if infectProb<transmit and neighborNode not in healedNodes and neighborNode not in infectedNodes:
                    tempInfected.add(neighborNode)
            healProb = random.random()
            if healProb<heal:
                healedNodes.add(infectedNode)
        infectedNodes = infectedNodes.union(tempInfected)
        infectedNodes = infectedNodes - healedNodes
        results.append( float(len(infectedNodes))/graph.number_of_nodes() )
    return results

def saveFigure(values,transmit,heal):
    fig , ax = plt.subplots(nrows=1,ncols=1)
    ax.plot(range(1,len(values)+1),values)
    fig.savefig('results_plot_transmit('+str(transmit)+')_heal('+str(heal)+').jpg')
    plt.close(fig)


if __name__=='__main__':
    filename = '../virus/static.network'
    transmit = 0.2
    heal = 0.7
    noOfSim = 100

    if len(sys.argv)>1:
        if len(sys.argv)<5:
            print 'Not enough arguments'
            exit()
        filename = str(sys.argv[1])
        transmit = float(sys.argv[2])
        heal = float(sys.argv[3])
        noOfSim = int(sys.argv[4])

    graph = createGraph(filename)
    finalResults = [ 0. for i in xrange(noOfSim) ]
    for i in xrange(10):
        results = getSimulationResults(graph,transmit,heal,noOfSim)
        finalResults = [ finalResults[index] + results[index] for index in xrange(noOfSim)  ]
    finalResults = map(lambda x: x/10,finalResults)
    saveFigure(finalResults,transmit,heal)
    exit()
