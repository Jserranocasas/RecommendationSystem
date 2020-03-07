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

        tags = {}
        tagsItems = {}
        for row in reader:
            idTag = row[0] + "-" + row[1]

            if idTag in tags:
                tags[idTag].incrementCount()
            else:
                tags[idTag] = Tag(row[0], row[1])

            idMovie, tag = row[0], row[1]
            if tag in tagsItems:
                dic = tagsItems[tag]
                if idMovie in dic:
                    dic[idMovie] = dic[idMovie] + 1
                else:
                    dic[idMovie] = 1
                tagsItems[tag] = dic
            else:
                dic = {}
                dic[idMovie] = 1
                tagsItems[tag] = dic

        dataItemTags = list(tagsItems.items())
        tagsItems = np.array(dataItemTags)

        return tags, tagsItems


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
        ratings = {}
        for row in reader:
            idTag = row[0] + "-" + row[1]
            ratings[idTag] = Rating(row[0], row[1], float(row[2]))

        return ratings


def CreateItemProfiles(movies, tags, tagsItems):
    """
    Create item profiles for technique TF-IDF
    @param: movies Movies
    @param: tags Tags
    @param: tagsItems
    """

    high, width = len(movies), len(tagsItems)
    moviesProfiles = [[0.0 for j in range(width)] for i in range(high)]

    i, j = 0, 0
    summationItemProfile = 0.0
    for movie in movies:
        for tagItem in tagsItems:
            existTag = movie.id + "-" + tagItem[0]

            if existTag in tags:
                invDocFrequency = math.log10(high / len(tagItem[1]))  # TODO
                itemProfile = tags[existTag].count * invDocFrequency
                moviesProfiles[i][j] = itemProfile
                summationItemProfile += itemProfile * itemProfile

            j += 1
        j = 0
        i += 1

    summationItemProfile = math.sqrt(summationItemProfile)

    for i in range(len(moviesProfiles)):
        for j in range(len(moviesProfiles[i])):
            moviesProfiles[i][j] /= summationItemProfile

    return moviesProfiles


def CreateUserProfiles(itemProfile, user, movies, tags, tagsItems, ratings):
    """
    Create user profile for technique TF-IDF
    @param: itemProfile Matrix
    @param: users User    
    @param: movies Movies
    @param: tags Tags
    @param: tagsItems
    @param: ratings
    """
    high, width = len(movies), len(tagsItems)

    userMatrix = [[0.0 for j in range(width)] for i in range(high)]

    i, j = 0, 0
    numberRatings = 0
    averageRating = 0.0

    for movie in movies:
        existRating = user + "-" + movie.id
        rating = ratings.get(existRating, Rating(0, 0, 0.0)).value

        for j in range(width):

            if rating != 0.0:
                numberRatings += 1
                averageRating += rating
                userMatrix[i][j] = rating  # Keep r now for greater efficiency

        i += 1

    averageRating /= numberRatings

    userProfile = [0.0 for j in range(width)]
    for i in range(len(userMatrix)):
        for j in range(len(userMatrix[i])):
            userMatrix[i][j] -= averageRating
            userMatrix[i][j] *= itemProfile[i][j]
            userProfile[j] += userMatrix[i][j]

    return userProfile


def CalculateSimilarity(userProfile, itemProfile):
    """
    Calculate similarity through the cosine function of the two vectors
    @param: userProfile Vector
    @param: itemProfile Vector  
    """

    summationUser = 0.0
    summationItem = 0.0
    summationUI = 0.0
    

    for i in range(len(userProfile)):
        summationUser += userProfile[i] * userProfile[i]
        summationItem += itemProfile[i] * itemProfile[i]
        summationUI += userProfile[i] * itemProfile[i]

    return summationUI / (math.sqrt(summationUser) * math.sqrt(summationItem))

def main():
    print("¡Hola, mundo!")

    user = "1"
    tags, tagsItems = ReaderCSVTag()
    movies, ratings = ReaderCSVMovies(), ReaderCSVRating()

    itemProfile = CreateItemProfiles(movies, tags, tagsItems)
    userProfile = CreateUserProfiles(
        itemProfile, user, movies, tags, tagsItems, ratings)

    print(CalculateSimilarity(userProfile, itemProfile[0]))

    print("¡Adiós, mundo cruel!")


if __name__ == "__main__":
    main()
