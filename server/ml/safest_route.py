"""
Combines path_finder (Dijkstra over a waypoint graph) with hazard-avoidance
weighting: edges near active disaster reports get an inflated cost so the
shortest-*safe*-path naturally routes around them.
"""
from typing import Hashable, List, Tuple

from ml.graph_algorithms import Graph
from ml.dijkstra import dijkstra
from utils.location import haversine_km

HAZARD_PENALTY_RADIUS_KM = 3.0
HAZARD_PENALTY_MULTIPLIER = 5.0


def _edge_hazard_penalty(a: Tuple[float, float], b: Tuple[float, float], hazards: List[Tuple[float, float]]) -> float:
    midpoint = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    for hazard_lat, hazard_lng in hazards:
        if haversine_km(midpoint[0], midpoint[1], hazard_lat, hazard_lng) <= HAZARD_PENALTY_RADIUS_KM:
            return HAZARD_PENALTY_MULTIPLIER
    return 1.0


def build_hazard_aware_graph(
    segments: List[Tuple[Tuple[float, float], Tuple[float, float], float]],
    hazards: List[Tuple[float, float]],
) -> Graph:
    graph = Graph()
    for a, b, dist in segments:
        penalty = _edge_hazard_penalty(a, b, hazards)
        graph.add_edge(a, b, dist * penalty)
    return graph


def find_safest_route(
    segments: List[Tuple[Tuple[float, float], Tuple[float, float], float]],
    hazards: List[Tuple[float, float]],
    start: Hashable,
    goal: Hashable,
):
    graph = build_hazard_aware_graph(segments, hazards)
    return dijkstra(graph, start, goal)
