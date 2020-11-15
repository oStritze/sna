import networkx as nx
import matplotlib.pyplot as plt


def plot_graph(G: nx.Graph, figsize=(20, 20), with_labels=True, arrows=True):
	plt.figure(figsize=figsize)
	nx.draw(G, with_labels=with_labels, arrows=arrows)
	plt.show()


def plot_colored_graph(G: nx.Graph, node_color_attr=None, edge_color_attr=None, edge_width_factor=None, pos=None, figsize=(20, 20),
					   node_cmap=plt.cm.plasma, edge_cmap=plt.cm.viridis, node_ticks=None, edge_ticks=None):
	node_colors = None if node_color_attr is None else [G.nodes()[n][node_color_attr] for n in G.nodes()]
	edge_colors = None if edge_color_attr is None else [G.edges()[e][edge_color_attr] for e in G.edges()]
	edge_widths = 1 if edge_width_factor is None else [c / max(edge_colors) * edge_width_factor for c in edge_colors]

	plt.figure(figsize=figsize)
	if pos is None:
		pos = nx.spring_layout(G, seed=7)
	ec = nx.draw_networkx_edges(G, pos, edge_color=edge_colors, edge_cmap=edge_cmap, width=edge_widths)
	nc = nx.draw_networkx_nodes(G, pos, node_color=node_colors, cmap=node_cmap)

	if node_color_attr is not None:
		if node_ticks is None:
			plt.colorbar(nc, label=node_color_attr)
		else:
			cbar = plt.colorbar(nc, label=node_color_attr, ticks=range(len(node_ticks)))
			cbar.ax.set_yticklabels(node_ticks)
	if edge_color_attr is not None:
		if edge_ticks is None:
			plt.colorbar(ec, label=edge_color_attr)
		else:
			cbar = plt.colorbar(ec, label=edge_color_attr, ticks=range(len(edge_ticks)))
			cbar.ax.set_yticklabels(edge_ticks)

	plt.axis('off')
	plt.show()
