class User(object):

    def __init__(self, name, password, score=0, winnings=0):
        self.name = name  # User's name
        self.password = password  # User's password
        self.score = score  # The current points of the user
        self.winnings = winnings  # The number of the winnings that the user had
