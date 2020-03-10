from Rating import Rating
from Movie import Movie
from User import User
from Tag import Tag
from time import time

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
        movieIndex = 0
        for row in reader:
            movies.append(Movie(movieIndex, int(row[0]), row[1]))
            movieIndex += 1

        return movies


def ReaderCSVTag():
    """
    Read a csv file to save the content corresponding to the tags
    @return: a dictionary with tags. These save the items that have
    """

    with open(kt.CSV_TAG, newline='', errors="ignore") as File:
        reader = csv.reader(File)

        dicTags = {}
        for row in reader:
            movieId, tagKey = row[0], row[1]
            tag = dicTags.get(tagKey, {})

            if not tag:
                tag[movieId] = 1
                dicTags[tagKey] = tag
            else:
                movieWithTag = tag.get(movieId, {})
                if not movieWithTag:
                    tag[movieId] = 1
                else:
                    tag[movieId] += 1

        return dicTags


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
            userId, movieId, value = int(row[0]), int(row[1]), float(row[2])

            rating = dicRatings.get(userId, {})

            if not rating:
                rating[movieId] = value
                dicRatings[userId] = rating
            else:
                rating[movieId] = value
                dicRatings[userId] = rating

        return dicRatings


def createItemProfiles(listMovies, dicTags):
    """
    Create item profiles for technique TF-IDF
    @param: listMovies movie list
    @param: dicTags tag dictionary with their occurance count
    @param: listTags tag list
    @return: items Profiles Normalized
    """

    itemsProfiles = np.zeros((len(listMovies), len(dicTags.keys())))

    tagIndex = 0 
    for moviesWithTag in dicTags.values():
        for idMovie, termFrequency in moviesWithTag.items():
            movieIndex = indexOfMovie(listMovies, idMovie)  # movie index in list
            idf = math.log10(len(listMovies)/len(moviesWithTag))

            itemsProfiles[movieIndex][tagIndex] = termFrequency * idf

        tagIndex += 1

    # Normalize items profiles
    itemsProfilesNormalized = np.zeros(itemsProfiles.shape)
    i = 0
    for v in itemsProfiles:
        normalized = v / np.sqrt(np.sum(v*v))
        itemsProfilesNormalized[i] = normalized
        i += 1

    return itemsProfilesNormalized


def createUserProfile(user, itemProfiles, listMovies, dicRatings):
    """
    Create a user profile for technique TF-IDF
    @param user int Id to identify the user
    @param itemProfiles item profile for technique TF-IDF
    @param listMovies movie list
    @param dicTags tag dictionary
    @param listTags tag list
    @param dicRatings rating dictionary
    @return: user profile corresponding to user
    """
    userProfile = np.zeros((len(itemProfiles[0])))
    ratingByUser = dicRatings[user]
    averageRating = np.array(list(ratingByUser.values())).mean()

    for userRatings in ratingByUser.items():
        # Movie index in list
        movieIndex = indexOfMovie(listMovies, userRatings[0])  
        ratingValue = userRatings[1]

        w = ratingValue - averageRating
        userProfile += (itemProfiles[movieIndex] * w)

    return userProfile


def calculateSimilarity(user, userProfile, itemProfiles, listMovies, dicRatings):
    """
    Calculate the similiraty with the items that user has not rated through 
    the cosine function of the userProfile, itemProfiles vectors
    @param user int Id to identify the user
    @param userProfile User profile corresponding to rated movies
    @param itemProfiles Item profiles corresponding to assigned tags
    @param listMovies List with all available movies
    @param dicRatings Ratings dictionary with users ratings
    @return: A vector ordered by cosine function value what contain the 
    similarity between user profile and item profiles
    """

    ratingsByUser = dicRatings[user]

    # Items that user has not seen
    unseenMovies = []
    for movie in listMovies:
        if movie.id not in ratingsByUser:
            unseenMovies.append(movie)

    # Similarity with items
    similarity = []
    for movie in unseenMovies:
        itemProfile = itemProfiles[movie.index]
        cos = userProfile.dot(
            itemProfile) / (np.sqrt(userProfile.dot(userProfile)) * np.sqrt(itemProfile.dot(itemProfile)))

        similarity.append((movie, cos))

    # Sort by cos value
    similarity.sort(key=lambda tup: tup[1], reverse=True)

    return similarity


def indexOfMovie(listMovies, movieId):
    """
    Return the index of movie in the list, or -1 if not exits
    @param listMovies movie list
    @param movieId movie id to searh
    @return: movie index of the movie passed by parameter 
    """

    index = 0
    for movie in listMovies:
        if movie.id == int(movieId):
            return index
        index += 1

    return -1


def main():
    # Start counting.
    start_time = time()

    user = 500

    listMovies = ReaderCSVMovies()
    dicTags = ReaderCSVTag()
    dicRating = ReaderCSVRating()
    
    itemProfiles = createItemProfiles(listMovies, dicTags)
    userProfile = createUserProfile(user, itemProfiles, listMovies, dicRating)

    similarityItems = calculateSimilarity(
        user, userProfile, itemProfiles, listMovies, dicRating)

    for item in similarityItems:
        print("Pelicula: " + item[0].title + ". Afinidad: " + str(item[1]))

    # Calculate the elapsed time.
    elapsed_time = time() - start_time

    print("Elapsed time: %0.10f seconds." % elapsed_time)


if __name__ == "__main__":
    main()
