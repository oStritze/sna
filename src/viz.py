import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict


def plot_graph(G: nx.Graph, figsize=(20, 20), with_labels=True, arrows=True):
	plt.figure(figsize=figsize)
	nx.draw(G, with_labels=with_labels, arrows=arrows)
	plt.show()


def plot_colored_graph(G: nx.Graph, node_color_attr=None, edge_color_attr=None, edge_width_factor=None, pos=None, figsize=(20, 20),
					   node_cmap=plt.cm.plasma, edge_cmap=plt.cm.viridis, node_ticks=None, edge_ticks=None, node_size=300, ax=None):
	node_colors = None if node_color_attr is None else [G.nodes()[n][node_color_attr] for n in G.nodes()]
	edge_colors = None if edge_color_attr is None else [G.edges()[e][edge_color_attr] for e in G.edges()]
	edge_widths = 1 if edge_width_factor is None else [c / max(edge_colors) * edge_width_factor for c in edge_colors]

	if ax is None:
		plt.figure(figsize=figsize)
	if pos is None:
		pos = nx.spring_layout(G, seed=7)
	ec = nx.draw_networkx_edges(G, pos, edge_color=edge_colors, edge_cmap=edge_cmap, width=edge_widths, ax=ax)
	nc = nx.draw_networkx_nodes(G, pos, node_color=node_colors, cmap=node_cmap, node_size=node_size, ax=ax)

	if node_color_attr is not None:
		if node_ticks is None:
			plt.colorbar(nc, label=node_color_attr, ax=ax)
		else:
			cbar = plt.colorbar(nc, label=node_color_attr, ticks=range(len(node_ticks)), ax=ax)
			cbar.ax.set_yticklabels(node_ticks)
	if edge_color_attr is not None:
		if edge_ticks is None:
			plt.colorbar(ec, label=edge_color_attr, ax=ax)
		else:
			cbar = plt.colorbar(ec, label=edge_color_attr, ticks=range(len(edge_ticks)), ax=ax)
			cbar.ax.set_yticklabels(edge_ticks)

	if ax is None:
		plt.axis('off')
		plt.show()


def compare_snapshots(snapshots_list: List[Dict], ranges: List[range], figsize=(25, 15)):
	date_indices = sum([list(r) for r in ranges], [])
	range_ids = sum([[i] * len(r) for (i, r) in enumerate(ranges)], [])

	dates = sorted(snapshots_list[0].keys())
	dates = [dates[i] for i in date_indices]

	nrows, ncols = len(snapshots_list), len(dates)
	fig, ax = plt.subplots(nrows=nrows, ncols=ncols, sharey=True, figsize=figsize)
	for i, ax_i in enumerate(ax):
		for j, ax_j in enumerate(ax_i):
			snapshots = snapshots_list[i]
			date = dates[j]
			G = snapshots[date]
			plot_colored_graph(G, edge_color_attr="weight", edge_width_factor=10, node_size=20,
							   pos=nx.circular_layout(G), ax=ax_j)
			range_id = range_ids[j]
			ax_j.set_title(date, {"color": "black" if range_id % 2 == 0 else "red"})
