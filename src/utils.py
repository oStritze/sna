import pandas as pd
import community as community_louvain # pip install python-louvain
import networkx as nx
from collections import defaultdict
from typing import List
import read_graph
from datetime import datetime, timedelta
from collections import Counter


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
def get_communities(G, min_size=100, random_state=19):
	graph = G.to_undirected()

	# compute the best partition
	partition = community_louvain.best_partition(graph, random_state=random_state)  # source: https://github.com/taynaud/python-louvain

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


def generate_snapshots_over_time(postings, votes, community: List[int], interval: int, unit: str, max_snapshots=None):
	if interval < 1 or unit not in ["h", "d"]:
		raise Exception("Illegal interval or unit values")

	G = read_graph.get_all_users_interactions(postings, votes, multi_di_graph=True, with_timestamp=True)
	G = G.subgraph(community)
	edges = G.edges(data=True)
	created_ats = [attr["created_at"] for (_, _, attr) in edges]
	date = str_to_datetime(min(created_ats))
	max_date = str_to_datetime(max(created_ats))
	Gs = []
	while date <= max_date and (max_snapshots is None or len(Gs) < max_snapshots):
		print(date)
		edges_snapshot = [(a, b) for (a, b, attr) in edges if str_to_datetime(attr["created_at"]) <= date]
		nodes_snapshot = list(sum(edges_snapshot, ()))
		G_snapshot = G.subgraph(nodes_snapshot)
		Gs.append(reduce_multi_graph(G_snapshot))
		if unit == "h":
			date += timedelta(hours=interval)
		elif unit == "d":
			date += timedelta(days=interval)
	return Gs


def reduce_multi_graph(graph: nx.MultiGraph, thresh=0):
	"""
	:return: A non-multi graph from a multi graph, where the number of edges between two nodes is preserved in an edge attribute "weight"
	"""
	width_dict = Counter([tuple(sorted(edge)) for edge in graph.edges()])
	edge_width = [(u, v, value) for ((u, v), value) in width_dict.items()]
	all_int_weighted = pd.DataFrame(edge_width, columns=["user1", "user2", "weight"])
	all_int_weighted_high = all_int_weighted[all_int_weighted.weight >= thresh]
	return nx.from_pandas_edgelist(all_int_weighted_high, source="user1", target="user2", edge_attr=True)


def str_to_datetime(date_str: str):
	return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
