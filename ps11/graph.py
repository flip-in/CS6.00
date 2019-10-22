# 6.00 Problem Set 11
#
# graph.py
#
# A set of data structures to represent graphs
#

class Node(object):
   def __init__(self, name):
       self.name = str(name)
   def getName(self):
       return self.name
   def __str__(self):
       return self.name
   def __repr__(self):
      return self.name
   def __eq__(self, other):
       return self.name == other.name
   def __ne__(self, other):
      return not self.__eq__(other)

class Edge(object):
   def __init__(self, src, dest):
       self.src = src
       self.dest = dest
   def getSource(self):
       return self.src
   def getDestination(self):
       return self.dest
   def __str__(self):
       return str(self.src) + '->' + str(self.dest)

class WeightedEdge(Edge):
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight
    def getWeight(self):
        return self.weight
    def __str__(self):
        return str(self.src) + '->' + str(self.dest) + ' dist: ' + str(self.weight[0]) + ', ' + str(self.weight[1])

class Digraph(object):
   """
   A directed graph
   """
   def __init__(self):
       self.nodes = set([])
       self.edges = {}
   def addNode(self, node):
       if node in self.nodes:
           raise ValueError('Duplicate node')
       else:
           self.nodes.add(node)
           self.edges[node] = []
   def addEdge(self, edge):
       src = edge.getSource()
       dest = edge.getDestination()
       if not(src in self.nodes and dest in self.nodes):
           raise ValueError('Node not in graph')
       self.edges[src].append(dest)
#       self.edges[src] = dest
   def childrenOf(self, node):
       return self.edges[node]
   def hasNode(self, node):
       return node in self.nodes
   def getNode(self, node_name):
       for node in self.nodes:
           if str(node) == node_name:
               return node
   def __str__(self):
       res = ''
       for k in self.edges:
           for d in self.edges[k]:
               res = res + str(k) + '->' + str(d) + '\n'
       return res[:-1]

class WeightedDigraph(Digraph):
    def __init__(self):
        self.nodes = set([])
        self.edges = {}
        self.weights = {}
    def addWeightedEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        weight = edge.getWeight()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.weights[(src, dest)] = weight
    
    def getWeight(self, src, dest):
        return self.weights[src,dest]
    
    def __str__(self):
        res = ''
        for d in self.weights:
            res = res + str(d[0]) + '->' + str(d[1]) + ' ' + 'tot_dist: ' + str(self.weights[d][0]) +  '||' + 'out_dist: ' +  str(self.weights[d][1]) + '\n'            
        return res[:-1] 

#test_map = [['a', 'b', 2, 1], ['b','c', 3,2], ['b','d', 4,2], ['d','e', 2,1]]
#
#test_weightedGraph = WeightedDigraph()
#
#test_nodes = []
#
#test_nodes.append(Node('a'))
#test_nodes.append(Node('b'))
#test_nodes.append(Node('c'))
#test_nodes.append(Node('d'))
#test_nodes.append(Node('e'))
#
#for test_node in test_nodes:
#    test_weightedGraph.addNode(test_node)
#    
#test_weightedGraph.addEdge(Edge(test_nodes[0], test_nodes[1]))
#test_weightedGraph.addEdge(Edge(test_nodes[1], test_nodes[2]))
#test_weightedGraph.addEdge(Edge(test_nodes[1], test_nodes[3]))
#test_weightedGraph.addEdge(Edge(test_nodes[3], test_nodes[4]))
#
#test_weightedGraph.addWeightedEdge(WeightedEdge(test_nodes[0], test_nodes[1], (test_map[0][2], test_map[0][3])))
#test_weightedGraph.addWeightedEdge(WeightedEdge(test_nodes[1], test_nodes[2], (test_map[1][2], test_map[1][3])))
#test_weightedGraph.addWeightedEdge(WeightedEdge(test_nodes[1], test_nodes[3], (test_map[2][2], test_map[2][3])))
#test_weightedGraph.addWeightedEdge(WeightedEdge(test_nodes[3], test_nodes[4], (test_map[3][2], test_map[3][3])))
#
#print test_weightedGraph