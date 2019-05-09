import pygame
from math import sin, cos, pi
from math import atan2, pi
import math
import os
from Charachters import Medusa, Minotaur, Wizard, Skeleton
from Castle import Castle
from client_game import *
from datetime import datetime
from user_login import *


def menu_screen():
    pic = 'screens/menu_screen.png'
    screen_to_show = build_screen(1440, 759)
    run = True
    while run:
        run = not quit_pressed()
        screen_to_show.blit(pygame.image.load(pic), (0, 0))
        pygame.display.flip()
        (mouse_x, mouse_y) = mouse()
        if mouse_x:
            if (mouse_x >= 770) and (mouse_y >= 421) and (mouse_x <= 916) and (mouse_y <= 486):
                return 'sign in'
            elif (mouse_x >= 528) and (mouse_y >= 418) and (mouse_x <= 675) and (mouse_y <= 485):
                return 'login'


def opening_screen(name, password, client_socket):
    pic = 'screens/opening.png'
    screen_to_show = build_screen(1440, 759)
    run = True
    while run:
        run = not quit_pressed()
        screen_to_show.blit(pygame.image.load(pic), (0, 0))
        pygame.display.flip()
        (mouse_x, mouse_y) = mouse()
        if mouse_x is not False:
            if (mouse_x >= 500) and (mouse_y >= 439) and (mouse_x <= 574) and (mouse_y <= 513):
                if instructions_screen(name, password, client_socket):
                    return True
            elif (mouse_x >= 850) and (mouse_y >= 432) and (mouse_x <= 927) and (mouse_y <= 513):
                if story_screen(name, password, client_socket):
                    return True
            elif (mouse_x >= 26) and (mouse_y >= 32) and (mouse_x <= 72) and (mouse_y <= 82):
                music()
            elif (mouse_x >= 385) and (mouse_y >= 434) and (mouse_x <= 455) and (mouse_y <= 508):
                client_socket.send('get score;' + name + ';' + password)
                data = client_socket.recv(1024)
                if score_screen(name, password, client_socket, data):
                    return True
            elif (mouse_x >= 967) and (mouse_y >= 430) and (mouse_x <= 1041) and (mouse_y <= 510):
                client_socket.send('get winning table')
                data = client_socket.recv(1024)
                if winning_table_screen(name, password, client_socket, data):
                    return True
            elif (mouse_x >= 628) and (mouse_y >= 431) and (mouse_x <= 806) and (mouse_y <= 513):
                return True
            elif (mouse_x >= 683) and (mouse_y >= 563) and (mouse_x <= 760) and (mouse_y <= 642):
                return False


def score_screen(name, password, client_socket, data):
    pic = 'screens/score.png'
    screen_to_show = build_screen(1440, 759)
    run = True
    score = data.split(';')[0]
    winnings = data.split(';')[1]
    font = pygame.font.SysFont(None, 50)
    text_score = font.render(score, True, pg.Color('orange4'))
    text_winnings = font.render(winnings, True, pg.Color('orange4'))
    screen_to_show.blit(pygame.image.load(pic), (0, 0))
    screen_to_show.blit(text_score, (780, 400))
    screen_to_show.blit(text_winnings, (780, 495))
    pygame.display.flip()
    while run:
        run = not quit_pressed()
        (mouse_x, mouse_y) = mouse()
        if mouse_x is not False:
            if (mouse_x >= 673) and (mouse_y >= 658) and (mouse_x <= 748) and (mouse_y <= 737):
                return opening_screen(name, password, client_socket)
            elif (mouse_x >= 26) and (mouse_y >= 32) and (mouse_x <= 72) and (mouse_y <= 82):
                music()


