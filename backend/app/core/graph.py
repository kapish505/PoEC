import networkx as nx
from typing import List, Any
from app.models import Transaction, GraphSnapshot
from app.core.hashing import hash_content
from datetime import datetime

def build_graph(transactions: List[Transaction]) -> nx.DiGraph:
    """
    Constructs a directed graph from a list of transactions.
    Edges are weighted by aggregated amount.
    """
    G = nx.DiGraph()
    
    for tx in transactions:
        u, v = tx.source_entity, tx.target_entity
        amount = tx.amount
        ts_str = tx.timestamp.strftime("%Y-%m-%d")
        
        if G.has_edge(u, v):
            G[u][v]['weight'] += amount
            G[u][v]['count'] += 1
            G[u][v]['transactions'].append(tx.transaction_id)
            G[u][v]['types'].add(tx.transaction_type)
            G[u][v]['dates'].add(ts_str)
        else:
            G.add_edge(u, v, 
                weight=amount, 
                count=1, 
                transactions=[tx.transaction_id],
                types={tx.transaction_type},
                dates={ts_str}
            )
            
    # Convert sets to lists for JSON serialization
    for u, v, data in G.edges(data=True):
        data['types'] = list(data['types'])
        data['dates'] = sorted(list(data['dates']))
            
    return G

def snapshot_graph(G: nx.DiGraph) -> GraphSnapshot:
    """
    Creates a snapshot metadata object + hash from the graph.
    """
    # Serialize for hashing (node-link data)
    data = nx.node_link_data(G)
    content_hash = hash_content(data)
    
    return GraphSnapshot(
        snapshot_id=content_hash[:16], # partial hash as ID
        start_date=datetime.now(), # Placeholder, in real app derive from tx range
        end_date=datetime.now(),
        node_count=G.number_of_nodes(),
        edge_count=G.number_of_edges(),
        data_hash=content_hash
    )

def build_time_sliced_graphs(transactions: List[Transaction], window: str = 'M') -> List[tuple[str, nx.DiGraph]]:
    """
    Slices transactions into time windows (e.g., 'M' for Month) and builds graphs for each.
    Returns list of (slice_label, DiGraph).
    """
    slices = {}
    
    for tx in transactions:
        # Determine slice key
        ts = tx.timestamp
        if window == 'M':
            key = ts.strftime('%Y-%m') # 2024-01
        elif window == 'Q':
            quarter = (ts.month - 1) // 3 + 1
            key = f"{ts.year}-Q{quarter}"
        else:
            key = "ALL"
            
        if key not in slices:
            slices[key] = []
        slices[key].append(tx)
        
    results = []
    # Sort keys to ensure chronological order
    sorted_keys = sorted(slices.keys())
    
    for key in sorted_keys:
        print(f"DEBUG: Building graph for slice {key} with {len(slices[key])} txs")
        sub_graph = build_graph(slices[key])
        results.append((key, sub_graph))
        
    return results
