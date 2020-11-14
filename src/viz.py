import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

def plot_graph(G: nx.Graph, figsize=(20, 20), with_labels=True, arrows=True):
	plt.figure(figsize=figsize)
	nx.draw(G, with_labels=with_labels, arrows=arrows)
	plt.show()