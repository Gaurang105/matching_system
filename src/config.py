import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Model Settings
    BERT_MODEL_NAME = os.getenv('BERT_MODEL_NAME', 'bert-base-uncased')
    DEVICE = 'cpu'
    
    # Matching System Settings
    SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', 0.6))
    TOP_K_MATCHES = int(os.getenv('TOP_K_MATCHES', 5))
    
    # Development Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Weights for similarity calculation
    PREFERENCE_WEIGHT = 0.4
    PROMPT_WEIGHT = 0.4
    PERSONALITY_WEIGHT = 0.2

    # Preference Sub-weights
    AGE_WEIGHT = 0.3
    LOCATION_WEIGHT = 0.3
    INTERESTS_WEIGHT = 0.4
    
    # Location Matching Weights
    LOCATION_SEMANTIC_WEIGHT = 0.7
    LOCATION_GEOGRAPHIC_WEIGHT = 0.3
    
    # Interest Matching Weights
    INTERESTS_EXACT_WEIGHT = 0.7
    INTERESTS_FUZZY_WEIGHT = 0.3
    
    # Personality Match Threshold
    PERSONALITY_MATCH_THRESHOLD = 0.2  # 20% difference allowed
    
    # Geographic Settings
    LOCATION_DISTANCE_SCALE = 500  # distance decay
    
    # Cache Settings
    LOCATION_CACHE_SIZE = 1000