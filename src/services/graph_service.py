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
        
        pagerank_scores = nx.pagerank(
            self.graph,
            personalization={user_id: 1.0},
            weight='weight'
        )
        del pagerank_scores[user_id]
        
        # Normalize scores to 0-1 range
        if pagerank_scores:
            max_score = max(pagerank_scores.values())
            min_score = min(pagerank_scores.values())
            score_range = max_score - min_score
            
            if score_range > 0:
                normalized_scores = {
                    k: (v - min_score) / score_range 
                    for k, v in pagerank_scores.items()
                }
            else:
                normalized_scores = pagerank_scores
                
            matches = sorted(
                normalized_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:top_k]
        else:
            matches = []
        
        return matches