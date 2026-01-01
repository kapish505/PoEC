import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data
import networkx as nx
import numpy as np
import gc

class GCNEncoder(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GCNEncoder, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, x, edge_index, edge_weight=None):
        x = self.conv1(x, edge_index, edge_weight)
        x = F.relu(x)
        x = self.conv2(x, edge_index, edge_weight)
        return x

class GCNDecoder(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GCNDecoder, self).__init__()
        # Simple inner product decoder or MLP
        self.lin1 = nn.Linear(in_channels * 2, hidden_channels)
        self.lin2 = nn.Linear(hidden_channels, 1)

    def forward(self, z, edge_index):
        # Concatenate source and target embeddings
        row, col = edge_index
        z_src = z[row]
        z_dst = z[col]
        edge_feat = torch.cat([z_src, z_dst], dim=1)
        
        x = F.relu(self.lin1(edge_feat))
        x = torch.sigmoid(self.lin2(x))
        return x

class GraphAutoEncoder(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GraphAutoEncoder, self).__init__()
        self.encoder = GCNEncoder(in_channels, hidden_channels, out_channels)
        self.decoder = GCNDecoder(out_channels, hidden_channels, 1)

    def forward(self, x, edge_index, edge_weight=None):
        z = self.encoder(x, edge_index, edge_weight)
        return z

    def recon_loss(self, z, edge_index, edge_weight=None):
        # Contrastive loss or MSE on edge existance
        # For simplicity: Predict probability of *existing* edges (should be close to 1)
        # And negative edges (should be close to 0)
        
        pos_out = self.decoder(z, edge_index)
        pos_loss = -torch.log(pos_out + 1e-15).mean()
        
        # Negative sampling
        neg_edge_index = torch.randint(0, z.size(0), edge_index.size(), dtype=torch.long)
        neg_out = self.decoder(z, neg_edge_index)
        neg_loss = -torch.log(1 - neg_out + 1e-15).mean()
        
        return pos_loss + neg_loss
    
    def predict_anomaly_scores(self, z, edge_index):
        """
        Returns edge anomaly scores (1.0 - probability of existence).
        High score = Model thinks edge shouldn't exist = Anomaly.
        """
        with torch.no_grad():
            out = self.decoder(z, edge_index)
            scores = 1.0 - out.squeeze()
        return scores

class AnomalyDetector:
    def __init__(self, input_dim=5):
        self.model = GraphAutoEncoder(input_dim, 16, 8)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)
        
    def prepare_data(self, G: nx.DiGraph) -> Data:
        """
        Converts NetworkX graph to PyG Data object with feature engineering.
        """
        # Node mapping
        nodes = list(G.nodes())
        node_map = {n: i for i, n in enumerate(nodes)}
        
        # Features: [in_degree, out_degree, total_in_amount, total_out_amount, clustering_coeff]
        x = []
        for n in nodes:
            in_deg = G.in_degree(n)
            out_deg = G.out_degree(n)
            
            # Simple aggregations
            in_amt = sum(d.get('weight', 0) for _, _, d in G.in_edges(n, data=True))
            out_amt = sum(d.get('weight', 0) for _, _, d in G.out_edges(n, data=True))
            
            # Placeholder for clustering (networkx logic is slow for large graphs, using 0 for speed)
            clustering = 0 
            
            x.append([in_deg, out_deg, in_amt, out_amt, clustering])
            
        x = torch.tensor(x, dtype=torch.float)
        # Normalize features
        if x.size(0) > 1:
            x = (x - x.mean(dim=0)) / (x.std(dim=0) + 1e-6)
            
        # Edges
        edge_indices = []
        edge_weights = []
        transactions_map = {} # edge_index col -> tx_ids
        
        for i, (u, v, d) in enumerate(G.edges(data=True)):
            src = node_map[u]
            dst = node_map[v]
            edge_indices.append([src, dst])
            edge_weights.append(d.get('weight', 0))
            
        edge_index = torch.tensor(edge_indices, dtype=torch.long).t().contiguous()
        edge_weight = torch.tensor(edge_weights, dtype=torch.float)
        
    
    def train_baseline(self, G: nx.DiGraph, epochs=50):
        data, _ = self.prepare_data(G)
        self.model.train()
        
        for epoch in range(epochs):
            self.optimizer.zero_grad()
            z = self.model(data.x, data.edge_index, data.edge_attr)
            loss = self.model.recon_loss(z, data.edge_index, data.edge_attr)
            loss.backward()
            self.optimizer.step()
            
        # Free up training graph memory immediately
        self.optimizer.zero_grad()
        loss = None
        z = None
        gc.collect()
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
            
        return data # Return processed data for inference
    
    def detect(self, G: nx.DiGraph):
        data, node_map = self.prepare_data(G)
        inv_map = {v: k for k, v in node_map.items()}
        
        self.model.eval()
        
        # OOM FIX: Wrap entire inference in no_grad to prevent graph storage
        with torch.no_grad():
            z = self.model(data.x, data.edge_index, data.edge_attr)
            scores = self.model.predict_anomaly_scores(z, data.edge_index)
        
        # Thresholding (e.g., top 5% or > 0.8)
        anomalies = []
        all_scores = []
        
        if scores.ndim == 0:
             scores = scores.unsqueeze(0)
             
        for i, score in enumerate(scores):
            src_idx = data.edge_index[0, i].item()
            dst_idx = data.edge_index[1, i].item()
            src = inv_map[src_idx]
            dst = inv_map[dst_idx]
            
            # Store all scores for visualization/debugging
            all_scores.append({
                "source": src,
                "target": dst,
                "score": float(score)
            })
            
            if score > 0.5: # Lowered threshold to 0.5 to catch "Watchlist" candidates
                anomalies.append({
                    "source": src,
                    "target": dst,
                    "score": float(score),
                    "type": "STRUCTURAL_ANOMALY",
                    "explanation": f"Model assigned {float(score):.2f} improbability to this link based on node features."
                })
        
        # Explicit cleanup
        del data
        del z
        del scores
        gc.collect()
                
        return {"anomalies": anomalies, "edge_scores": all_scores}
