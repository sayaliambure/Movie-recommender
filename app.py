import streamlit as st
import pickle
import pandas as pd
import requests
import os
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
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


def save_feedback(movie, feedback):
    if not os.path.exists('feedback.csv') or os.stat('feedback.csv').st_size == 0:
        feedback_df = pd.DataFrame(columns=['movie', 'feedback'])
    else:
        feedback_df = pd.read_csv('feedback.csv')

    new_feedback = pd.DataFrame({'movie': [movie], 'feedback': [feedback]})
    feedback_df = pd.concat([feedback_df, new_feedback], ignore_index=True)
    feedback_df.to_csv('feedback.csv', index=False)



def generate_feedback_chart():
    if os.path.exists('feedback.csv') and os.stat('feedback.csv').st_size != 0:
        feedback_df = pd.read_csv('feedback.csv')
        try:
            # Pie Chart
            feedback_counts = feedback_df['feedback'].value_counts().sort_index()
            fig, ax = plt.subplots(figsize=(6, 6))
            colors = sns.color_palette('pastel')[0:5]
            ax.pie(feedback_counts, labels=feedback_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')
            st.pyplot(fig)

            # Bar Chart
            st.write("### Feedback Distribution")
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(x=feedback_counts.index, y=feedback_counts.values, palette='viridis', ax=ax)
            ax.set_xlabel('Rating')
            ax.set_ylabel('Count')
            st.pyplot(fig)

            # Histogram
            st.write("### Feedback Histogram")
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.histplot(feedback_df['feedback'], bins=5, kde=True, color='skyblue', ax=ax)
            ax.set_xlabel('Rating')
            ax.set_ylabel('Frequency')
            st.pyplot(fig)

            # Word Cloud
            st.write("### Recommended Movies Word Cloud")
            text = ' '.join(feedback_df['movie'])
            wordcloud = WordCloud(width=600, height=300, background_color='white').generate(text)
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

            # Top N Movies
            st.write("### Top 5 Movies Based on Feedback")
            top_movies = feedback_df.groupby('movie')['feedback'].mean().sort_values(ascending=False).head(5)
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(x=top_movies.values, y=top_movies.index, palette='coolwarm', ax=ax)
            ax.set_xlabel('Average Rating')
            ax.set_ylabel('Movie')
            st.pyplot(fig)


        except pd.errors.EmptyDataError:
            st.write("No feedback data available.")
      
    else:
        st.write("No feedback data available.")


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies_list = movies_list['title'].values
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

if 'recommendations' not in st.session_state:
    st.session_state['recommendations'] = None

selected_movie_name = st.selectbox(
  'Which movie would you like to search!?',
  movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    # names = recommend(selected_movie_name)
    st.session_state['recommendations'] = (names, posters)

if st.session_state['recommendations']:
    names, posters = st.session_state['recommendations']

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


    st.text(" ")
    st.text(" ")
    st.text(" ")

    # Feedback Submission
    feedback = st.slider('How satisfied are you with these recommendations?', 1, 5, 3)
    if st.button('Submit Feedback'):
        save_feedback(selected_movie_name, feedback)
        st.success('Thank you for your feedback!')


    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.text(" ")


st.markdown("""<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

st.text(" ")
st.text(" ")
st.text(" ")
# User Feedback Section
lable = '<p style="font-size:28px; font-weight:bold">User Feedback</p>'
st.markdown(lable, unsafe_allow_html=True)

# View Feedback Chart
if st.button('View Feedback Summary'):
    generate_feedback_chart()