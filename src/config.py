import os
from dotenv import load_dotenv
import torch

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