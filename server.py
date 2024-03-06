from fastapi import FastAPI, HTTPException, Query
import requests
import os
from dotenv import load_dotenv

app = FastAPI()

# Load variable dari file .env
load_dotenv()

@app.get("/movie")
async def get_movie_info(title: str = Query(None, description="Judul film yang ingin dicari"), genre: str = Query(None, description="Genre film yang ingin dicari"), popular: str = Query(False, description="Cari film yang sedang populer"), upcoming: str = Query(False, description="Cari film yang akan rilis")):
    try:
        # Ambil variable dari file .env
        omdb_apikey = os.getenv("OMDB_API_KEY")
        tmdb_apikey = os.getenv("TMDB_API_KEY")

        omdb_url = f"http://www.omdbapi.com/?t={title}&apikey={omdb_apikey}"

        # Jika mencari film yang populer
        if popular:
            tmdb_url = "https://api.themoviedb.org/3/movie/popular"
            params = {
                "api_key": tmdb_apikey,
                "language": "en-US",
                "page": 1
            }
            response = requests.get(tmdb_url, params=params)
            response.raise_for_status()

            # Ambil judul film-film yang populer
            popular_movies = [movie.get('title') for movie in response.json().get('results', [])]

            return {"popular_movies": popular_movies}
        
        # Jika mencari film yang akan rilis
        if upcoming:
            tmdb_url = "https://api.themoviedb.org/3/movie/upcoming"
            params = {
                "api_key": tmdb_apikey,
                "language": "en-US",
                "sort_by": "release_date.asc",
                "page": 1
            }
            response = requests.get(tmdb_url, params=params)
            response.raise_for_status()

        # Jika ada genre yang diberikan, tambahkan ke URL
        if genre:
            omdb_url += f"&type={genre}"
        
        response = requests.get(omdb_url)
        response.raise_for_status()
        
        movie_data = response.json()
        
        # Menyimpan data yang diperlukan ke dalam variabel temp
        genre = movie_data.get('Genre')
        tahun_rilis = movie_data.get('Released')
        aktor = movie_data.get('Actors')
        
        temp = {
            "genre": genre,
            "tahun_rilis": tahun_rilis,
            "aktor": aktor
        }
        
        return temp
    except requests.HTTPError as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)