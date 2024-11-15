import networkx as nx
from typing import Dict, List, Tuple
from ..config import Config
from ..models.user import User

class GraphService:
    def __init__(self):
        self.graph = nx.Graph()
        
    def add_user(self, user: User) -> None:
        """Add a new user node to the graph"""
        self.graph.add_node(user.user_id)
    
    def update_user_connections(self, user: User, similarities: Dict[str, float]) -> None:
        """Update user connections in the graph based on similarities"""
        for other_id, similarity in similarities.items():
            if similarity > Config.SIMILARITY_THRESHOLD:
                self.graph.add_edge(user.user_id, other_id, weight=similarity)
    
    def find_matches(self, user_id: str, top_k: int = None) -> List[Tuple[str, float]]:
        """Find matches using personalized PageRank"""
        if not top_k:
            top_k = Config.TOP_K_MATCHES
            
        if user_id not in self.graph:
            return []
        
        # Calculate personalized PageRank
        pagerank_scores = nx.pagerank(
            self.graph,
            personalization={user_id: 1.0},
            weight='weight'
        )
        
        # Remove the user themselves and sort by score
        del pagerank_scores[user_id]
        matches = sorted(
            pagerank_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]
        
        return matches