def winning_table_screen(name, password, client_socket, data):
    pic = 'screens/winning table.png'
    screen_to_show = build_screen(1440, 759)
    data = data.replace('[', '').replace(']', '').replace("'", '')
    list_winners = data.split(',')
    run = True
    while run:
        run = not quit_pressed()
        screen_to_show.blit(pygame.image.load(pic), (0, 0))
        if len(list_winners) > 0:
            if list_winners[0][0] == ' ':
                list_winners[0] = list_winners[0][1:]
            font = pygame.font.SysFont(None, 40)
            if len(list_winners[0]) > 14:
                list_winners[0] = list_winners[0][:14] + '...'
            text_winner = font.render(list_winners[0], True, pg.Color('orange4'))
            screen_to_show.blit(text_winner, (600, 265))
        if len(list_winners) > 1:
            if list_winners[0][0] == ' ':
                list_winners[0] = list_winners[0][1:]
            font = pygame.font.SysFont(None, 40)
            if len(list_winners[1]) > 14:
                list_winners[1] = list_winners[1][:14] + '...'
            text_winner = font.render(list_winners[1], True, pg.Color('orange4'))
            screen_to_show.blit(text_winner, (600, 390))
        if len(list_winners) > 2:
            if list_winners[2][0] == ' ':
                list_winners[2] = list_winners[2][1:]
            font = pygame.font.SysFont(None, 40)
            if len(list_winners[2]) > 14:
                list_winners[2] = list_winners[2][:14] + '...'
            text_winner = font.render(list_winners[2], True, pg.Color('orange4'))
            screen_to_show.blit(text_winner, (600, 510))
        pygame.display.flip()
        (mouse_x, mouse_y) = mouse()
        if mouse_x is not False:
            if (mouse_x >= 673) and (mouse_y >= 658) and (mouse_x <= 748) and (mouse_y <= 737):
                return opening_screen(name, password, client_socket)
            elif (mouse_x >= 26) and (mouse_y >= 32) and (mouse_x <= 72) and (mouse_y <= 82):
                music()


def story_screen(name, password, client_socket):
    pic = 'screens/game_stroy.png'
    screen_to_show = build_screen(1440, 759)
    run = True
    while run:
        run = not quit_pressed()
        screen_to_show.blit(pygame.image.load(pic), (0, 0))
        pygame.display.flip()
        (mouse_x, mouse_y) = mouse()
        if mouse_x is not False:
            if (mouse_x >= 474) and (mouse_y >= 580) and (mouse_x <= 552) and (mouse_y <= 662):
                return instructions_screen(name, password, client_socket)
            elif (mouse_x >= 872) and (mouse_y >= 584) and (mouse_x <= 948) and (mouse_y <= 661):
                return opening_screen(name, password, client_socket)
            elif (mouse_x >= 623) and (mouse_y >= 602) and (mouse_x <= 802) and (mouse_y <= 681):
                return True
            elif (mouse_x >= 26) and (mouse_y >= 32) and (mouse_x <= 72) and (mouse_y <= 82):
                music()


def instructions_screen(name, password, client_socket):
    pic = 'screens/instructions.png'
    screen_to_show = build_screen(1440, 759)
    run = True
    while run:
        run = not quit_pressed()
        screen_to_show.blit(pygame.image.load(pic), (0, 0))
        pygame.display.flip()
        (mouse_x, mouse_y) = mouse()
        if mouse_x is not False:
            if (mouse_x >= 489) and (mouse_y >= 580) and (mouse_x <= 563) and (mouse_y <= 658):
                return story_screen(name, password, client_socket)
            elif (mouse_x >= 875) and (mouse_y >= 583) and (mouse_x <= 947) and (mouse_y <= 656):
                return opening_screen(name, password, client_socket)
            elif (mouse_x >= 626) and (mouse_y >= 601) and (mouse_x <= 802) and (mouse_y <= 681):
                return True
            elif (mouse_x >= 27) and (mouse_y >= 36) and (mouse_x <= 73) and (mouse_y <= 81):
                music()


