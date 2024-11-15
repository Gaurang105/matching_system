from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np

@dataclass
class User:
    user_id: str
    preferences: Dict
    personality: Dict
    interactions: List = field(default_factory=list)
    prompt_embedding: Optional[np.ndarray] = None