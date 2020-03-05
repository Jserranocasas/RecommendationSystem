from Rating import Rating
from Movie import Movie
from User import User
from Tag import Tag

import Constants as kt
import csv


def ReaderCSV(csvPath):
    """
    Read a csv file and save the content in the corresponding objects
    """

    with open(csvPath, newline='', errors = "ignore") as File:
        reader = csv.reader(File)

        """ Parse the movies of csv """
        if(csvPath == kt.CSV_MOVIES):
            Movies = {}
            for row in reader:
                posStartBracket = row[1].find("(")
                posEndBracket = row[1].find(")")
                title = row[1][0:posStartBracket-1]
                year = row[1][posStartBracket+1:posEndBracket]

                Movies[row[0]] = Movie(row[0], title, year)

            return Movies

        """ Parse the tags of csv """
        if(csvPath == kt.CSV_TAG):
            Tags = []
            for row in reader:
                Tags.append( Tag(row[0], row[1]))

            return Tags

        """ Parse the users of csv """
        if(csvPath == kt.CSV_USER):
            Users = {}
            for row in reader:
                Users[row[0]] = User(row[0], row[1])

            return Users

        """ Parse the ratings of csv """
        if(csvPath == kt.CSV_RATING):
            Ratings = {}
            for row in reader:
                idTag = row[0] + "-" + row[1]
                Ratings[idTag] = Rating(idTag, row[0], row[1], row[2])

            return Ratings


def main():
    print("¡Hola, mundo!")

    m = ReaderCSV(kt.CSV_MOVIES)
    u = ReaderCSV(kt.CSV_USER)
    r = ReaderCSV(kt.CSV_RATING)
    t = ReaderCSV(kt.CSV_TAG)

    print("Movie 11 --> " + m['11'].title)
    print("User 1000 --> " + u['1000'].description)
    print("Rating 1 --> " + r['1-809'].value)
    print("Tag 0 --> " + t[0].description)

    print("¡Adios, mundo!")


if __name__ == "__main__":
    main()
