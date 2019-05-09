import pygame
from math import sin, cos, pi
from math import atan2, pi
import math
from Charachters import *
from Castle import Castle
import socket
import select
import sys
import random
from datetime import datetime


def quit_pressed():
    finish = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    return finish


def build_screen(window_width, window_height):
    pygame.init()
    size = (window_width, window_height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Games Of Magic")
    return screen


def build_areana(screen):
    image = 'skillz/frozen copy 2.jpeg'
    img = pygame.image.load(image)
    screen.blit(img, (0, 0))


def show_creachers(creachers):
    creachers_to_run = creachers[:]
    for creacher in creachers_to_run:
        if creacher.health == 0:
            creachers.remove(creacher)
        elif creacher.attacked:
            creacher.show_attack()
        else:
            creacher.show_walk()
    del creachers_to_run


def show_castles(castles):
    castles_to_run = castles[:]
    for castle in castles_to_run:
        if castle.health == 0:
            castles.remove(castle)
        else:
            castle.show()
    del castles_to_run
    return True


def run_creachers(my_list, enemy_enemy, castle):
    my_creachers_to_run = my_list[:]
    for my_creacher in my_creachers_to_run:
        my_creacher.attacked = False
        if my_creacher.type != 'Minotaur':
            closest_enemy_creacher = closest_object_to_object(my_creacher, enemy_enemy)
            if closest_enemy_creacher:
              if closest_enemy_creacher.type != 'Minotaur':
                  if my_creacher.in_attack_range(closest_enemy_creacher):
                      my_creacher.attack(closest_enemy_creacher)
                      my_creacher.attacked = True
              elif my_creacher.distance(closest_enemy_creacher)/2 <= my_creacher.attack_range:
                  my_creacher.attack(closest_enemy_creacher)
                  my_creacher.attacked = True
        if not my_creacher.attacked:
            if my_creacher.distance(castle) <= 300:
                my_creacher.attack(castle)
                my_creacher.attacked = True
            else:
                my_creacher.move_to(castle)
    return my_creachers_to_run


def closest_object_to_object(obj, list_to_find):
    if len(list_to_find) > 0:
        return sorted(list_to_find, key=lambda v: v.distance(obj))[0]


def show_mana(mana, screen):
    if mana > 0:
        pygame.draw.rect(screen, (180, 82, 205), (84, 24, mana * 16, 20))
    pygame.font.init()
    myfont = pygame.font.SysFont('comicsansms', 32)
    textsurface = myfont.render(str(mana), False, (75,0,130))
    screen.blit(textsurface, (39, 25))


def characters_names_list():
    characters_names = ['Medusa', 'Wizard', 'Minotaur', 'Skeleton', 'Golem', 'Knight']
    list_ch = []
    while len(list_ch) < 6:
        obj = characters_names[random.randint(0, len(characters_names) - 1)]
        list_ch.append(obj)
        characters_names.remove(obj)
    return list_ch


def mouse():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            return pygame.mouse.get_pos()
    return False, False


def show_toolbar(characters_names, screen):
    dict_names = {'Medusa': 'Fantasy Free Game Kit/Characters/Monster - Medusa/Spriter Files/Assets/Head/Head.png',
                  'Wizard': 'Fantasy Free Game Kit/Characters/Hero - Wizard/Spriter File/Head/Head.png',
                  'Minotaur': 'Fantasy Free Game Kit/Characters/Monster - Minotaur/Spriter File/Assets/Head/Head.png',
                  'Skeleton': 'Fantasy Free Game Kit/Characters/Monster - Skeleton/Spriter File/Assets/Head/Head.png',
                  'Golem': 'Golem/Golem_1/PNG/Vector Parts/Head copy.png',
                  'Knight': 'knights/__SCML/3_KNIGHT/3_head_.png'}
    img = pygame.image.load(dict_names[characters_names[0]])
    if characters_names[0] is 'Wizard' or characters_names[0] is 'Minotaur':
        screen.blit(img, (150, 50))
    else:
        screen.blit(img, (160, 45))
    img = pygame.image.load(dict_names[characters_names[1]])
    if characters_names[0] == 'Wizard' or characters_names[0] == 'Minotaur':
        screen.blit(img, (40, 50))
    else:
        screen.blit(img, (56, 45))


def in_toolbar(x, y):
    if (x >= 150) and (y >= 50) and (x <= 250) and (y <= 143):
        return 'Right'
    if (x >= 40) and (y >= 50) and (x <= 140) and (y <= 143):
        return 'Left'
    else:
        return False


def handel_charachter_to_append(mouse_x, mouse_y, characters_names, character_to_append, client_socket, mana, my_side):
    dict_names_cost = {'Medusa': 6, 'Wizard': 4, 'Minotaur': 5, 'Skeleton': 4, 'Golem': 3, 'Knight': 6}
    if mouse_x:
        flag = False
        if my_side == 'right':
            if mouse_x >= 720:
                flag = True
        elif my_side == 'left':
            if mouse_x <= 720:
                flag = True
        if character_to_append is not '':
            if in_toolbar(mouse_x, mouse_y):
                if in_toolbar(mouse_x, mouse_y) is 'Right':
                    return characters_names[0], mana
                else:
                    return characters_names[1], mana
            elif flag and mana >= dict_names_cost[character_to_append]:
                client_socket.send(character_to_append + ':' + str(mouse_x) + ':' + str(mouse_y) + ':' + my_side)
                characters_names.remove(character_to_append)
                characters_names.append(character_to_append)
                return '', mana - dict_names_cost[character_to_append]
            else:
                return character_to_append, mana
        elif in_toolbar(mouse_x, mouse_y):
            if in_toolbar(mouse_x, mouse_y) is 'Right':
                return characters_names[0], mana
            else:
                return characters_names[1], mana
        else:
            return character_to_append, mana
    else:
        return character_to_append, mana


def return_character_by_string(data, screen, my_side, my_creachers, enemy_creachers):
    list_data = data.split(':')
    character_side = {'left': 'right', 'right': 'left'}
    if list_data[3] == my_side:
        if list_data[0] == 'Medusa':
            my_creachers.append(Medusa(int(list_data[1]), int(list_data[2]), character_side[list_data[3]], screen))
        elif list_data[0] == 'Wizard':
            my_creachers.append(Wizard(int(list_data[1]), int(list_data[2]), character_side[list_data[3]], screen))
        elif list_data[0] == 'Minotaur':
            my_creachers.append(Minotaur(int(list_data[1]), int(list_data[2]), character_side[list_data[3]], screen))
        elif list_data[0] == 'Skeleton':
            my_creachers.append(Skeleton(int(list_data[1]), int(list_data[2]), character_side[list_data[3]], screen))
        elif list_data[0] == 'Golem':
            my_creachers.append(Golem(int(list_data[1]), int(list_data[2]), character_side[list_data[3]], screen))
        elif list_data[0] == 'Knight':
            my_creachers.append(Knight(int(list_data[1]), int(list_data[2]), character_side[list_data[3]], screen))
    else:
        if list_data[0] == 'Medusa':
            enemy_creachers.append(Medusa(int(list_data[1]), int(list_data[2]), character_side[list_data[3]], screen))
        elif list_data[0] == 'Wizard':
            enemy_creachers.append(Wizard(int(list_data[1]), int(list_data[2]), character_side[list_data[3]], screen))
        elif list_data[0] == 'Minotaur':
            enemy_creachers.append(Minotaur(int(list_data[1]), int(list_data[2]), character_side[list_data[3]], screen))
        elif list_data[0] == 'Skeleton':
            enemy_creachers.append(Skeleton(int(list_data[1]), int(list_data[2]), character_side[list_data[3]], screen))
        elif list_data[0] == 'Golem':
            enemy_creachers.append(Golem(int(list_data[1]), int(list_data[2]), character_side[list_data[3]], screen))
        elif list_data[0] == 'Knight':
            enemy_creachers.append(Knight(int(list_data[1]), int(list_data[2]), character_side[list_data[3]], screen))
    return my_creachers, enemy_creachers


def update_mana(mana, turn):
    if turn % 35 == 0 and mana < 10:
        return mana + 1
    else:
        return mana


def set_castles(my_side, screen):
    if my_side == 'left':
        my_castle = Castle(-150, 580, 'left', screen, 21)
        enemy_castle = Castle(1300, 50, 'right', screen, 24)
    else:
        my_castle = Castle(1300, 50, 'right', screen, 24)
        enemy_castle = Castle(-150, 580, 'left', screen, 21)
    return my_castle, enemy_castle


def show_side(screen, my_side, turn):
    dict_colors_by_side = {'left': (139, 76, 57), 'right': (54, 100, 139)}
    if turn <= 15:
        font = pygame.font.SysFont("comicsansms", 72)
        text = font.render(my_side.upper(), True, dict_colors_by_side[my_side])
        screen.blit(text, (732 - text.get_width() // 2, 340 - text.get_height() // 2))


def music_battle():
    pygame.mixer.music.load('music1.mp3')
    pygame.mixer.music.play(-1, 2)


def main():
    client_socket = sys.argv[0]
    music_battle()
    my_side = sys.argv[1]
    screen = build_screen(1440, 819)
    turn = 0
    my_creachers = []
    enemy_creachers = []
    my_castle, enemy_castle = set_castles(my_side, screen)
    castle_for_good_graphics = Castle(1300, -1000000, 'right', screen, 24)
    characters_names = characters_names_list()
    character_to_append = ''
    mana = 3
    run = True
    while run:
        turn += 1
        ready = select.select([client_socket], [], [], 0.016)
        if ready[0]:
            data = client_socket.recv(1024)
            if data != 'finish':
                my_creachers, enemy_creachers = return_character_by_string(data, screen, my_side, my_creachers,
                                                                           enemy_creachers)
            else:
                run = False
        if run:
            mana = update_mana(mana, turn)
            build_areana(screen)
            show_mana(mana, screen)
            show_side(screen, my_side, turn)
            my_castle.show()
            enemy_castle.show()
            show_toolbar(characters_names, screen)
            show_creachers(my_creachers)
            show_creachers(enemy_creachers)
            pygame.display.flip()
            castle_for_good_graphics.show()
            my_creachers_new = run_creachers(my_creachers, enemy_creachers, enemy_castle)
            enemy_creachers_new = run_creachers(enemy_creachers, my_creachers, my_castle)
            my_creachers = my_creachers_new
            enemy_creachers = enemy_creachers_new
            mouse_x, mouse_y = mouse()
            character_to_append, mana = handel_charachter_to_append(mouse_x, mouse_y, characters_names,
                                                                    character_to_append, client_socket, mana, my_side)
            run = run and (not quit_pressed()) and my_castle.health is not 0 and enemy_castle.health is not 0
    sys.argv = [my_castle]


if __name__ == "__main__":
    main()
