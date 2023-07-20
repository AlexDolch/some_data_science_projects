import pandas as pd
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('./data/movies.csv')
ratings = pd.read_csv('./data/ratings.csv')
movies_ratings = pd.pivot_table(data=ratings, values='rating', index='userId', columns='movieId')

genre_list = []
for genre in movies.genres:
    for item in genre.split('|'):
        genre_list.append(item)
genres = set(genre_list)

st.title('WBSFlix')
st.subheader('Welcome to our movie recommender')


def top_n_movies(movies=movies, ratings=ratings):
    n = 10
    
    movies_ratings = (pd.merge(movies, 
                        ratings.groupby('movieId').agg(total_rating=('rating','sum'),
                                                       avg_rating = ('rating','mean')), 
                        how='inner', 
                        on='movieId')
                      .sort_values(by='total_rating', ascending=False)
                      .drop(columns=['movieId', 'total_rating'])
                      .rename(columns={'genres':'Genre', 'avg_rating':'Rating'})
                      .set_index('title')
                      # [['title', 'genres', 'avg_rating']]
                      .rename_axis(index='Title'))
    
    movies_ratings1 = (movies_ratings.head(n)
                       .style.format({'Rating':'{:.2f}'})
                       )


    st.dataframe(movies_ratings1,
            use_container_width=True)
    
    if st.button("Want to see more?", key=111):
        movies_ratings2 = (movies_ratings.iloc[11:21]
                       .style.format({'avg_rating':'{:.2f}'}).hide(axis='index')
                       )
        st.dataframe(movies_ratings2,
            use_container_width=True)
    else:
        pass
    


def top_genre_movies(style, genres=genres, movies=movies, ratings=ratings):
    n = 10
    
    movies_ratings = (pd.merge(movies, 
                        ratings.groupby('movieId').agg(total_rating=('rating','sum'),
                                                       avg_rating = ('rating','mean')), 
                        how='inner', 
                        on='movieId')
                      .query(f'genres.str.contains("{style}")')
                      .sort_values(by='total_rating', ascending=False)
                      .drop(columns=['movieId', 'total_rating'])
                      .rename(columns={'genres':'Genre', 'avg_rating':'Rating'})
                      .set_index('title')
                      )
   
    movies_ratings1 = (movies_ratings 
                      .head(n)
                      .style.format({'Rating':'{:.2f}'})
                      )
           
    st.dataframe(movies_ratings1,
                 use_container_width=True)
                  
    if st.button("Want to see more?", key=222):
        movies_ratings2 = (movies_ratings.iloc[11:21]
                           .style.format({'Rating':'{:.2f}'})
                           )
        st.dataframe(movies_ratings2,
            use_container_width=True)
    else:
        pass
    


def movie_item_similarity(match, movies=movies, ratings=ratings, movies_ratings=movies_ratings):
    # st.write(movies_ratings.head())
    st.write(match)
    n=10
    try:
        based_on = movies.loc[movies.title.str.contains(match, case=False)].movieId.iloc[0]
        flavored = movies.loc[movies.title.str.contains(match, case=False)].genres.iloc[0].split('|')
        rated = list(movies_ratings[based_on].dropna().index)
        
        n_minimum=10
        correlation = pd.DataFrame()
        while len(correlation) < n:
            correlation = pd.DataFrame({'PearsonR': movies_ratings.loc[rated].dropna(axis=1, how='all').corr(min_periods=n_minimum)[based_on]}).dropna().drop(based_on)
            n_minimum -= 2
            
        correlation = (
                       pd.merge(
                                correlation, 
                                ratings.groupby('movieId')
                                .agg(avg_rating=('rating','mean'), num_ratings=('rating','count')), 
                                how='left', on='movieId'
                                )
                         .query('num_ratings >= 10')
                      )

        correlation = (
                       pd.merge(
                                correlation,
                                movies,
                                on='movieId',
                                how='left'
                                )
                        )
        
        genre_points = []
        for movie in correlation.iterrows():
            i = 0
            for genre in (movie[1]['genres'].split('|')):
                if genre in flavored:
                    i += 1
            genre_points.append(i/10)
        correlation['genre_points'] = genre_points
        correlation = correlation.assign(genre_adjusted = lambda x: x.PearsonR + x.genre_points)
        correlation = (correlation
                       .sort_values(by='genre_adjusted', ascending=False)
                       .rename(columns={'genres':'Genre', 'avg_rating':'Rating'})
                       .set_index('title')
                       [['Genre', 'Rating']]
                       .head(n)
                       .style.format({'Rating':'{:.2f}'})
                      )
        st.dataframe(correlation,
                     use_container_width=True)
    except:
        st.write('Sorry, try another title.')



def movie_user_similarity(user, movies=movies, ratings=ratings, movies_ratings=movies_ratings):
    n = 10

    try:
        similarities = pd.DataFrame(cosine_similarity(movies_ratings.fillna(0)),
                                columns=movies_ratings.index, index=movies_ratings.index)
        weights = similarities[user].drop(user)/sum(similarities[user].drop(user))
        unrated = movies_ratings.loc[user].isna()
        weighted = movies_ratings.loc[:, unrated].fillna(0).drop(user).T.dot(weights)
        top_movies = movies.set_index('movieId')
        top_movies['rating'] = weighted

        top_movies = (
                           pd.merge(
                                    top_movies, 
                                    ratings.groupby('movieId')
                                    .agg(avg_rating=('rating','mean'), num_ratings=('rating','count')), 
                                    how='left', on='movieId'
                                    )
                             .query('num_ratings >= 10')
                             .sort_values(by='rating', ascending=False)
                          )
        top_movies1 = (top_movies
                       .rename(columns={'genres':'Genre', 'avg_rating':'Rating'})
                       .set_index('title')
                       [['Genre', 'Rating']]#, 'num_ratings']]
                       .head(n)
                       .style.format({'Rating':'{:.2f}'})
                       )

        st.dataframe(top_movies1,
                     use_container_width=True)
    except:
        st.write("Sorry, we can't find your user number.")




def secret_stash(movies=movies, ratings=ratings):
    movies_ratings = pd.merge(movies, 
                        ratings.groupby('movieId').agg(avg_rating = ('rating','mean'), num_ratings=('rating','count')), 
                        how='inner', 
                        on='movieId')
    movies_ratings = (movies_ratings
            .query('num_ratings < 10')
            .sort_values(by='avg_rating', ascending=False)
            .drop(columns=['movieId', 'num_ratings'])
            .rename(columns={'genres':'Genre', 'avg_rating':'Rating'})
            .set_index('title')
            .head(15)
            .sample()
            .style.format({'Rating':'{:.2f}'})
            )
    return st.dataframe(movies_ratings,
            use_container_width=True)



Recom = st.radio("Do you want movie recommendation for a specific genre?", 
    ('Blank','Yes', 'No'))

if Recom == 'No':
    st.write('You decided to consider all genres')
    top_n_movies()
elif Recom == 'Yes':
    style = st.selectbox('Select the genre you want from the list',genres)
    top_genre_movies(style)
else:
    st.write('You have not selected any option')



st.write("Want to capture the feel of a certain movie?")
movie = st.text_input("Enter a title here", value=None)
if movie != 'None':
    movie_item_similarity(movie)
    
st.write("Want to see what users like you have enjoyed?")
user = int(st.text_input("Enter your user number here", value=None))
if user != 'None':
    movie_user_similarity(user)
         
if st.button("Or try something from our secret stash!", key=200):
    secret_stash()

