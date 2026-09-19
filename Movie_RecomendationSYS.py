# Import necessary libraries
import urllib.request, zipfile
import pandas as pd
from difflib import get_close_matches

# SSL workaround for downloading the dataset
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# Download and extract the dataset
url = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
urllib.request.urlretrieve(url, "ml.zip")

with zipfile.ZipFile("ml.zip") as z:
    z.extractall()

# Load the dataset into a pandas DataFrame
movies = pd.read_csv("ml-latest-small/movies.csv")


def find_by_genre(genre):
    """Print all movies whose genres contain the given text."""
    genre_movies = movies[movies["genres"].str.contains(genre, case=False, na=False)]
    print(genre_movies[["title", "genres"]])


def shared_genres(title1, title2):
    """Return how many genres two movies (by exact title) have in common."""
    index1 = movies[movies["title"] == title1].index[0]
    index2 = movies[movies["title"] == title2].index[0]

    genres1 = movies.iloc[index1]["genres"].split("|")
    genres2 = movies.iloc[index2]["genres"].split("|")

    shared = 0
    for genre in genres1:
        if genre in genres2:
            shared = shared + 1

    return shared


def recommend(target_title, top_n=5):
    """Return the top_n movies most similar to target_title, by shared genres."""
    target_genres = movies[movies["title"] == target_title]["genres"].values[0].split("|")

    results = []

    for i in range(len(movies)):
        other_title = movies.iloc[i]["title"]

        if other_title == target_title:
            continue

        other_genres = movies.iloc[i]["genres"].split("|")
        shared = 0

        for genre in target_genres:
            if genre in other_genres:
                shared = shared + 1

        results.append((other_title, shared))

    results_sorted = sorted(results, key=lambda x: x[1], reverse=True)
    return results_sorted[:top_n]


def find_closest_title(title, cutoff=0.5):
    """Return the closest movie title, or None when no match is found."""
    titles = movies["title"].dropna().tolist()
    matches = get_close_matches(title, titles, n=1, cutoff=cutoff)
    return matches[0] if matches else None


# ---------------- MAIN LOOP ----------------
while True:
    user_movie = input("Enter a movie title (or 'exit' to quit): ")

    if user_movie.lower() == "exit":
        print("Goodbye!")
        break

    closest = find_closest_title(user_movie)

    if closest:
        print("Did you mean:", closest, "?")
        recommendations = recommend(closest)

        print("Because you liked", closest, "you might also like:")
        for title, score in recommendations:
            print(title, "-", score, "shared genres")
    else:
        print("Sorry, no close match found.")

    print()