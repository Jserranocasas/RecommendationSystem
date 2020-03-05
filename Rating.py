class Rating:
    """
    Class that represent a rating
    """

    def __init__(self, idRating, idUser, idMovie, value):
        """ Rating Class Constructor """
        self.idRating = idRating
        self.idUser = idUser
        self.idMovie = idMovie
        self.value = value
