from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np

@dataclass
class User:
    user_id: str
    preferences: Dict
    personality: Dict
    prompt_embedding: Optional[np.ndarray] = None