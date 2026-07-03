from flask import Flask, render_template, request
import pickle
import requests

app = Flask(__name__)

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values.tolist()


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path

    except Exception as e:
        print("Poster Error:", e)

    return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]

        # Get precomputed recommendations
        recommendations = similarity[index]

        recommended_movies = []

        for item in recommendations:

            # If stored as (movie_index, score)
            if isinstance(item, tuple):
                movie_index = item[0]
            else:
                # If stored as only movie indices
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
        selected_movie = request.form.get("selected_movie")

        if selected_movie:
            recommendations = recommend(selected_movie)

    return render_template(
        "index.html",
        movie_list=movie_list,
        recommendations=recommendations,
        selected_movie=selected_movie
    )


if __name__ == "__main__":
    app.run(debug=True)