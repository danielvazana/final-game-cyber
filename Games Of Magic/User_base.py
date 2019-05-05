class User(object):
    """
    A user object that helps the server maintain user information.
    The object contains user information: name, password, score and number of wins.
    """
    def __init__(self, name, password, score=0, winnings=0):
        self.name = name  # User's name
        self.password = password  # User's password
        self.score = score  # The current points of the user
        self.winnings = winnings  # The number of the winnings that the user had
