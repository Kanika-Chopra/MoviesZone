from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Create your views here.

def index(request):
    return render(request, "index-1.html")

def signup(request):
        return render(request, "signup.html")

def recommend(request):
    movies_data = pd.read_csv('rec_system\movies.csv')
    movies_data.head()

    # number of rows and columns in the data frame

    movies_data.shape

    # selecting the relevant features for recommendation

    selected_features = ['genres','keywords','tagline','cast','director']
    # print(selected_features)

    # replacing the null valuess with null string

    for feature in selected_features:
        movies_data[feature] = movies_data[feature].fillna('')
    
    # combining all the 5 selected features

    combined_features = movies_data['genres']+' '+movies_data['keywords']+' '+movies_data['tagline']+' '+movies_data['cast']+' '+movies_data['director']
    # print(combined_features)

    # converting the text data to feature vectors

    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    # print(feature_vectors)



    # getting the similarity scores using cosine similarity

    similarity = cosine_similarity(feature_vectors)
    # print(similarity)

    # getting the movie name from the user
    
         
    movie_name = request.GET.get('search')
    

    # creating a list with all the movie names given in the dataset

    list_of_all_titles = movies_data['title'].tolist()
    print(list_of_all_titles)

    # finding the close match for the movie name given by the user

    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    print(find_close_match)

    close_match = find_close_match[0]
    print(close_match)

    # finding the index of the movie with title

    index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
    print(index_of_the_movie)

    # getting a list of similar movies

    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    print(similarity_score)

    # sorting the movies based on their similarity score

    sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 
    print(sorted_similar_movies)


    # print the name of similar movies based on the index

    print('Movies suggested for you : \n')

    i = 1
    movies_list = []
    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index = movies_data[movies_data.index==index]['title'].values[0]
        if (i<31):
            movies_list.append(title_from_index)
            print(i, '.',title_from_index)
            i+=1
    print(movies_list)
    return render(request, "Recommend.html", {
        "movies_list": movies_list,
    })
