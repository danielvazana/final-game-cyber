class Tournament(object):
    """
    A tournament object that contains the participants' sockets, a player dictionary containing their opponent,
    a second round list, and more.
    """
    def __init__(self, socket1, socket2, socket3, socket4):
        self.points = 0  # The total points the the winner will earn
        self.round = 1
        self.team_1 = (socket1, socket2)
        self.team_2 = (socket3, socket4)
        self.final = []  # The winners of the first round and the players of the second round
        self.dict_has_other_player = {socket1: socket2, socket2: socket1, socket3: socket4, socket4: socket3}
        self.dict_user_has_tuple = {socket1: (socket1, socket2), socket2: (socket1, socket2),
                                    socket3: (socket3, socket4), socket4: (socket3, socket4)}

    def new_winner(self, socket_won):
        self.final.append(socket_won)
        if len(self.final) == 2:
            self.round = 2
            del self.dict_user_has_tuple[self.dict_has_other_player[self.final[0]]]
            del self.dict_user_has_tuple[self.dict_has_other_player[self.final[1]]]
            self.dict_user_has_tuple = {}
            del self.dict_has_other_player[self.dict_has_other_player[self.final[0]]]
            del self.dict_has_other_player[self.dict_has_other_player[self.final[1]]]
            self.dict_has_other_player = {}
            self.dict_has_other_player.update({self.final[0]: self.final[1]})
            self.dict_has_other_player.update({self.final[1]: self.final[0]})
            self.dict_user_has_tuple.update({self.final[0]: (self.final[0], self.final[1])})
            self.dict_user_has_tuple.update({self.final[1]: (self.final[0], self.final[1])})
            return True
        else:
            return False

    def __str__(self):
        return 'Tournament , points :', str(self.points), ', round :', str(self.round)
