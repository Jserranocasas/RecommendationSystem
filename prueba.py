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
    Read a csv file and save the content in the corresponding objects
    """

    with open(kt.CSV_MOVIES, newline='') as File:
        reader = csv.reader(File)
        movies = []
        for row in reader:
            movies.append(Movie(row[0], row[1]))

        return movies


def ReaderCSVTag():
    """
    Read a csv file and save the content in the corresponding objects
    @return:
    """

    with open(kt.CSV_TAG, newline='', errors="ignore") as File:
        reader = csv.reader(File)

        tags = {}
        itemTags = {}
        for row in reader:
            idTag = row[0] + "-" + row[1]

            if idTag in tags:
                tags[idTag].incrementCount()
            else:
                tags[idTag] = Tag(row[0], row[1])

            idMovie, tag = row[0], row[1]
            if tag in itemTags:
                dic = itemTags[tag]
                if idMovie in dic:
                    dic[idMovie] = dic[idMovie] + 1
                else:
                    dic[idMovie] = 1
                itemTags[tag] = dic
            else:
                dic = {}
                dic[idMovie] = 1
                itemTags[tag] = dic

        dataItemTags = list(itemTags.items())
        itemTags = np.array(dataItemTags)

        return tags, itemTags


def ReaderCSVUser():
    """
    Read a csv file and save the content in the corresponding objects
    @return:
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
    @return:
    """

    with open(kt.CSV_RATING, newline='') as File:
        reader = csv.reader(File)
        ratings = {}
        for row in reader:
            idTag = row[0] + "-" + row[1]
            ratings[idTag] = Rating(row[0], row[1], row[2])

        return ratings


def CreateItemProfiles(movies, tags, itemTags):
    """
    Create item profiles for technique TF-IDF
    @param: movies Movies
    @param: tags Tags
    @param: itemTags
    """
    w, h = len(movies), len(itemTags)

    moviesProfiles = [[0 for j in range(h)] for i in range(w)]
    
    i, j = 0, 0
    summationItemProfile = 0
    for movie in movies:
        for itemT in itemTags:
            idTag = movie.id+"-"+itemT[0]
            
            if idTag in tags:
                idf = math.log10(w / len(itemT[1]))
                itemProfile = tags[idTag].count * idf
                moviesProfiles[i][j] = itemProfile
                summationItemProfile += itemProfile*itemProfile

            j+=1
        j=0
        i+=1

    summationItemProfile = math.sqrt(summationItemProfile)

    for i in range(len(moviesProfiles)):
        for j in range(len(moviesProfiles[i])):
            moviesProfiles[i][j] /=  summationItemProfile

    return moviesProfiles


def main():
    print("¡Hola, mundo!")

    tags, itemTags=ReaderCSVTag()
    itemProfile=CreateItemProfiles(
        ReaderCSVMovies(), tags, itemTags)

    print("¡Adiós, mundo cruel!")

if __name__ == "__main__":
    main()