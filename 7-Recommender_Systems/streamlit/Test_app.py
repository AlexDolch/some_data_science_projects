import streamlit as st
import pandas as pd
import seaborn as sns


movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

genre_list = []
for genre in movies.genres:
    for item in genre.split('|'):
        genre_list.append(item)
genres = set(genre_list)

def top_n_movies(movies=movies, ratings=ratings):
    try:
        n = number
    except:
        n = 10
    movies_ratings = pd.merge(movies, 
                        ratings.groupby('movieId').agg(total_rating=('rating','sum'),
                                                       avg_rating = ('rating','mean')), 
                        how='inner', 
                        on='movieId')
    movies_ratings['avg_rating'] = movies_ratings.avg_rating.apply(lambda x: round(x, 2))
    
    return (movies_ratings.sort_values(by='total_rating', ascending=False)
            .drop(columns=['movieId', 'total_rating'])
            .set_index('title')
            .head(n).style.format({'avg_rating':'{:.2f}'}))

def top_genre_movies(movies=movies, ratings=ratings):
    genre_list = []
    for genre in movies.genres:
        for item in genre.split('|'):
            genre_list.append(item)
    genres = set(genre_list)
    style = Genre_y 
    #style = input("What's your genre?\nIf you'd like a list of genres, type '?'  ").strip().title()
    # print(style, type(style))
    # print(style == '?')
    #while True:
        #if style == '?':
            #print(genres)
            #style = input("What's your genre?  ").strip().title()
            #continue
        #elif style not in genres:
            #style = input(f"{style} is not a valid genre.\nIf you'd like a list of genres, type '?'  ").strip().title()
            #continue
        #else:
            #style = Genre_y 
            #break
    #try:
     #   n = int(input('How many movies?  '))
      #  if n <= 0:
       #     n = 1
    #except:
    n = number
    movies_ratings = pd.merge(movies, 
                        ratings.groupby('movieId').agg(total_rating=('rating','sum'),
                                                       avg_rating = ('rating','mean')), 
                        how='inner', 
                        on='movieId')
    movies_ratings['avg_rating'] = movies_ratings.avg_rating.apply(lambda x: round(x, 2))
    return (movies_ratings
            .query(f'genres.str.contains("{style}")')
            .sort_values(by='total_rating', ascending=False)
            .drop(columns=['movieId', 'total_rating'])
            .set_index('title')
            .head(n).style.format({'avg_rating':'{:.2f}'}))



st.image('movies-tiles2.JPG')
st.title("WBSFlix")

st.subheader('Welcome to our movie recommender')
st.markdown(
    """ <style>
            div[role="radiogroup"] >  :first-child{
                display: none !important;
            }
        </style>  
        """,
    unsafe_allow_html=True
)

Recom = st.radio("Do you want movie recommendation for a specific genre?", 
    ('Blank','Yes', 'No'))

if Recom == 'No':
    st.write('You decided to consider all genres')
    number = st.number_input('Instert number of movies would you like to consider',min_value=1, max_value=10) 
    st.dataframe(top_n_movies())
else:
    if Recom == 'Yes':
        Genre_y = st.selectbox('Select the genre you want from the list',(genres))
        number = st.number_input('Instert number of movies would you like to consider',min_value=1, max_value=10) 
        #st.button('Submit')
        st.dataframe(top_genre_movies())
    else:
        st.write('You have not selected any option')




