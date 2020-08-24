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
movie_id = input('Enter movie ID: ')

movie_attributes = ['adult', 'backdrop_path', 'budget', 'id', 'popularity', 'poster_path', 'release_date', 'revenue', 'runtime', 'status', 'title', 'vote_average']
cast_attributes = ['id', 'character', 'name', 'gender', 'birthday', 'deathday', 'popularity', 'place_of_birth', 'profile_path']

movie_details = requests.get(getMovieURL(movie_id, api_key)).json()
movie_df = pd.DataFrame([movie_details], columns=movie_attributes)
movie_df.to_csv('movie.csv', index=False)

mapping = list()
movie_casts = requests.get(getCreditsURL(movie_id, api_key)).json()['cast']
for cast in movie_casts:
    cast_id = str(cast['id'])
    cast_details = requests.get(getPersonURL(cast_id, api_key)).json()
    for attr in cast_attributes:
        if attr in cast:
            continue
        cast[attr] = cast_details[attr]
    other_movies = requests.get(getPersonMoviesURL(cast_id, api_key)).json()['cast']
    for movie in other_movies:
        other_movie_id = str(movie['id'])
        if movie_id == other_movie_id:
            continue
        a_map = {"cast_id": cast_id, "other_movie_id": other_movie_id}
        mapping.append(a_map)

movie_casts_df = pd.DataFrame(movie_casts, columns=cast_attributes)
movie_casts_df.to_csv('cast.csv', index=False)

mapping_df = pd.DataFrame(mapping, columns=['cast_id', 'other_movie_id'])
mapping_df.to_csv('mapping.csv', index=False)

all_other_movie_ids = set(movie_id for a_map in mapping for movie_id in a_map.values())
print(len(all_other_movie_ids))
all_other_movie_details = list()
for other_movie_id in all_other_movie_ids:
    other_movie_details = requests.get(getMovieURL(other_movie_id, api_key)).json()
    all_other_movie_details.append(other_movie_details)
other_movies_df = pd.DataFrame(all_other_movie_details, columns=movie_attributes)
other_movies_df.to_csv('other_movies.csv', index=False)
