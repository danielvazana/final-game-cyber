import socket
import select
import datetime
from User_base import User
from Tournament_base import Tournament

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(2000000000)
open_client_sockets = []
messages_to_send = []
wait_for_game = []
send_start_game = []
dict_has_other_player = {}
dict_user_has_tuple = {}
sockets_to_quit = []
users_dict = {}
self_messages_to_send = []
wait_for_tournament = []
dict_has_tournament = {}


def send_waiting_messages(wait_list):
    list1 = messages_to_send[:]
    list2 = sockets_to_quit[:]
    list3 = send_start_game[:]
    list4 = self_messages_to_send[:]
    for message in list1:
        (client_socket, data_of_message) = message
        if client_socket in wait_list and client_socket in dict_has_other_player \
                and dict_has_other_player[client_socket] in wait_list:
            soket1, socket2 = dict_user_has_tuple[client_socket]
            soket1.send(data_of_message)
            socket2.send(data_of_message)
            messages_to_send.remove(message)
        elif client_socket in wait_list and client_socket in dict_has_tournament and \
                dict_has_tournament[client_socket].dict_has_other_player[client_socket] in wait_list:
            soket1, socket2 = dict_has_tournament[client_socket].dict_user_has_tuple[client_socket]
            soket1.send(data_of_message)
            socket2.send(data_of_message)
            messages_to_send.remove(message)
    for socket_quited in list2:
        if socket_quited in dict_has_other_player and dict_has_other_player[socket_quited] in wait_list:
            dict_has_other_player[socket_quited].send('finish')
            del dict_user_has_tuple[dict_has_other_player[socket_quited]]
            del dict_user_has_tuple[socket_quited]
            del dict_has_other_player[dict_has_other_player[socket_quited]]
            del dict_has_other_player[socket_quited]
            sockets_to_quit.remove(socket_quited)
        elif socket_quited in dict_has_tournament:
            if socket_quited in dict_has_tournament[socket_quited].dict_has_other_player and \
                    dict_has_tournament[socket_quited].dict_has_other_player[socket_quited] in wait_list:
                dict_has_tournament[socket_quited].dict_has_other_player[socket_quited].send('finish')
                del dict_has_tournament[socket_quited]
    for tuple_to_send in list3:
        socket1, socket2 = tuple_to_send
        if socket1 in wait_list and socket2 in wait_list:
            socket1.send('right;')
            socket2.send('left;')
            send_start_game.remove(tuple_to_send)
    for message_login in list4:
        (client_socket, data_of_message_login) = message_login
        if client_socket in wait_list:
            client_socket.send(data_of_message_login)
            self_messages_to_send.remove(message_login)
    del list1
    del list2
    del list3
    del list4


while True:
    read_list, write_list, x_list = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
    for current_socket in read_list:
        if current_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            open_client_sockets.append(new_socket)
        else:
            data = current_socket.recv(1024)
            if data == '':
                print open_client_sockets
                if current_socket in wait_for_game:
                    wait_for_game.remove(current_socket)
                if current_socket in wait_for_tournament:
                    wait_for_tournament.remove(current_socket)
                if current_socket in dict_has_other_player:
                    sockets_to_quit.append(current_socket)
                if current_socket in dict_has_tournament:
                    sockets_to_quit.append(current_socket)
            else:
                if 'get winning table' in data:
                    self_messages_to_send.append((current_socket, str(
                        sorted(users_dict, key=lambda v: users_dict[v].score, reverse=True)[:3])))
                elif 'add points and winning' in data:
                    name = data.split(';')[1]
                    password = data.split(';')[2]
                    points = data.split(';')[3]
                    if name in users_dict:
                        if users_dict[name].password == password:
                            users_dict[name].winnings += 1
                            users_dict[name].score += int(points)
                    if current_socket in dict_has_other_player:
                        del dict_has_other_player[dict_has_other_player[current_socket]]
                        del dict_has_other_player[current_socket]
                elif 'add points to tournament and winning;' in data:
                    if current_socket in dict_has_tournament and \
                            dict_has_tournament[current_socket].dict_has_other_player[
                                current_socket] in dict_has_tournament:
                        del dict_has_tournament[
                            dict_has_tournament[current_socket].dict_has_other_player[current_socket]]
                    name = data.split(';')[1]
                    password = data.split(';')[2]
                    points = data.split(';')[3]
                    if name in users_dict:
                        if users_dict[name].password == password:
                            users_dict[name].winnings += 1
                    dict_has_tournament[current_socket].points += int(points)
                    if dict_has_tournament[current_socket].round == 1:
                        new_game = dict_has_tournament[current_socket].new_winner(current_socket)
                        if new_game:
                            send_start_game.append((dict_has_tournament[current_socket].final[0],
                                                    dict_has_tournament[current_socket].final[1]))
                    else:
                        users_dict[name].score += dict_has_tournament[current_socket].points
                        del dict_has_tournament[current_socket]
                elif 'get score' in data:
                    name = data.split(';')[1]
                    password = data.split(';')[2]
                    if name in users_dict:
                        if users_dict[name].password == password:
                            self_messages_to_send.append(
                                (current_socket, str(users_dict[name].score) + ';' + str(users_dict[name].winnings)))
                elif 'login' in data:
                    name = data.split(';')[1]
                    password = data.split(';')[2]
                    if name in users_dict:
                        if users_dict[name].password == password:
                            self_messages_to_send.append((current_socket, 'ok'))
                        else:
                            self_messages_to_send.append((current_socket, 'Incorrect password'))
                    else:
                        self_messages_to_send.append((current_socket, 'There is no such user'))
                elif 'sign in' in data:
                    name = data.split(';')[1]
                    password = data.split(';')[2]
                    if name not in users_dict:
                        users_dict.update({name: User(name, password)})
                        self_messages_to_send.append((current_socket, 'ok'))
                    else:
                        self_messages_to_send.append((current_socket, 'Username already exists'))
                elif 'tournament' in data:
                    wait_for_tournament.append(current_socket)
                    if len(wait_for_tournament) == 4:
                        new_tournament = Tournament(wait_for_tournament[0], wait_for_tournament[1],
                                                    wait_for_tournament[2],
                                                    wait_for_tournament[3])
                        send_start_game.append(new_tournament.team_1)
                        send_start_game.append(new_tournament.team_2)
                        dict_has_tournament.update({wait_for_tournament[0]: new_tournament})
                        dict_has_tournament.update({wait_for_tournament[1]: new_tournament})
                        dict_has_tournament.update({wait_for_tournament[2]: new_tournament})
                        dict_has_tournament.update({wait_for_tournament[3]: new_tournament})
                        wait_for_tournament = []
                elif 'want-play' in data:
                    if len(wait_for_game) == 0:
                        wait_for_game.append(current_socket)
                    else:
                        send_start_game.append((wait_for_game[0], current_socket))
                        dict_has_other_player.update({current_socket: wait_for_game[0]})
                        dict_has_other_player.update({wait_for_game[0]: current_socket})
                        dict_user_has_tuple.update({current_socket: (wait_for_game[0], current_socket)})
                        dict_user_has_tuple.update({wait_for_game[0]: (wait_for_game[0], current_socket)})
                        wait_for_game.remove(wait_for_game[0])
                else:
                    messages_to_send.append((current_socket, data))

    send_waiting_messages(write_list)
