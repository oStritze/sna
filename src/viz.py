import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

def plot_graph(G: nx.Graph, figsize=(20, 20), with_labels=True, arrows=True):
	plt.figure(figsize=figsize)
	nx.draw(G, with_labels=with_labels, arrows=arrows)
	plt.show()

def plot_colored_graph(G: nx.Graph, color_attr: str, figsize=(20, 20), cmap="viridis"):
	colors = [G.nodes()[n][color_attr] for n in G.nodes()]
	plt.figure(figsize=figsize)
	pos = nx.spring_layout(G)
	ec = nx.draw_networkx_edges(G, pos, alpha=0.5)
	nc = nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=100, cmap=cmap)
	plt.colorbar(nc)
	plt.axis('off')
	plt.show()
