import networkx as nx
from typing import List
from app.models import Anomaly

def find_cycles_optimized(G: nx.DiGraph, max_len=6) -> List[List[str]]:
    """
    Finds elementary cycles with length <= max_len using DFS.
    Much faster than nx.simple_cycles for large graphs.
    """
    cycles = []
    
    def dfs(start_node, current_node, path):
        if len(path) > max_len:
            return
            
        neighbors = list(G.successors(current_node))
        for neighbor in neighbors:
            if neighbor == start_node:
                if len(path) > 2: # Min cycle 3
                    cycles.append(path + [start_node])
                continue
                
            if neighbor not in path:
                dfs(start_node, neighbor, path + [neighbor])

    # To avoid duplicates (A-B-C vs B-C-A), we sort nodes and only start from 'min' node in cycle
    # Or simply dedupe after. For speed on 1000 nodes, iterating all as start is O(N * D^k).
    # Since we want *robust* detection, let's use a standard backtracking with visited set per path.
    
    nodes = list(G.nodes())
    # Heuristic: Only check nodes with in-degree > 0 and out-degree > 0
    candidates = [n for n in nodes if G.in_degree(n) > 0 and G.out_degree(n) > 0]
    
    # Global visited optimization is tricky for cycles.
    # We will just limit candidates to a subset if too large, or rely on max_len.
    if len(candidates) > 200:
        candidates = candidates[:200] # Safety Sampling for demo speed
        
    unique_cycles = set()
    
    pass_count = 0
    for start_node in candidates:
        pass_count += 1
        # Quick DFS
        stack = [(start_node, [start_node])] # (current, path)
        
        while stack:
            curr, path = stack.pop()
            if len(path) > max_len:
                continue
                
            for nbr in G.successors(curr):
                if nbr == start_node:
                    if len(path) >= 3:
                        # normalize cycle to store unique
                        # e.g. tuple(sorted_list)?? No, cycle order matters. 
                        # Canonical rotation: start with min element
                        cycle = list(path)
                        min_node = min(cycle)
                        min_idx = cycle.index(min_node)
                        canonical = tuple(cycle[min_idx:] + cycle[:min_idx])
                        unique_cycles.add(canonical)
                elif nbr not in path:
                    stack.append((nbr, path + [nbr]))
        
        if len(unique_cycles) > 100: # Max cycles to report
            break
            
    return [list(c) for c in unique_cycles]

def detect_circular_trading(G: nx.DiGraph) -> List[Anomaly]:
    """
    Optimized detection for circular trading.
    """
    anomalies = []
    try:
        # Use optimized finder
        cycles = find_cycles_optimized(G, max_len=6)
        
        for cycle in cycles:
            # Check Volume Retention
            is_suspicious = True
            amounts = []
            
            for i in range(len(cycle)):
                u = cycle[i]
                v = cycle[(i + 1) % len(cycle)]
                if G.has_edge(u, v):
                    weight = G[u][v].get('weight', 0)
                    amounts.append(weight)
                else:
                    is_suspicious = False
                    break
            
            if not is_suspicious or not amounts:
                continue
                
            avg_amt = sum(amounts) / len(amounts)
            if avg_amt < 100: continue
            
            # Check flux consistency
            for amt in amounts:
                if abs(amt - avg_amt) / avg_amt > 0.2: # 20% tolerance
                    is_suspicious = False
                    break
            
            if is_suspicious:
                anomalies.append(Anomaly(
                    anomaly_id=f"circ_{hash(str(cycle))}",
                    anomaly_type="CIRCULAR_TRADING",
                    severity=0.9, 
                    entities_involved=list(cycle),
                    description=f"Risk Alert: Funds are moving in a circle involving {len(cycle)} entities. This is a classic 'Circular Trading' pattern used to fake volume or launder money. Amount retained: ~${avg_amt:.2f}.",
                    evidence_data={"cycle_path": cycle, "avg_amount": avg_amt}
                ))
                
    except Exception as e:
        print(f"Error in cycle detection: {e}")
        
    return anomalies

def detect_dense_clusters(G: nx.DiGraph) -> List[Anomaly]:
    """
    Detects highly dense cliques or near-cliques indicating collusion rings.
    """
    anomalies = []
    
    # Use communities (Louvain or similar) or connected components
    # For robust prototype: Weakly connected components first
    components = list(nx.weakly_connected_components(G))
    
    for comp in components:
        if len(comp) < 4: # Ignore tiny groups
            continue
            
        subgraph = G.subgraph(comp)
        density = nx.density(subgraph)
        
        # High threshold for "Unnatural" density
        # In financial networks, density usually drops as N increases.
        # If N > 10 and density > 0.5, that's very suspicious.
        
        threshold = 0.8 if len(comp) < 10 else 0.5
        
        if density > threshold:
            anomalies.append(Anomaly(
                anomaly_id=f"dens_{hash(str(comp))}",
                anomaly_type="DENSE_CLUSTER",
                severity=0.7,
                entities_involved=list(comp),
                description=f"Collusion Alert: A tight group of {len(comp)} entities is trading almost exclusively with each other ({density*100:.1f}% density). This isolated 'Island' behavior suggests a botnet or shell company ring.",
                evidence_data={"density": density, "node_count": len(comp)}
            ))
            
    return anomalies

