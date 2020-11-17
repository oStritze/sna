import networkx as nx
import pandas as pd


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
