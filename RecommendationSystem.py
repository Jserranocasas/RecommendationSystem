from Rating import Rating
from Movie import Movie
from User import User
from Tag import Tag

import Constants as kt
import numpy as np
import math
import csv


def ReaderCSVMovies():
    """
    Read a csv file to save the content corresponding to the movies
    @return: a array with the movies 
    """

    with open(kt.CSV_MOVIES, newline='') as File:
        reader = csv.reader(File)
        movies = []
        for row in reader:
            movies.append(Movie(row[0], row[1]))

        return movies


def ReaderCSVTag():
    """
    Read a csv file to save the content corresponding to the tags
    @return: a dictionary with the tags and a array with the items what have the tags
    """

    with open(kt.CSV_TAG, newline='', errors="ignore") as File:
        reader = csv.reader(File)

        dicTags = {}
        for row in reader:
            idMovie, tag = row[0], row[1]
            if tag in dicTags:
                dic = dicTags[tag]
                if idMovie in dic:
                    dic[idMovie] = dic[idMovie] + 1
                else:
                    dic[idMovie] = 1
                dicTags[tag] = dic
            else:
                dic = {}
                dic[idMovie] = 1
                dicTags[tag] = dic

        return dicTags, list(dicTags.keys())


def ReaderCSVUser():
    """
    Read a csv file to save the content corresponding to the users
    @return: a dictionary with the users 
    """
    with open(kt.CSV_USER, newline='') as File:
        reader = csv.reader(File)
        users = {}
        for row in reader:
            users[row[0]] = User(row[0], row[1])

        return users


def ReaderCSVRating():
    """
    Read a csv file and save the content in the corresponding objects
    @return: a dictionary with the rating of the movies rated by the user
    """

    with open(kt.CSV_RATING, newline='') as File:
        reader = csv.reader(File)

        dicRatings = {}
        for row in reader:
            idUser, idMovie, rating = int(row[0]), int(row[1]), float(row[2])
            if idUser in dicRatings:
                dic = dicRatings[idUser]
                dic[idMovie] = rating
                dicRatings[idUser] = dic
            else:
                dic = {}
                dic[idMovie] = rating
                dicRatings[idUser] = dic
        
        return dicRatings

def createItemProfiles(listMovies, dicTags, listTags):
    """
    Create item profiles for technique TF-IDF
    @param: listMovies movie list
    @param: dicTags tag dictionary with their occurance count
    @param: listTags tag list
    """

    itemsProfiles = np.zeros((len(listMovies), len(listTags)))
    
    iot = 0 #tag index
    for tag in listTags:
        occurance = dicTags[tag]

        for tuple in occurance.items():
            idMovie = tuple[0]
            iom = indexOfMovie(listMovies, idMovie) #movie index in list

            tf = tuple[1]
            idf = math.log10(len(listMovies)/len(occurance))

            itemsProfiles[iom][iot] = tf * idf
        
        iot += 1

    #Normalize array
    itemsProfilesNormalized = np.zeros(itemsProfiles.shape)
    i = 0
    for v in itemsProfiles:
        normalized = v / np.sqrt(np.sum(v**2))
        itemsProfilesNormalized[i] = normalized
        i+=1
    
    return itemsProfilesNormalized

def createUserProfile(user, itemProfiles, listMovies, dicRatings):
    """
    Create a user profile for technique TF-IDF
    @param user user to create the profile
    @param itemProfiles item profile for technique TF-IDF
    @param listMovies movie list
    @param dicTags tag dictionary
    @param listTags tag list
    @param dicRatings rating dictionary
    """
    userProfile = np.zeros((len(itemProfiles[0])))
    ratingByUser = dicRatings[user]
    averageRating = np.array(list(ratingByUser.values())).mean()

    for tuple in ratingByUser.items():
        iom = indexOfMovie(listMovies, tuple[0]) #movie index in list
        rating = tuple[1]

        w = rating - averageRating
        userProfile += (itemProfiles[iom] * w)

    return userProfile

def calculateSimilarity(user, userProfile, itemProfiles, listMovies, dicRatings):
    """
    Calculate the similiraty with the items that user has not rated
    @param user user id
    @param userProfile user profile
    @param itemProfiles item profiles
    @param listMovies movie list
    @param dicRating rating dictionary
    """
    ratingsByUser = dicRatings[user]

    #Items that user has not seen
    movieIds = []
    for movie in listMovies:
        if int(movie.id) not in ratingsByUser:
            movieIds.append(movie.id)

    similarity = []
    #Similarity with items
    for movieId in movieIds:
        iom = indexOfMovie(listMovies, movieId)
        itemProfile = itemProfiles[iom]
        cos = userProfile.dot(itemProfile) / (np.sqrt(userProfile.dot(userProfile)) * np.sqrt(itemProfile.dot(itemProfile)))
        similarity.append((listMovies[indexOfMovie(listMovies, movieId)].title, cos))

    #Sort by cos value
    similarity.sort(key=lambda tup: tup[1], reverse=True)

    return similarity

def indexOfMovie(listMovies, movieId):
    """
    Return the index of movie in the list, or -1 if not exits
    @param listMovies movie list
    @param movieId movie id to searh
    """
    index = 0

    for movie in listMovies:
        if int(movie.id) == int(movieId):
            return index
        index += 1
    
    return -1

def recommend(user, count):
    listMovies = ReaderCSVMovies()
    dicTags, listTags = ReaderCSVTag()
    dicRating = ReaderCSVRating()

    if user not in dicRating:
        raise ValueError("Not exist this user in database")
    
    itemProfiles = createItemProfiles(listMovies, dicTags, listTags)
    userProfile = createUserProfile(user, itemProfiles, listMovies, dicRating)

    similarityItems = calculateSimilarity(user, userProfile, itemProfiles, listMovies, dicRating)

    if len(similarityItems) < count:
        return similarityItems
    else:
        v = []
        for i in range(count):
            v.append(similarityItems[i])
        return v
