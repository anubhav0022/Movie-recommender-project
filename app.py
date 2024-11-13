import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    # Fetch the movie poster using TMDB API
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=de2bac42a54bd6b3a2fd3a87e602faea&language=en-US')
    data = response.json()
    # Return the image URL
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    # Get the index of the movie in the dataset
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    # Get the top 5 recommended movies based on cosine similarity
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []

    # Loop through the recommended movies list and fet ch title and poster
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']  # Assuming 'movie_id' is the correct column name
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# Load similarity matrix and movie data from pickle files
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pickle.load(open('movies.pkl', 'rb'))
movie_list = movies['title'].values

# Streamlit UI
st.title('Movie Recommender System')

# Dropdown to select a movie
selected_movie_name = st.selectbox("Choose a movie to get recommendations", movie_list)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    # Creating columns to display the recommended movies
    col1, col2, col3, col4, col5 = st.columns(5)  # Updated to 5 columns

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
