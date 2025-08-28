# import movies
import streamlit as st
from click import option

import pickle
import pandas as pd
import requests

import os
import gdown

API_KEY = "c66ec16a34d3689c86820c72fc7a22ec"


# from pandas.io.formats.format import return_docstring
# from select import select

def download_file_from_google_drive(url, output):
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# def fetch_poster(movie_id):
#     try:
#         url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
#         response = requests.get(url, timeout=5)
#         response.raise_for_status()
#         data = response.json()
#         return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', "")
#     except Exception as e:
#         print("Error fetching poster:", e)
#         return "https://via.placeholder.com/300x450?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for j in movies_list:
        movie_id = movies.iloc[j[0]].movie_id

        recommended_movies.append(movies.iloc[j[0]].title)

    #  fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters

try:
    with open("movie_dict.pkl", "rb") as f:
        movies_dict = pickle.load(f)
    movies = pd.DataFrame(movies_dict)
except Exception as e:
    st.error(f"Error loading movie_dict.pkl: {e}")
    movies = pd.DataFrame()  # fallback
SIMILARITY_ID = "PUT_SIMILARITY_FILE_ID_HERE"

# Download similarity.pkl from Drive
SIMILARITY_ID = "1AbCdEfGhIjKlMnOpQrStUvWxYz"
download_file_from_drive(SIMILARITY_ID, "similarity.pkl")
similarity = pickle.load(open("similarity.pkl", "rb"))


st.title('Movie Recommender System')


selected_movie_name = st.selectbox(
'How would you like to be contacted ?',
movies['title'].values
)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    # for i in recommendations:
    #     st.write(i)
    # col1, col2, col3, col4, col5 =st.beta_columns(5)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col1:
        st.text(names[1])
        st.image(posters[1])
    with col1:
        st.text(names[2])
        st.image(posters[2])
    with col1:
        st.text(names[3])
        st.image(posters[3])
    with col1:
        st.text(names[4])
        st.image(posters[4])



