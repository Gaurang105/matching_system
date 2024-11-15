import os
import sys
import logging
from typing import Dict, List

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.services.matching_service import MatchingService

# Basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_user_pool() -> List[Dict]:
    """Create sample users"""
    return [
        {
            "user_id": "tech_1",
            "preferences": {
                "age_range": "25-35",
                "location": "New York",
                "interests": ["AI", "startups", "tech"]
            },
            "personality": {
                "extroversion": 0.7,
                "openness": 0.9,
                "conscientiousness": 0.8
            },
            "prompt": "AI enthusiast looking for tech collaborations"
        },
        {
            "user_id": "design_1",
            "preferences": {
                "age_range": "25-35",
                "location": "San Francisco",
                "interests": ["design", "tech", "UI/UX"]
            },
            "personality": {
                "extroversion": 0.6,
                "openness": 0.9,
                "conscientiousness": 0.7
            },
            "prompt": "Designer interested in tech and art"
        },
        {
            "user_id": "data_1",
            "preferences": {
                "age_range": "30-40",
                "location": "Boston",
                "interests": ["data science", "ML", "AI"]
            },
            "personality": {
                "extroversion": 0.5,
                "openness": 0.8,
                "conscientiousness": 0.9
            },
            "prompt": "Data scientist seeking ML projects"
        },
        {
            "user_id": "dev_1",
            "preferences": {
                "age_range": "25-35",
                "location": "Seattle",
                "interests": ["backend", "cloud", "DevOps"]
            },
            "personality": {
                "extroversion": 0.4,
                "openness": 0.8,
                "conscientiousness": 0.9
            },
            "prompt": "Backend developer interested in cloud architecture"
        },
        {
            "user_id": "product_1",
            "preferences": {
                "age_range": "30-40",
                "location": "New York",
                "interests": ["product management", "tech", "startups"]
            },
            "personality": {
                "extroversion": 0.8,
                "openness": 0.7,
                "conscientiousness": 0.8
            },
            "prompt": "Product manager looking for technical co-founder"
        },
        {
            "user_id": "ml_1",
            "preferences": {
                "age_range": "25-35",
                "location": "Boston",
                "interests": ["machine learning", "NLP", "AI"]
            },
            "personality": {
                "extroversion": 0.5,
                "openness": 0.9,
                "conscientiousness": 0.8
            },
            "prompt": "ML researcher focusing on natural language processing"
        },
        {
            "user_id": "frontend_1",
            "preferences": {
                "age_range": "25-35",
                "location": "San Francisco",
                "interests": ["frontend", "React", "UX"]
            },
            "personality": {
                "extroversion": 0.6,
                "openness": 0.8,
                "conscientiousness": 0.7
            },
            "prompt": "Frontend developer specializing in React and modern JS"
        },
        {
            "user_id": "startup_1",
            "preferences": {
                "age_range": "30-40",
                "location": "New York",
                "interests": ["startups", "entrepreneurship", "AI"]
            },
            "personality": {
                "extroversion": 0.8,
                "openness": 0.9,
                "conscientiousness": 0.7
            },
            "prompt": "Startup founder building AI solutions"
        },
        {
            "user_id": "mobile_1",
            "preferences": {
                "age_range": "25-35",
                "location": "Seattle",
                "interests": ["mobile", "iOS", "Swift"]
            },
            "personality": {
                "extroversion": 0.6,
                "openness": 0.7,
                "conscientiousness": 0.8
            },
            "prompt": "iOS developer building mobile applications"
        },
        {
            "user_id": "security_1",
            "preferences": {
                "age_range": "30-40",
                "location": "San Francisco",
                "interests": ["security", "blockchain", "crypto"]
            },
            "personality": {
                "extroversion": 0.4,
                "openness": 0.8,
                "conscientiousness": 0.9
            },
            "prompt": "Security engineer interested in blockchain"
        },
        {
            "user_id": "data_2",
            "preferences": {
                "age_range": "25-35",
                "location": "Chicago",
                "interests": ["data engineering", "big data", "cloud"]
            },
            "personality": {
                "extroversion": 0.5,
                "openness": 0.8,
                "conscientiousness": 0.9
            },
            "prompt": "Data engineer working with big data solutions"
        },
        {
            "user_id": "research_1",
            "preferences": {
                "age_range": "30-40",
                "location": "Boston",
                "interests": ["AI research", "deep learning", "computer vision"]
            },
            "personality": {
                "extroversion": 0.4,
                "openness": 0.9,
                "conscientiousness": 0.8
            },
            "prompt": "AI researcher focusing on computer vision applications"
        },
        {
            "user_id": "fullstack_1",
            "preferences": {
                "age_range": "25-35",
                "location": "Austin",
                "interests": ["fullstack", "JavaScript", "Python"]
            },
            "personality": {
                "extroversion": 0.6,
                "openness": 0.8,
                "conscientiousness": 0.7
            },
            "prompt": "Full stack developer proficient in multiple technologies"
        },
        {
            "user_id": "gaming_1",
            "preferences": {
                "age_range": "25-35",
                "location": "Seattle",
                "interests": ["game development", "Unity", "3D graphics"]
            },
            "personality": {
                "extroversion": 0.6,
                "openness": 0.9,
                "conscientiousness": 0.7
            },
            "prompt": "Game developer working with Unity and 3D graphics"
        },
        {
            "user_id": "robotics_1",
            "preferences": {
                "age_range": "30-40",
                "location": "Boston",
                "interests": ["robotics", "AI", "computer vision"]
            },
            "personality": {
                "extroversion": 0.5,
                "openness": 0.9,
                "conscientiousness": 0.8
            },
            "prompt": "Robotics engineer working on AI-powered systems"
        }
    ]

def simulate_new_user() -> Dict:
    """Create a test user"""
    return {
        "user_id": "new_user",
        "preferences": {
            "age_range": "25-35",
            "location": "New York",
            "interests": ["AI", "tech", "startups"]
        },
        "personality": {
            "extroversion": 0.7,
            "openness": 0.9,
            "conscientiousness": 0.8
        },
        "prompt": "Looking for AI and tech collaborators"
    }

def main():
    try:
        # Initialize service
        matching_service = MatchingService()
        
        # Create user pool
        user_pool = create_user_pool()
        
        # Add users to system
        for user in user_pool:
            matching_service.signup_user(
                user_id=user["user_id"],
                preferences=user["preferences"],
                personality=user["personality"]
            )
            matching_service.process_user_prompt(
                user["user_id"],
                user["prompt"]
            )
        
        # Add test user
        new_user = simulate_new_user()
        matching_service.signup_user(
            user_id=new_user["user_id"],
            preferences=new_user["preferences"],
            personality=new_user["personality"]
        )
        matching_service.process_user_prompt(
            new_user["user_id"],
            new_user["prompt"]
        )
        
        # Find matches
        matches = matching_service.find_matches(new_user["user_id"])
        
        # Print results
        logger.info("\nMatches for new user:")
        for user_id, score in matches:
            logger.info(f"Match: {user_id}, Score: {score:.2f}")
            match_user = next((u for u in user_pool if u["user_id"] == user_id), None)
            if match_user:
                logger.info(f"Location: {match_user['preferences']['location']}")
                logger.info(f"Interests: {', '.join(match_user['preferences']['interests'])}")
                logger.info("---")
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()