def build_screen(window_width, window_height):
    # Init screen
    pygame.init()
    size = (window_width, window_height)
    screen_to_show = pygame.display.set_mode(size)
    pygame.display.set_caption("Games Of Magic")
    return screen_to_show


def mouse():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            return pygame.mouse.get_pos()
    return False, False


def quit_pressed():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    return False


def music():
    if pygame.mixer.music.get_busy() == 1:
        pygame.mixer.music.stop()
    else:
        pygame.mixer.music.play(-1, 2)


def play_intro():
    pygame.mixer.music.load('opening_music.mp3')
    pygame.mixer.music.play(-1, 2)


def show_loading_screen(is_not_tournament):
    dictionary_pic = {True: 'screens/loading.png', False: 'screens/loading2.png'}
    pic = dictionary_pic[is_not_tournament]
    screen_to_show = build_screen(1440, 759)
    screen_to_show.blit(pygame.image.load(pic), (0, 0))
    pygame.display.flip()


def after_battle_screen(my_castle):
    dict_after_battle = {'loser': 'screens/loser.png', 'winner': 'screens/winner.png'}
    run = True
    screen_to_show = build_screen(1440, 759)
    play_intro()
    if my_castle.health == 0:
        img = pygame.image.load(dict_after_battle['loser'])
        screen_to_show.blit(img, (0, 0))
        pygame.display.flip()
    else:
        img = pygame.image.load(dict_after_battle['winner'])
        screen_to_show.blit(img, (0, 0))
        pygame.display.flip()
    while run:
        run = not quit_pressed()
        mouse_x, mouse_y = mouse()
        if mouse_x:
            if (mouse_x >= 670) and (mouse_y >= 657) and (mouse_x <= 747) and (mouse_y <= 738):
                run = False


def communication_with_server_and_run_game(client_socket, open_client_sockets, name, password, is_not_tournament):
    data = ''
    while len(data) == 0:
        show_loading_screen(is_not_tournament)
        read_list, write_list, x_list = select.select([client_socket] + open_client_sockets, open_client_sockets, [])
        if read_list:
            data = client_socket.recv(1024)
    my_side = data.split(';')[0]
    sys.argv = [client_socket, my_side, name, password]
    execfile("client_game.py")
    return sys.argv[0]


def main():
    client_socket = socket.socket()
    client_socket.connect(('142.93.106.146', 8080))
    client_socket.setblocking(True)
    login_or_sign_in = menu_screen()
    sys.argv = [client_socket, login_or_sign_in]
    execfile("user_login.py")
    name = sys.argv[0]
    password = sys.argv[1]
    open_client_sockets = [client_socket]
    build_screen(1440, 759)
    play_intro()
    while True:
        is_not_tournament = opening_screen(name, password, client_socket)
        if is_not_tournament:
            client_socket.send('want-play')
            show_loading_screen(is_not_tournament)
            my_castle = communication_with_server_and_run_game(client_socket, open_client_sockets, name, password,
                                                               is_not_tournament)
            if my_castle.health != 0:
                client_socket.send('add points and winning;' + name + ';' + password + ';' + str(int(my_castle.health)))
            after_battle_screen(my_castle)
        else:
            client_socket.send('tournament')
            show_loading_screen(is_not_tournament)
            my_castle = communication_with_server_and_run_game(client_socket, open_client_sockets, name, password,
                                                               is_not_tournament)
            if my_castle.health != 0:
                play_intro()
                client_socket.send(
                    'add points to tournament and winning;' + name + ';' + password + ';' + str(int(my_castle.health)))
                my_castle = communication_with_server_and_run_game(client_socket, open_client_sockets, name, password,
                                                                   is_not_tournament)
                if my_castle.health != 0:
                    client_socket.send('add points to tournament and winning;' + name + ';' + password + ';' + str(
                        int(my_castle.health)))
            after_battle_screen(my_castle)


if __name__ == "__main__":
    main()
