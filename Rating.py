class Rating:
    """
    Class that represent a rating
    """

    def __init__(self, idUser, idMovie, value):
        """ Rating Class Constructor """
        self.idUser = idUser
        self.idMovie = idMovie
        self.value = value
