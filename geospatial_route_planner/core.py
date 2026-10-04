"""Deterministic Dijkstra routing over validated directed weighted graphs."""

import heapq, math


def validate(spec):
    if not isinstance(spec, dict):
        raise ValueError("Network must be an object")
    nodes = spec.get("nodes")
    edges = spec.get("edges")
    if (
        not isinstance(nodes, list)
        or not nodes
        or any(not isinstance(n, str) or not n or ":" in n for n in nodes)
        or len(nodes) != len(set(nodes))
    ):
        raise ValueError("Nodes must be unique nonempty strings without colons")
    if not isinstance(edges, list):
        raise ValueError("Edges must be an array")
    graph = {node: [] for node in nodes}
    seen = set()
    for edge in edges:
        if not isinstance(edge, dict):
            raise ValueError("Edge must be an object")
        start, end, cost = edge.get("from"), edge.get("to"), edge.get("cost")
        if start not in graph or end not in graph:
            raise ValueError("Edge refers to unknown node")
        if (
            isinstance(cost, bool)
            or not isinstance(cost, (int, float))
            or not math.isfinite(cost)
            or cost < 0
        ):
            raise ValueError("Edge cost must be finite and nonnegative")
        if (start, end) in seen:
            raise ValueError("Duplicate directed edge")
        seen.add((start, end))
        graph[start].append((end, cost))
    for values in graph.values():
        values.sort()
    return graph


def route(spec, start, end, blocked=()):
    graph = validate(spec)
    if start not in graph or end not in graph:
        raise ValueError("Start and destination must be known nodes")
    blocked = set(blocked)
    for item in blocked:
        if not isinstance(item, str) or item.count(":") != 1:
            raise ValueError("Blocked links use from:to syntax")
        left, right = item.split(":")
        if (
            left not in graph
            or right not in graph
            or not any(node == right for node, _ in graph[left])
        ):
            raise ValueError("Blocked link does not exist")
    # Lexicographic path ordering resolves ties reproducibly.
    queue = [(0, (start,), start)]
    best = {start: (0, (start,))}
    settled = set()
    while queue:
        cost, path, current = heapq.heappop(queue)
        if current in settled:
            continue
        settled.add(current)
        if current == end:
            return {
                "reachable": True,
                "path": list(path),
                "cost": cost,
                "visited_nodes": len(settled),
            }
        for node, weight in graph[current]:
            if current + ":" + node in blocked or node in settled:
                continue
            candidate = (cost + weight, path + (node,))
            if not math.isfinite(candidate[0]):
                raise ValueError("Accumulated route cost exceeds numeric range")
            if node not in best or candidate < best[node]:
                best[node] = candidate
                heapq.heappush(queue, (candidate[0], candidate[1], node))
    return {"reachable": False, "path": [], "cost": None, "visited_nodes": len(settled)}


def route_via(spec, start, end, via=(), blocked=()):
    stops = [start, *via, end]
    path = []
    cost = 0
    visited = 0
    for left, right in zip(stops, stops[1:]):
        result = route(spec, left, right, blocked)
        if not result["reachable"]:
            return {
                "reachable": False,
                "path": [],
                "cost": None,
                "failed_segment": [left, right],
                "stops": stops,
            }
        path.extend(result["path"] if not path else result["path"][1:])
        cost += result["cost"]
        visited += result["visited_nodes"]
        if not math.isfinite(cost):
            raise ValueError("Accumulated route cost exceeds numeric range")
    return {
        "reachable": True,
        "path": path,
        "cost": cost,
        "visited_nodes": visited,
        "stops": stops,
    }
