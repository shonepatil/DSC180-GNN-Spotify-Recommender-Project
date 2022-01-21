from operator import xor
import pandas as pd
import networkx as nx
import torch
import numpy as np
import os
import json
from sklearn.preprocessing import StandardScaler
from dgl.data.utils import save_graphs
from dgl.nn import SAGEConv
import sys
sys.path.insert(0, 'src/model')
import dgl

def encode_onehot(labels):
    classes = set(labels)
    classes_dict = {c: np.identity(len(classes))[i, :] for i, c in
                    enumerate(classes)}
    labels_onehot = np.array(list(map(classes_dict.get, labels)),
                             dtype=np.int32)
    return labels_onehot

def frac_mat_power(m, n):
    evals, evecs = torch.eig (m, eigenvectors = True)  # get eigendecomposition
    evals = evals[:, 0]                                # get real part of (real) eigenvalues
    # rebuild original matrix
    mchk = torch.matmul (evecs, torch.matmul (torch.diag (evals), torch.inverse (evecs)))
    mchk - m                                           # check decomposition
    evpow = evals**(n)                              # raise eigenvalues to fractional power
    # build exponentiated matrix from exponentiated eigenvalues
    mpow = torch.matmul (evecs, torch.matmul (torch.diag (evpow), torch.inverse (evecs)))
    return mpow

def accuracy(output, labels):
    preds = output.max(1)[1].type_as(labels)
    correct = preds.eq(labels).double()
    correct = correct.sum()
    return correct / len(labels)

def load_data(path, dataset, train, val, test, include_ad_hoc_feat=False, include_node2vec=False):
    """Load network dataset"""
    print('Loading {} dataset...'.format(dataset))

    # Construct graph
    G = nx.Graph(name = 'G')
    
    # Load data

    # Choose how many playlists to load in
    n = 10000
    count = 0
    print('Loading {} playlists'.format(n))
    for i in range(999, n, 1000):
        with open(path + 'mpd.slice.{}-{}.json'.format(i - 999, i)) as f:
            data = json.load(f)
            playlists = data['playlists']
            count += create_nodes_edges(G, playlists)

    print('Playlist co-occurences: ' + str(count))

    # See top co-occurence pairs of songs
    # print(sorted(G.edges(data=True),key= lambda x: x[2]['weight'],reverse=True)[:5])

    # See graph info
    print('Graph Info:\n', nx.info(G))
    
    # Get the Adjacency Matrix (A) and Node Features Matrix (X) as numpy array

    # Include Ad-Hoc graph variables

    # Standardize X


    # Dump to CSV

    # # list of name, degree, score 
    # nodes = G.nodes
        
    # # dictionary of lists  
    # dic = {'track_uri': nodes}  
        
    # df = pd.DataFrame(dic)
        
    # # saving the dataframe 
    # df.to_csv('170k_songs.csv') 
    
    return G

# Create graph nodes and edges
def create_nodes_edges(G, playlists):
    count = 0
    for p in playlists:
        tracks = p['tracks']

        # keep track of pairs in current playlist
        seen = set()

        for i in range(len(tracks)): # create nodes
            first = tracks[i]['track_uri'][14:]

            for j in range(i + 1, len(tracks)):
                second = tracks[j]['track_uri'][14:]

                if first != second: # create edges
                    # Ensures co-occurence increased only if edge pair is found in new playlist
                    if not G.has_edge(first, second):
                        G.add_edge(first, second, weight=1)
                        seen.add(frozenset([first, second]))
                    elif frozenset([first, second]) not in seen:
                        G[first][second]['weight'] += 1
                        seen.add(frozenset([first, second]))
                        count += 1

    return count

# nxG = load_data("data/", "Spotify Playlist", 140, 300, 1000, False)
# dglG = dgl.from_networkx(nxG)
# save_graphs("./test_save.bin", dglG)