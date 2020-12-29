import networkx as nx
import pandas as pd
import community as community_louvain # pip install python-louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict


def read_all_postings():
	postings = pd.read_csv("../data/raw/Postings_01052019_15052019.csv", delimiter=";")
	return pd.concat([postings, pd.read_csv("../data/raw/Postings_16052019_31052019.csv", delimiter=";")])


def read_all_votes():
	votes = pd.read_csv("../data/raw/Votes_01052019_15052019.csv", delimiter=";")
	return pd.concat([votes, pd.read_csv("../data/raw/Votes_16052019_31052019.csv", delimiter=";")])


def get_in_degrees(G: nx.DiGraph):
	return {n: G.in_degree(n) for n in G.nodes()}


def get_out_degrees(G: nx.DiGraph):
	return {n: G.out_degree(n) for n in G.nodes()}


def get_distinct_cliques(G: nx.Graph, n=None):
	if G.is_directed():
		G = G.to_undirected()

	cliques = sorted(list(nx.find_cliques(G)), key=lambda c: len(c), reverse=True)
	nodes = set()
	distinct_cliques = []
	for c in cliques:
		if n is not None and len(distinct_cliques) >= n:
			break
		if len(nodes.intersection(set(c))) == 0:
			nodes = nodes.union(set(c))
			distinct_cliques.append(c)
	return distinct_cliques


# Get communities from a graph based on modularity maximization
# G .. weighted Graph
# min_size .. ignore communities below minimum size (as modularity maximization does not work for small communities)
# returns list of communities where each community is a list of node IDs, sorted by size of community (descending)
def get_communities(G, min_size=100):
	graph = G.to_undirected()

	# compute the best partition
	partition = community_louvain.best_partition(graph)  # source: https://github.com/taynaud/python-louvain

	# extract communities as lists of node IDs with community ID as key
	all_communities = defaultdict(list)
	for key, value in sorted(partition.items()):
		all_communities[value].append(key)

	# drop small communities < min_size (modularity maximization does not correctly identify small communities)
	communities = []
	for val in all_communities.values():
		if len(val) >= min_size:
			communities.append(val)

	# sort by community size in descending order
	communities.sort(key=len, reverse=True)

	return communities