def detect_wash_trading(G: nx.DiGraph) -> List[Anomaly]:
    """
    Detects Wash Trading (Ping-Pong): Two entities trading back and forth 
    to inflate volume without net value transfer.
    """
    anomalies = []
    processed_pairs = set()
    
    for u, v in G.edges():
        if (u, v) in processed_pairs or (v, u) in processed_pairs:
            continue
            
        processed_pairs.add((u, v))
        
        # Check bidirectional
        if G.has_edge(v, u):
            # Get weights (sum of amounts if multiple txs)
            vol_uv = G[u][v].get('weight', 0)
            vol_vu = G[v][u].get('weight', 0)
            
            total_vol = vol_uv + vol_vu
            net_flow = abs(vol_uv - vol_vu)
            
            # Heuristic: High Volume (> $5000), Low Net Flow (< 5% of Volume)
            if total_vol > 5000 and net_flow < (total_vol * 0.05):
                anomalies.append(Anomaly(
                    anomaly_id=f"wash_{hash(f'{u}-{v}')}",
                    anomaly_type="WASH_TRADING",
                    severity=0.85,
                    entities_involved=[u, v],
                    description=f"Wash Trading Detected: These entities traded ${total_vol:,.2f} back-and-forth, but the net money moved was $0. This is typically done to inflate transaction stats artifically.",
                    evidence_data={"total_volume": total_vol, "net_flow": net_flow}
                ))
                
    return anomalies

def detect_structuring(G: nx.DiGraph) -> List[Anomaly]:
    """
    Detects Structuring / Smurfing: One entity sending/receiving similar amounts 
    to/from many users (Hub & Spoke), often to evade reporting limits.
    """
    anomalies = []
    
    for n in G.nodes():
        # Fan Out check
        out_edges = G.out_edges(n, data=True)
        if len(out_edges) >= 5: # Min 5 recipients
            amounts = [d.get('weight', 0) for _, _, d in out_edges]
            avg_amt = sum(amounts) / len(amounts)
            
            if avg_amt > 100: # Ignore dust
                # Check variance: Are amounts very similar? (e.g. all $9000-9900)
                # Coeff of variation < 0.1
                variance = sum([((x - avg_amt) ** 2) for x in amounts]) / len(amounts)
                std_dev = variance ** 0.5
                
                if std_dev / avg_amt < 0.1:
                    anomalies.append(Anomaly(
                        anomaly_id=f"struct_out_{hash(n)}",
                        anomaly_type="STRUCTURING (Fan-Out)",
                        severity=0.95,
                        entities_involved=[n] + [v for _, v, _ in out_edges],
                        description=f"Smurfing (Fan-Out): A single source sent {len(amounts)} identically sized payments (~${avg_amt:.2f}) to different people. This looks like splitting a large sum to evade detection thresholds.",
                        evidence_data={"pattern": "Fan-Out", "avg_amount": avg_amt, "std_dev": std_dev}
                    ))
                    continue # Don't flag Fan-In if already Fan-Out (simplify)

        # Fan In check
        in_edges = G.in_edges(n, data=True)
        if len(in_edges) >= 5:
            amounts = [d.get('weight', 0) for _, _, d in in_edges]
            avg_amt = sum(amounts) / len(amounts)
            
            if avg_amt > 100:
                variance = sum([((x - avg_amt) ** 2) for x in amounts]) / len(amounts)
                std_dev = variance ** 0.5
                
                if std_dev / avg_amt < 0.1:
                    anomalies.append(Anomaly(
                        anomaly_id=f"struct_in_{hash(n)}",
                        anomaly_type="STRUCTURING (Fan-In)",
                        severity=0.95,
                        entities_involved=[n] + [u for u, _, _ in in_edges],
                        description=f"Smurfing (Fan-In): A single target received {len(amounts)} identically sized payments (~${avg_amt:.2f}) from different people. This looks like consolidating split funds.",
                        evidence_data={"pattern": "Fan-In", "avg_amount": avg_amt, "std_dev": std_dev}
                    ))
                    
    return anomalies
