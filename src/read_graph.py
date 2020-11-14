import pandas as pd
import networkx as nx

def get_users_commented_same_article(postings=None):
	if postings is None:
		postings = read_all_postings()

	postings = postings[["ID_CommunityIdentity", "ID_Article"]].drop_duplicates()
	postings2 = postings.copy()
	postings_merged = postings.merge(postings2, on="ID_Article").query("ID_CommunityIdentity_x != ID_CommunityIdentity_y")
	return nx.from_pandas_edgelist(postings_merged, source="ID_CommunityIdentity_x", target="ID_CommunityIdentity_y")

def get_users_voted_other_users(joined=None, positive_vote=True):
	if joined is None:
		postings = read_all_postings()
		votes = read_all_votes()
		joined = postings.merge(votes, on="ID_Posting")

	joined = joined[["ID_CommunityIdentity_v", "ID_Posting", "VoteNegative", "VotePositive", "ID_CommunityIdentity"]] \
		.query("VotePositive == {}".format(1 if positive_vote else 0))
	return nx.from_pandas_edgelist(joined, source="ID_CommunityIdentity_v", target="ID_CommunityIdentity", create_using=nx.DiGraph)

def get_users_commented_other_users(postings=None):
	if postings is None:
		postings = read_all_postings()

	parent_postings = postings.query("ID_Posting_Parent == 'NaN'")
	child_postings = postings.query("ID_Posting_Parent != 'NaN'")
	postings_joined = parent_postings.merge(child_postings, left_on="ID_Posting", right_on="ID_Posting_Parent", suffixes=("_parent", "_child"))
	return nx.from_pandas_edgelist(postings_joined, source="ID_CommunityIdentity_child", target="ID_CommunityIdentity_parent", create_using=nx.DiGraph)

def read_all_postings():
	postings = pd.read_csv("../data/raw/Postings_01052019_15052019.csv", delimiter=";")
	return pd.concat([postings, pd.read_csv("../data/raw/Postings_16052019_31052019.csv", delimiter=";")])

def read_all_votes():
	votes = pd.read_csv("../data/raw/Votes_01052019_15052019.csv", delimiter=";")
	return pd.concat([votes, pd.read_csv("../data/raw/Votes_16052019_31052019.csv", delimiter=";")])

