# AI Powered Matching System

A matching system that uses NLP, graph algorithms, and multi-factor similarity calculations to connect users based on their preferences, interests, location, and personality traits.

## Features

- Multi-factor Matching: Combines preferences, personality traits, and text-based prompts
- Location-aware: Uses both semantic and geographic distance for location matching
- Intelligent Interest Matching: Combines Jaccard similarity with fuzzy matching for interests
- NLP-powered: Uses BERT embeddings for understanding user prompts
- Graph-based: Implements PageRank algorithm for finding relevant matches

## Technical Stack

- Python 3.11.5
- PyTorch & Transformers (BERT)
- NetworkX for graph algorithms
- Fuzzy string matching
- Geopy for location services

## Installation

1. Clone the Repo
2. Install dependencies
3. Create a .env file:

BERT_MODEL_NAME=bert-base-uncased
DEVICE=cpu
SIMILARITY_THRESHOLD=0.6
TOP_K_MATCHES=5
DEBUG=True

4. Run this command to run the project:  python -m src.main