import networkx as nx

from networkx.algorithms.traversal.path import single_source_shortest_path
from oldowan.polymorphism import Polymorphism
from oldowan.polymorphism import InfiniteRange
from oldowan.mtdna import rCRSlist

def transition(position):
    ts_dict = {'A':'G', 'G':'A', 'C':'T', 'T':'C'}
    return ts_dict[rCRSlist[position]]
    

def read_network_csv(f):
    edges = {}
    G = nx.Graph()
    G.node_labels = {}
    G.node_labels[0] = 'CRS'
    G.edge_labels = {}
    
    for line in open(f, 'rU'):
        if line.startswith('#'):
            continue
        line = line.strip()
        if line == '':
            continue
        lineitems = list(x.strip() for x in line.split(','))
        if len(lineitems) != 5:
            raise Exception, 'format wrong on line "%s"' % line
        target = int(lineitems[0])
        source = int(lineitems[1])
        target_label = lineitems[2]
        position = None
        if lineitems[3] != '':
            position = int(lineitems[3])
        nucleotide = lineitems[4] 
        if lineitems[4] == '' and position is not None:
            nucleotide = transition(position)
            
        if not G.node_labels.has_key(target):
            G.node_labels[target] = target_label
        
        key = (target, source)
        poly = None
        if position is not None:
            poly = Polymorphism(position, 0, nucleotide, rCRSlist[position])
        if G.edge_labels.has_key(key):
            G.edge_labels[key].append(poly)
        else:
            G.edge_labels[key] = [poly]
            
    for ek in G.edge_labels.keys():
        G.add_edge(ek[0], ek[1])
    return G
    

def write_dot(G, path):
    # requires graphviz, pygraphviz, pydot
    g = nx.to_pydot(G)
    for n in g.get_nodes():
        n.set_label(G.node_labels[int(n.get_name())])
    for e in g.get_edges():
        key = (int(e.get_destination()), int(e.get_source()))
        s = '\\n'.join(list(str(x) for x in G.edge_labels[key]))
        e.set_label(s)
    g.write_dot(path)
    

def network_haplotypes(G, source=0):
    paths = single_source_shortest_path(G, source)
    haplotypes = {}
    for end in paths.keys():
        if source == end:
            continue
        polys = []
        for edge in zip(paths[end][1:], paths[end]):
            polys = polys + G.edge_labels[edge]
        polys = list(x for x in polys if x is not None)
        polys.sort()
        haplotypes[end] = polys
    return haplotypes


def network_match(G, H, query, polyrange=InfiniteRange()):
    reduced_query = list(x for x in query if x in polyrange)
    reduced_H = {}
    for node, hap in H.iteritems():
        reduced_H[node] = list(x for x in hap if x in polyrange)
    for poly in reduced_query:
        for node, hap in reduced_hap.iteritems():
            pass # evaluate match


def has_duplicates(l):
    return len(l) == len({}.fromkeys(l).keys())

