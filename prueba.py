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
            Tags = {}
            for row in reader:
                idMovie = row[0]
                tag = row[1]
                if tag in Tags:
                    dic = Tags[tag]
                    if idMovie in dic:
                        dic[idMovie] = dic[idMovie] + 1
                    else:
                        dic[idMovie] = 1
                    Tags[tag] = dic
                else:
                    dic = {}
                    dic[idMovie] = 1
                    Tags[tag] = dic

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

    print(t['Action'])

    print("¡Adios, mundo!")


if __name__ == "__main__":
    main()
