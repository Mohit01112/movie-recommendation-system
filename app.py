from flask import Flask, render_template, request
import pickle
import requests
import os

app = Flask(__name__)

# Get the directory where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load files
with open(os.path.join(BASE_DIR, "movie_list.pkl"), "rb") as f:
    movies = pickle.load(f)

with open(os.path.join(BASE_DIR, "similarity.pkl"), "rb") as f:
    similarity = pickle.load(f)

# List of all movie titles
movie_list = movies["title"].tolist()


def fetch_poster(movie_id):
    """
    Fetch poster from TMDB API
    """
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"

        params = {
            "api_key": os.getenv("TMDB_API_KEY"),
            "language": "en-US"
        }

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"

    except Exception as e:
        print("Poster Error:", e)

    return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):
    try:
        movie = movie.strip()

        if movie not in movie_list:
            print(f"Movie '{movie}' not found.")
            return []

        index = movies[movies["title"] == movie].index[0]

        recommendations = similarity[index]

        recommended_movies = []

        for item in recommendations:

            if isinstance(item, tuple):
                movie_index = item[0]
            else:
                movie_index = item

            movie_id = movies.iloc[movie_index].movie_id

            recommended_movies.append({
                "title": movies.iloc[movie_index].title,
                "poster": fetch_poster(movie_id)
            })

        return recommended_movies

    except Exception as e:
        print("Recommendation Error:", e)
        return []


@app.route("/", methods=["GET", "POST"])
def home():

    recommendations = None
    selected_movie = ""

    if request.method == "POST":

        selected_movie = request.form.get(
            "selected_movie",
            ""
        ).strip()

        if selected_movie:
            recommendations = recommend(selected_movie)

    return render_template(
        "index.html",
        movie_list=movie_list,
        recommendations=recommendations,
        selected_movie=selected_movie
    )


if __name__ == "__main__":
    app.run()
