from typing import Dict, List, Tuple, Optional
import numpy as np
from scipy.spatial.distance import cosine
from datetime import datetime
from fuzzywuzzy import fuzz
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from collections import OrderedDict

from ..models.user import User
from ..services.nlp_service import NLPService
from ..services.graph_service import GraphService
from ..config import Config

class MatchingService:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.nlp_service = NLPService()
        self.graph_service = GraphService()
        self.geocoder = Nominatim(user_agent="matching_system")
        self.location_cache = OrderedDict()
    
    def signup_user(self, user_id: str, preferences: Dict, 
                   personality: Dict) -> User:
        """Register a new user"""
        # Validate preferences
        required_fields = ['age_range', 'location', 'interests']
        if not all(field in preferences for field in required_fields):
            raise ValueError(f"Missing required preferences: {required_fields}")
            
        user = User(
            user_id=user_id,
            preferences=preferences,
            personality=personality
        )
        self.users[user_id] = user
        self.graph_service.add_user(user)
        return user
    
    def _calculate_age_range_overlap(self, range1: str, range2: str) -> float:
        """overlap between two age ranges"""
        try:
            start1, end1 = map(int, range1.split('-'))
            start2, end2 = map(int, range2.split('-'))
            
            overlap_start = max(start1, start2)
            overlap_end = min(end1, end2)
            
            if overlap_start > overlap_end:
                return 0.0
                
            overlap_length = overlap_end - overlap_start + 1
            range1_length = end1 - start1 + 1
            range2_length = end2 - start2 + 1
            
            return (2 * overlap_length) / (range1_length + range2_length)
        except (ValueError, AttributeError):
            return 0.0
    
    def _get_location_coords(self, location: str) -> Optional[Tuple[float, float]]:
        """Get coordinates for a location with caching"""
        if location in self.location_cache:
            return self.location_cache[location]
            
        try:
            # Get location data
            location_data = self.geocoder.geocode(location)
            if location_data:
                coords = (location_data.latitude, location_data.longitude)
                
                # Update cache with LRU behavior
                if len(self.location_cache) >= Config.LOCATION_CACHE_SIZE:
                    self.location_cache.popitem(last=False)
                self.location_cache[location] = coords
                
                return coords
        except Exception as e:
            if Config.DEBUG:
                print(f"Geocoding error for {location}: {e}")
        return None
    
    def _calculate_location_similarity(self, loc1: str, loc2: str) -> float:
        """location similarity using both semantic and geographic distance"""
        # Semantic similarity using fuzzy matching
        semantic_sim = fuzz.token_sort_ratio(loc1, loc2) / 100.0
        
        # Geographic distance similarity
        coords1 = self._get_location_coords(loc1)
        coords2 = self._get_location_coords(loc2)
        
        if coords1 and coords2:
            distance = geodesic(coords1, coords2).kilometers
            geo_sim = np.exp(-distance/Config.LOCATION_DISTANCE_SCALE)
        else:
            geo_sim = semantic_sim
        
        # Combine both similarities
        return (Config.LOCATION_SEMANTIC_WEIGHT * semantic_sim + 
                Config.LOCATION_GEOGRAPHIC_WEIGHT * geo_sim)
    
    def _calculate_interests_similarity(self, interests1: List[str], 
                                     interests2: List[str]) -> float:
        """Calculate interest similarity using Jaccard similarity and fuzzy matching"""
        # Normalize interests
        norm_interests1 = [i.lower().strip() for i in interests1]
        norm_interests2 = [i.lower().strip() for i in interests2]
        
        # Exact matches (Jaccard similarity)
        intersection = set(norm_interests1) & set(norm_interests2)
        union = set(norm_interests1) | set(norm_interests2)
        jaccard_sim = len(intersection) / len(union) if union else 0
        
        # Non-exact matches (Fuzzy matching)
        fuzzy_scores = []
        for int1 in norm_interests1:
            if int1 not in intersection:
                best_score = max(
                    (fuzz.ratio(int1, int2) / 100.0 
                     for int2 in norm_interests2 if int2 not in intersection),
                    default=0
                )
                fuzzy_scores.append(best_score)
        
        fuzzy_avg = np.mean(fuzzy_scores) if fuzzy_scores else 0
        return (Config.INTERESTS_EXACT_WEIGHT * jaccard_sim + 
                Config.INTERESTS_FUZZY_WEIGHT * fuzzy_avg)
    
    def _calculate_user_similarity(self, user1: User, user2: User) -> float:
        # Calculate preference similarities
        age_sim = self._calculate_age_range_overlap(
            user1.preferences["age_range"],
            user2.preferences["age_range"]
        )
        
        location_sim = self._calculate_location_similarity(
            user1.preferences["location"],
            user2.preferences["location"]
        )
        
        interests_sim = self._calculate_interests_similarity(
            user1.preferences["interests"],
            user2.preferences["interests"]
        )
        
        # Combine preference similarities
        pref_sim = (
            Config.AGE_WEIGHT * age_sim +
            Config.LOCATION_WEIGHT * location_sim +
            Config.INTERESTS_WEIGHT * interests_sim
        )
        
        # Calculate prompt similarity
        prompt_sim = 0
        if user1.prompt_embedding is not None and user2.prompt_embedding is not None:
            prompt_sim = 1 - cosine(
                user1.prompt_embedding.flatten(),
                user2.prompt_embedding.flatten()
            )
        
        # Calculate personality similarity with threshold
        pers_sim = sum(
            abs(user1.personality[k] - user2.personality[k]) <= Config.PERSONALITY_MATCH_THRESHOLD
            for k in user1.personality
        ) / len(user1.personality)
        
        # Final weighted combination
        return (Config.PREFERENCE_WEIGHT * pref_sim +
                Config.PROMPT_WEIGHT * prompt_sim +
                Config.PERSONALITY_WEIGHT * pers_sim)
    
    def process_user_prompt(self, user_id: str, prompt: str) -> None:
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found")
            
        prompt_embedding = self.nlp_service.get_prompt_embedding(prompt)
        self.users[user_id].prompt_embedding = prompt_embedding
        
        # Update similarities and graph
        similarities = self._calculate_similarities(user_id)
        self.graph_service.update_user_connections(
            self.users[user_id], similarities)
    
    def _calculate_similarities(self, user_id: str) -> Dict[str, float]:
        similarities = {}
        user = self.users[user_id]
        
        for other_id, other_user in self.users.items():
            if other_id != user_id:
                similarity = self._calculate_user_similarity(user, other_user)
                similarities[other_id] = similarity
                
        return similarities
    
    def find_matches(self, user_id: str, top_k: int = None) -> List[Tuple[str, float]]:
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found")
            
        return self.graph_service.find_matches(user_id, top_k)