import streamlit as st
import pickle
import pandas as pd
import requests

# API key: 8265bd1679663a7ea12ac168da84d2e8


def fetch_poster(movie_id):
  response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
  data = response.json()
  return "http://image.tmdb.org/t/p/w500/" + data['poster_path']



def recommend(movie):
  movie_index = movies[movies['title'] == movie].index[0]
  distances = similarity[movie_index]
  movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1]) [1:4]

  recommended_movies = []
  recommended_movies_posters = []
  for i in movie_list:
      movie_id = movies.iloc[i[0]].movie_id
      recommended_movies.append(movies.iloc[i[0]].title)
      # fetch poster from API      
      recommended_movies_posters.append(fetch_poster(movie_id))

  return recommended_movies, recommended_movies_posters
  # return recommended_movies


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies_list = movies_list['title'].values
movies = pd.DataFrame(movies_dict)


similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
  'Which movie would you like to search!?',
  movies['title'].values
)

if st.button('Recommend'):
  names, posters = recommend(selected_movie_name)
  # names = recommend(selected_movie_name)

  st.text(" ")
  st.text("Movies you should watch😉👇✨")
  st.text(" ")


  for i in names:
    st.write("✔️" ,i)

  st.text(" ")
  st.text(" ")
  st.text(" ")

  col1, col2, col3 = st.columns(3)
  with col1:
    st.text(names[0])
    st.image(posters[0])
  with col2:
    st.text(names[1])
    st.image(posters[1])
  with col3:
    st.text(names[2])
    st.image(posters[2])
  # with col4:
  #   st.text(names[3])
  #   st.image(posters[3])
  # with col5:
  #   st.text(names[4])
  #   st.image(posters[4])