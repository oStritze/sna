import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict
import utils
import pandas as pd


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


def compare_snapshots(snapshots_list: List[Dict], ranges: List[range], figsize=(25, 15), include_final=False):
	"""
	:param snapshots_list: list of dictionaries. Each dict consists of a date key and a graph value
	:param ranges: list of range objects. Each range specifies indices of the sorted date keyset, e.g. [range(2, 4), range(9, 12)]
		compares the snapshots of the 2nd to 3rd and 9th to 11th date.
	:param include_final: If True, the snapshot of the latest date is plotted (Default False)
	"""
	date_indices = sum([list(r) for r in ranges], [])
	range_ids = sum([[i] * len(r) for (i, r) in enumerate(ranges)], [])

	dates = sorted(snapshots_list[0].keys())
	selected_dates = [dates[i] for i in date_indices]
	if include_final:
		selected_dates.append(dates[-1])
		range_ids.append(max(range_ids) + 1)

	nrows, ncols = len(snapshots_list), len(selected_dates)
	fig, ax = plt.subplots(nrows=nrows, ncols=ncols, sharey=True, figsize=figsize)
	for i, ax_i in enumerate(ax):
		for j, ax_j in enumerate(ax_i):
			snapshots = snapshots_list[i]
			date = selected_dates[j]
			G = snapshots[date]
			plot_colored_graph(G, edge_color_attr="weight", edge_width_factor=10, node_size=20,
							   pos=nx.circular_layout(G), ax=ax_j)
			range_id = range_ids[j]
			ax_j.set_title(date, {"color": "black" if range_id % 2 == 0 else "red"})


def compare_snapshot_weights(snapshots_list: List[Dict], figsize=(10, 5)):
	weights = []
	for i, snapshots in enumerate(snapshots_list):
		for date in snapshots:
			G = snapshots[date]
			weights.append({"community": i, "snapshot": date, "weight": utils.get_weight_sum(G)})
	weights = pd.DataFrame(weights).set_index("community")

	fig = plt.figure(figsize=figsize)
	for community in weights.index.unique():
		data = weights.loc[community]
		plt.plot(data["snapshot"], data["weight"], label=community)

	plt.title("Community Development")
	plt.xlabel("Time")
	plt.ylabel("Interactions inside community")
	plt.legend()
	plt.show()
