import requests
import pandas as pd

def getMovieURL(movie_id, api_key):
    return "https://api.themoviedb.org/3/movie/"+movie_id+"?api_key="+api_key+"&language=en-US"

def getCreditsURL(movie_id, api_key):
    return "https://api.themoviedb.org/3/movie/"+movie_id+"/credits?api_key="+api_key+"&language=en-US"

def getPersonURL(person_id, api_key):
    return "https://api.themoviedb.org/3/person/"+person_id+"?api_key="+api_key+"&language=en-US"

def getPersonMoviesURL(person_id, api_key):
    return "https://api.themoviedb.org/3/person/"+person_id+"/movie_credits?api_key="+api_key+"&language=en-US"


api_key = input('Enter your TMDB API Key: ')
movie_id = '24428'

#movie_attributes = ['adult', 'backdrop_path', 'budget', 'id', 'popularity', 'poster_path', 'release_date', 'revenue', 'runtime', 'status', 'title', 'vote_average']
movie_attributes = ['adult', 'backdrop_path', 'id', 'popularity', 'poster_path', 'release_date', 'title', 'vote_average']
cast_attributes = ['character', 'gender', 'id', 'name', 'profile_path']
cast_additional_attributes = ['id', 'birthday', 'deathday', 'popularity', 'place_of_birth']

movie_details = requests.get(getMovieURL(movie_id, api_key)).json()
movie_df = pd.DataFrame([movie_details], columns=movie_attributes)
#print(movie_df)

movie_cast_details = requests.get(getCreditsURL(movie_id, api_key)).json()['cast']
movie_cast_df = pd.DataFrame(movie_cast_details, columns=cast_attributes)
#print(movie_cast_df)

cast_additional_data = list()
cast_other_movies_data = list()
for cast_id in movie_cast_df['id']:
    person_details = requests.get(getPersonURL(str(cast_id), api_key)).json()
    cast_additional_data.append(person_details)
    #print(person_details)
    other_movies = requests.get(getPersonMoviesURL(str(cast_id), api_key)).json()['cast']
    cast_other_movies_data.extend(other_movies)
    break

#person_df = pd.DataFrame(cast_additional_data, columns=cast_additional_attributes)
#print(person_df)
cast_other_movies_df = pd.DataFrame(cast_other_movies_data, columns=movie_attributes)
print(cast_other_movies_df)