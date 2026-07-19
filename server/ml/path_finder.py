"""
Builds an `ml.graph_algorithms.Graph` from a list of road/waypoint segments
and exposes a single find_path() call used by safest_route.py.
"""
from typing import Dict, Hashable, List, Tuple

from ml.graph_algorithms import Graph
from ml.dijkstra import dijkstra


def build_graph(segments: List[Tuple[Hashable, Hashable, float]]) -> Graph:
    """segments: list of (node_a, node_b, distance_km)."""
    graph = Graph()
    for a, b, dist in segments:
        graph.add_edge(a, b, dist)
    return graph


def find_path(segments: List[Tuple[Hashable, Hashable, float]], start: Hashable, goal: Hashable):
    graph = build_graph(segments)
    return dijkstra(graph, start, goal)
