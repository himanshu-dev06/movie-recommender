# Movie Recommendation System

A content-based movie recommender built in Python using the MovieLens dataset.
It takes a movie title (even with typos) and suggests similar movies based on shared genres.

## How it works
1. Loads the MovieLens dataset with pandas
2. Corrects typos in the movie title using difflib
3. Compares genres between movies to find the most similar ones
4. Recommends the top 5 matches

## Setup
pip install -r requirements.txt
python Movie_RecomendationSYS.py

The dataset downloads automatically the first time you run it.

## Files
- Movie_RecomendationSYS.py — the main program
