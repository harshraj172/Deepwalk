# -*- coding: utf-8 -*-
"""Deepwalk.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IsehyRWKpn_DCEG0VvViL_UMaZDOJIWJ

#Importing the necessary libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import networkx as nx # for making graph matrix 
import pandas as pd
import numpy as np
import random
from tqdm import tqdm
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
# %matplotlib inline

"""#Constructing the graph"""

G = nx.from_pandas_edgelist(df, "source", "target", edge_attr=True, create_using=nx.Graph())

"""#Random walk:
- A function that will take a node and length of the path to be traversed as inputs. 
- It will walk through the connected nodes from the specified input node in a random fashion. Finally, it will return the sequence of traversed nodes:


"""

def get_randomwalk(node, path_length):
    
    random_walk = [node] # initializing the random walk with the starting node itself
    
    for i in range(path_length-1):
        temp = list(G.neighbors(node)) # a list containing neighboring nodes
        temp = list(set(temp) - set(random_walk)) # discarding the values already traversed
        if len(temp) == 0: # if there is no new node then break
            break

        random_node = random.choice(temp)
        random_walk.append(random_node)
        node = random_node # updating the node with the newly added random_node
        
    return random_walk

"""# Calling the random walk function on every node of the graph"""

# get list of all nodes from the graph
all_nodes = list(G.nodes())

random_walks = []
for n in tqdm(all_nodes):
    for i in range(5): # producing sequence from a particular node 5 times(gamma)
        random_walks.append(get_randomwalk(n,10))
        
# count of sequences produced
len(random_walks)

"""# Using Skip Gram method to get the node embedding
- Use these sequences as inputs to a skip-gram model 
- Extract the weight learned by the model (which are nothing but the node embeddings).
"""

from gensim.models import Word2Vec

# Clearing the warnings
import warnings
warnings.filterwarnings('ignore')

"""# Train skip-gram (word2vec) model"""

model = Word2Vec(window = 4, sg = 1, hs = 0,
                 negative = 10, # for negative sampling
                 alpha=0.03, min_alpha=0.0007,
                 seed = 14)

model.build_vocab(random_walks, progress_per=2)

model.train(random_walks, total_examples = model.corpus_count, epochs=20, report_delay=1)

"""# Visualization the nodes"""

