from typing import Dict, List, Tuple
import numpy as np
from scipy.spatial.distance import cosine
from datetime import datetime

from ..models.user import User
from ..services.nlp_service import NLPService
from ..services.graph_service import GraphService
from ..config import Config

class MatchingService:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.nlp_service = NLPService()
        self.graph_service = GraphService()
    
    def signup_user(self, user_id: str, preferences: Dict, 
                   personality: Dict) -> User:
        """Register a new user"""
        user = User(
            user_id=user_id,
            preferences=preferences,
            personality=personality
        )
        self.users[user_id] = user
        self.graph_service.add_user(user)
        return user
    
    def process_user_prompt(self, user_id: str, prompt: str) -> None:
        """Process and store user prompt embedding"""
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found")
            
        prompt_embedding = self.nlp_service.get_prompt_embedding(prompt)
        self.users[user_id].prompt_embedding = prompt_embedding
        
        # Update similarities and graph
        similarities = self._calculate_similarities(user_id)
        self.graph_service.update_user_connections(
            self.users[user_id], similarities)
    
    def _calculate_similarities(self, user_id: str) -> Dict[str, float]:
        """Calculate similarities between a user and all other users"""
        similarities = {}
        user = self.users[user_id]
        
        for other_id, other_user in self.users.items():
            if other_id != user_id:
                similarity = self._calculate_user_similarity(user, other_user)
                similarities[other_id] = similarity
                
        return similarities
    
    def _calculate_user_similarity(self, user1: User, user2: User) -> float:
        """Calculate similarity between two users"""
        # Preference similarity
        pref_sim = sum(
            user1.preferences[k] == user2.preferences[k]
            for k in user1.preferences
        ) / len(user1.preferences)
        
        # Prompt similarity
        prompt_sim = 0
        if user1.prompt_embedding is not None and user2.prompt_embedding is not None:
            prompt_sim = 1 - cosine(
                user1.prompt_embedding.flatten(),
                user2.prompt_embedding.flatten()
            )
        
        # Personality similarity
        pers_sim = sum(
            user1.personality[k] == user2.personality[k]
            for k in user1.personality
        ) / len(user1.personality)
        
        # Weighted combination
        return (Config.PREFERENCE_WEIGHT * pref_sim +
                Config.PROMPT_WEIGHT * prompt_sim +
                Config.PERSONALITY_WEIGHT * pers_sim)
    
    def find_matches(self, user_id: str, top_k: int = None) -> List[Tuple[str, float]]:
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found")
            
        return self.graph_service.find_matches(user_id, top_k)