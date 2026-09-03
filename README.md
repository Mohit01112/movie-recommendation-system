<div align="center">

# 🎬 Movie Recommendation System

### A Content-Based Movie Recommendation Engine built with Flask, Scikit-learn & TMDB API

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.1-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Scikit--learn](https://img.shields.io/badge/Scikit--learn-1.7.0-orange?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render&logoColor=white)](https://render.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#)

**Select a movie → Get similar movie recommendations → See their posters, instantly.**

[🚀 Live Demo](https://movie-recommendation-system-r3e5.onrender.com/) · [💻 GitHub Repo](https://github.com/Mohit01112/movie-recommendation-system) · [🐛 Report Bug](#) · [✨ Request Feature](#)

</div>

---

## 📖 Overview

A machine learning-based web application that recommends movies similar to a user-selected movie using a **content-based recommendation approach**, a **precomputed similarity matrix**, and a lightweight **Flask** front end. Movie posters are fetched dynamically via the **TMDB API**, so recommendations always come with visuals.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎬 Content-Based Engine | Recommends movies using similarity, not user ratings |
| 🧠 Precomputed Similarity | Similarity matrix is calculated once and reused for speed |
| 🌐 Flask Web App | Clean, simple interface for movie selection |
| 🔍 Interactive Selection | Pick any movie from the dataset via dropdown |
| 🖼️ Dynamic Posters | Live poster fetching from the TMDB API |
| ⚡ Fast Response | No on-the-fly similarity computation |
| 🛡️ Robust Error Handling | Graceful fallback for API / data errors |
| ☁️ Production Deployment | Hosted on Render using Gunicorn |

---

## 🎯 How It Works

```
1. User selects a movie
2. App checks if the movie exists in the dataset
3. Finds the movie's index
4. Retrieves its row from the similarity matrix
5. Identifies the most similar movies
6. Extracts their TMDB movie IDs
7. Calls the TMDB API to fetch poster images
8. Renders recommendations + posters to the user
```

---

## 🏗️ Architecture

```
                Movie Selection
                       │
                       ▼
                Flask Web App
                       │
                       ▼
         Movie Dataset (movie_list.pkl)
                       │
                       ▼
               Find Movie Index
                       │
                       ▼
       Similarity Matrix (similarity.pkl)
                       │
                       ▼
                Similar Movies
                       │
                       ▼
                   Movie IDs
                       │
                       ▼
                  TMDB API
                       │
                       ▼
                Movie Posters
                       │
                       ▼
              🎉 Recommendations
```

---

## 📁 Project Structure

```
movie-recommendation-system/
│
├── app.py                 # Flask application entry point
├── movie_list.pkl          # Processed movie dataset
├── similarity.pkl          # Precomputed similarity matrix
├── requirements.txt        # Python dependencies
├── README.md
│
├── templates/
│   └── index.html          # Front-end template
│
└── static/
    └── ...                 # CSS / static assets
```

---

## 🧠 Recommendation System

The engine relies on **similarity between movies**, not user-to-user behavior or ratings.

**Movie dataset** — loaded from `movie_list.pkl`, using `movies["title"]` and `movies.iloc[movie_index].movie_id`.

**Similarity data** — loaded once at startup from `similarity.pkl`:

```python
with open(os.path.join(BASE_DIR, "similarity.pkl"), "rb") as f:
    similarity = pickle.load(f)
```

When a movie is selected:

```python
index = movies[movies["title"] == movie].index[0]
recommendations = similarity[index]
```

---

## 🌐 TMDB API Integration

Posters are fetched using the movie's TMDB ID:

```python
url = f"https://api.themoviedb.org/3/movie/{movie_id}"
```

The API key is read securely from an environment variable:

```python
os.getenv("TMDB_API_KEY")
```

<details>
<summary>🖼️ <b>Click to view the full <code>fetch_poster()</code> function</b></summary>

```python
def fetch_poster(movie_id):
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
```

</details>

If a poster can't be retrieved, a **placeholder image** is shown instead — the app never breaks.

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Language** | Python 3.11 |
| **Backend** | Flask, Gunicorn |
| **ML / Data** | Pandas, NumPy, Scikit-learn, Pickle |
| **API** | Requests, TMDB API |
| **Frontend** | HTML, CSS |
| **Deployment** | Render |

</div>

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/Mohit01112/movie-recommendation-system.git
```

**2. Navigate to the project**
```bash
cd movie-recommendation-system
```

**3. Create a virtual environment** *(Windows)*
```bash
python -m venv venv
```

**4. Activate the virtual environment**
```bash
.\venv\Scripts\Activate.ps1
```

**5. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
TMDB_API_KEY=your_tmdb_api_key
```

The app reads it via:

```python
os.getenv("TMDB_API_KEY")
```

> ⚠️ **Never commit your API key to GitHub.**

**On Render:** add `TMDB_API_KEY` as an environment variable in your service's dashboard.

---

## 📦 Requirements

```text
Flask==3.1.1
requests==2.32.5
pandas==2.3.1
numpy==2.3.1
scikit-learn==1.7.0
gunicorn==23.0.0
pyarrow
```

```bash
pip install -r requirements.txt
```

---

## ▶️ Running Locally

```bash
python app.py
```

Then open your browser at:

```
http://127.0.0.1:5000
```

---

## 🖼️ Usage Guide

1. Open the application.
2. Select a movie from the dropdown list.
3. Submit your selection.
4. The engine finds similar movies.
5. Posters are fetched live from TMDB.
6. Recommendations are displayed instantly. 🎉

---

## 📊 Example Workflow

```
Selected Movie: "The Dark Knight"
        ↓
   Find Movie Index
        ↓
   Similarity Matrix
        ↓
   Find Similar Movies
        ↓
   Retrieve Movie IDs
        ↓
      TMDB API
        ↓
   Fetch Posters
        ↓
 Display Recommendations
```

---

## 🧩 Flask Application

The core app lives in `app.py`:

```python
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    selected_movie = request.form.get("selected_movie", "").strip()
    recommendations = recommend(selected_movie)

    return render_template(
        "index.html",
        movie_list=movie_list,
        recommendations=recommendations,
        selected_movie=selected_movie
    )
```

---

## 🛡️ Error Handling

Both the poster-fetching and recommendation logic are wrapped in `try/except` blocks so a single failure never crashes the app:

```python
try:
    ...
except Exception as e:
    print("Recommendation Error:", e)
    return []
```

If the TMDB request fails, a placeholder poster is returned instead.

---

## ⚡ Performance

Similarity data is **precomputed once** and stored in `similarity.pkl`, loaded at application startup — avoiding expensive recalculation on every request and keeping recommendations fast.

---

## ☁️ Deployment (Render)

| Setting | Value |
|---|---|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Server** | Gunicorn (production WSGI) |

---

## 🌍 Live Links

<div align="center">

🚀 **[Live Application](https://movie-recommendation-system-r3e5.onrender.com/)**
&nbsp;&nbsp;|&nbsp;&nbsp;
💻 **[GitHub Repository](https://github.com/Mohit01112/movie-recommendation-system)**

</div>

---

## 🔮 Future Improvements

- ⭐ Add movie ratings
- 🎭 Genre-based filtering
- 🔍 Search functionality
- 🎬 Movie descriptions
- 👥 Actor & director information
- 🎞️ Movie trailers
- ❤️ User favorites
- 👤 User accounts
- 📊 Popularity metrics
- 🤝 Collaborative filtering
- 🧠 Hybrid recommendation system
- ⚡ TMDB response caching
- 🗃️ Replace Pickle with a database
- 📱 Improved responsive UI

---

## ⚠️ Limitations

- Recommendations depend entirely on the precomputed similarity data.
- `movie_list.pkl` and `similarity.pkl` are required for the app to run.
- Posters depend on TMDB API availability and internet access.
- The system does not currently factor in individual user ratings.
- Recommendation quality depends on the features used during model preparation.
- Pickle files may have compatibility issues across Python/library versions.

---

## 🎯 Learning Outcomes

Through this project, hands-on experience was gained in:

`Python` · `Flask` · `Recommendation Systems` · `Content-Based Filtering` · `Pandas` · `NumPy` · `Scikit-learn` · `Pickle Serialization` · `REST APIs` · `TMDB API` · `Environment Variables` · `Error Handling` · `Git & GitHub` · `Virtual Environments` · `Gunicorn` · `Cloud Deployment`

---


## 👨‍💻 Author

**Mohit**

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-Mohit01112-181717?logo=github&logoColor=white)](https://github.com/Mohit01112)

⭐ **If you found this project useful, consider giving it a star!** ⭐

</div>
