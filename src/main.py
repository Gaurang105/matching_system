import os
import sys
import logging
from typing import Dict, List

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.services.matching_service import MatchingService

## logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_user_pool() -> List[Dict]:
    """Create sample users"""
    return [
        {
            "user_id": "tech_enthusiast_1",
            "preferences": {
                "age_range": "25-35",
                "location": "NYC",
                "interests": ["tech", "AI", "startups"]
            },
            "personality": {
                "extroversion": 0.7,
                "openness": 0.9,
                "conscientiousness": 0.8
            },
            "prompt": "Passionate about AI and building innovative solutions"
        },
        {
            "user_id": "creative_dev_2",
            "preferences": {
                "age_range": "25-35",
                "location": "SF",
                "interests": ["tech", "design", "art"]
            },
            "personality": {
                "extroversion": 0.6,
                "openness": 0.9,
                "conscientiousness": 0.7
            },
            "prompt": "Creative developer interested in the intersection of art and technology"
        },
        {
            "user_id": "data_scientist_3",
            "preferences": {
                "age_range": "30-40",
                "location": "Boston",
                "interests": ["tech", "data", "machine learning"]
            },
            "personality": {
                "extroversion": 0.5,
                "openness": 0.8,
                "conscientiousness": 0.9
            },
            "prompt": "Data scientist looking to collaborate on ML projects"
        },
        {
            "user_id": "startup_founder_4",
            "preferences": {
                "age_range": "25-35",
                "location": "NYC",
                "interests": ["tech", "entrepreneurship", "innovation"]
            },
            "personality": {
                "extroversion": 0.8,
                "openness": 0.9,
                "conscientiousness": 0.7
            },
            "prompt": "Startup founder seeking tech co-founder and collaborators"
        },
        {
            "user_id": "ux_designer_5",
            "preferences": {
                "age_range": "25-35",
                "location": "SF",
                "interests": ["design", "user experience", "tech"]
            },
            "personality": {
                "extroversion": 0.7,
                "openness": 0.8,
                "conscientiousness": 0.8
            },
            "prompt": "UX designer passionate about creating intuitive user experiences"
        }
    ]

def simulate_new_user() -> Dict:
    """Create a new user to test matching"""
    return {
        "user_id": "new_tech_user",
        "preferences": {
            "age_range": "25-35",
            "location": "NYC",
            "interests": ["tech", "AI", "startups"]
        },
        "personality": {
            "extroversion": 0.7,
            "openness": 0.9,
            "conscientiousness": 0.8
        },
        "prompt": "Looking to connect with AI enthusiasts and startup founders"
    }

def main():
    try:
        # Initialize matching service
        logger.info("\nInitializing matching service...")
        matching_service = MatchingService()
        
        # First, create a pool of users
        logger.info("\nCreating user pool...")
        user_pool = create_user_pool()
        
        # Add users from the pool
        logger.info("\nAdding users from pool:")
        for user_data in user_pool:
            logger.info(f"\nAdding user: {user_data['user_id']}")
            matching_service.signup_user(
                user_id=user_data["user_id"],
                preferences=user_data["preferences"],
                personality=user_data["personality"]
            )
            
            logger.info(f"Processing prompt for user: {user_data['user_id']}")
            matching_service.process_user_prompt(
                user_data["user_id"],
                user_data["prompt"]
            )
        
        logger.info("\n" + "="*50)
        logger.info("User pool created successfully!")
        logger.info(f"Total users in pool: {len(user_pool)}")
        logger.info("="*50)
        
        # Now simulate adding a new user
        logger.info("\nSimulating new user signup...")
        new_user = simulate_new_user()
        
        # Add the new user
        logger.info(f"\nAdding new user: {new_user['user_id']}")
        matching_service.signup_user(
            user_id=new_user["user_id"],
            preferences=new_user["preferences"],
            personality=new_user["personality"]
        )
        
        # Process new user's prompt
        logger.info(f"Processing prompt for new user: {new_user['user_id']}")
        matching_service.process_user_prompt(
            new_user["user_id"],
            new_user["prompt"]
        )
        
        # Find matches for the new user
        logger.info("\nFinding matches for new user...")
        matches = matching_service.find_matches(new_user["user_id"])
        
        # Print results
        logger.info("\nMatches found for new user:")
        logger.info("-" * 40)
        for user_id, score in matches:
            logger.info(f"Match: {user_id}")
            logger.info(f"Similarity Score: {score:.2f}")
            # Find the matching user's details from the pool
            matching_user = next((u for u in user_pool if u["user_id"] == user_id), None)
            if matching_user:
                logger.info(f"Location: {matching_user['preferences']['location']}")
                logger.info(f"Interests: {', '.join(matching_user['preferences']['interests'])}")
                logger.info(f"Prompt: {matching_user['prompt']}")
            logger.info("-" * 40)
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()