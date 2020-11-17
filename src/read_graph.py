import pandas as pd
import networkx as nx
from collections import Counter
import utils


def get_articles_shared_users(postings=None):
	"""
	:param postings: Custom postings dataframe, if None (default) use all postings.
	:return: An undirected graph with articles as nodes and edges between two articles, if there exists an user
	that commented both articles. The edges have an attributes 'Shared_Users' that count these users commented both articles.
	"""
	if postings is None:
		postings = utils.read_all_postings()

	postings = postings[["ID_CommunityIdentity", "ID_Article"]].drop_duplicates()
	postings2 = postings.copy()
	postings_merged = postings.merge(postings2, on="ID_CommunityIdentity").query("ID_Article_x != ID_Article_y")
	postings_merged = postings_merged.groupby(["ID_Article_x", "ID_Article_y"]).count() \
		.reset_index().rename(columns={"ID_CommunityIdentity": "Shared_Users"})
	return nx.from_pandas_edgelist(postings_merged, source="ID_Article_x", target="ID_Article_y", edge_attr=True)


def get_users_voted_other_users(joined=None, positive_vote=True, multi_di_graph=False):
	"""
	:param joined: Custom dataframe resulted by joining postings and votes, if None (default) join all postings with all votes.
	:param positive_vote: If True (default), consider positve votes between users, otherwise take negative votes.
	:param multi_di_graph: If True, return nx.MultiDiGraph, if False (default) nx.DiGraph.
	:return: A directed graph (or multigraph) with users as nodes and arc from user1 to user2, if user1 voted user2
		positively (negatively).
	"""
	if joined is None:
		postings = utils.read_all_postings()
		votes = utils.read_all_votes()
		joined = postings.merge(votes, on="ID_Posting", suffixes=("_p", "_v"))

	joined = joined[["ID_CommunityIdentity_p", "ID_Posting", "ID_CommunityIdentity_v", "VoteNegative", "VotePositive"]] \
		.query("{} == 1".format("VotePositive" if positive_vote else "VoteNegative"))
	if multi_di_graph:
		return nx.from_pandas_edgelist(joined, source="ID_CommunityIdentity_v", target="ID_CommunityIdentity_p", create_using=nx.MultiDiGraph)
	else:
		return nx.from_pandas_edgelist(joined, source="ID_CommunityIdentity_v", target="ID_CommunityIdentity_p", create_using=nx.DiGraph)


def get_users_commented_other_users(postings=None, multi_di_graph=False):
	"""
	:param postings: Custom postings dataframe, if None (default) use all postings.
	:param multi_di_graph: If True, return nx.MultiDiGraph, if False (default) nx.DiGraph.
	:return: A directed graph (or multigraph) with users as nodes and arc from user1 to user2, if user1 commented user2.
	"""
	if postings is None:
		postings = utils.read_all_postings()

	parent_postings = postings.query("ID_Posting_Parent == 'NaN'")
	child_postings = postings.query("ID_Posting_Parent != 'NaN'")
	postings_joined = parent_postings.merge(child_postings, left_on="ID_Posting", right_on="ID_Posting_Parent", suffixes=("_parent", "_child"))
	if multi_di_graph:
		return nx.from_pandas_edgelist(postings_joined, source="ID_CommunityIdentity_child", target="ID_CommunityIdentity_parent", create_using=nx.MultiDiGraph)
	else:
		return nx.from_pandas_edgelist(postings_joined, source="ID_CommunityIdentity_child", target="ID_CommunityIdentity_parent", create_using=nx.DiGraph)


def get_all_users_interactions(postings=None, votes=None, multi_di_graph=False):
	"""
	:param postings: Custom postings dataframe, if None (default) use all postings.
	:param votes: Custom votes dataframe, if None (default) use all votes.
	:param multi_di_graph: If True, return nx.MultiDiGraph, if False (default) nx.DiGraph.
	:return: A directed graph (or multigraph) with users as nodes and arc from user1 to user2, if user1 interacted with user2,
		i.e. voted positively, negatively, or did a comment.
	"""
	if postings is None or votes is None:
		postings = utils.read_all_postings()
		votes = utils.read_all_votes()

	joined = postings.merge(votes, on="ID_Posting", suffixes=("_p", "_v"))
	positives = get_users_voted_other_users(joined, positive_vote=True, multi_di_graph=multi_di_graph)
	negatives = get_users_voted_other_users(joined, positive_vote=False, multi_di_graph=multi_di_graph)
	comments = get_users_commented_other_users(postings, multi_di_graph=multi_di_graph)
	return nx.disjoint_union_all([positives, negatives, comments])


def get_weighted_interaction_graph(postings, votes, thresh=0):
	G = get_all_users_interactions(postings, votes, multi_di_graph=True)
	width_dict = Counter(G.edges())
	edge_width = [(u, v, value) for ((u, v), value) in width_dict.items()]
	all_int_weighted = pd.DataFrame(edge_width)
	all_int_weighted.columns = ["user1", "user2", "weight"]
	all_int_weighted_high = all_int_weighted[all_int_weighted.weight >= thresh]
	return nx.from_pandas_edgelist(all_int_weighted_high, source="user1", target="user2", edge_attr=True)