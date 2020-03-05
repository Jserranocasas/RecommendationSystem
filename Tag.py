class Tag:
    """
    Class that represent a tag
    """

    def __init__(self, idMovie, description):
        """ Tag Class Constructor """
        self.idMovie = idMovie
        self.description = description
        self.count = 1

    def addCount(self):
        self.count += 1
