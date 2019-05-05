import pygame
from math import sin, cos, pi
from math import atan2, pi
import math


class Character(object):
    """
    A basic object by which the characters can be constructed, with the help of the object, you can move, attack, check
    if an object is in an attack environment, show a walking picture, check a walking image and check the distance
    between two objects.
    """

    def __init__(self, type_character, x, y, width, height, width_attack, height_attack, start_health, power, cost,
                 step, attack_range, walk_img, attack_img,
                 side, limit_walking, limit_attacking, screen):
        self.type = type_character  # Character type (Miniature, Magician, etc.)
        self.x = x  # Position of the character on axis X.
        self.y = y  # Position of the character on axis Y.
        self.width = width  # The image's length is in walking mode
        self.height = height  # The height of the image of the character when it is in walking mode
        self.width_attack = width_attack  # The image's length is in attacking mode
        self.height_attack = height_attack  # The height of the image of the character when it is in assault mode
        self.start_health = start_health  # The amount of life with which the character begins
        self.health = start_health  # The current amount of life of the character
        self.hit_box_health = float(100) / float(start_health)  # Calculate for the view of the character's life
        self.hit_box = (self.x + self.width / 3, self.y + 11, 29, 52)  # The life gauge of the character
        self.power = power  # The amount of life that the character can download to other objects
        self.cost = cost  # The amount of potion the figure rises
        self.step = step  # The distance the figure moves
        self.attack_range = attack_range  # The distance the character can attack
        self.index_walking = 0  # The image of the character's current walk
        self.index_attacking = 0  # The image of the current attack of the character
        self.limit_walking = limit_walking  # The amount of images of the walk
        self.limit_attacking = limit_attacking  # The number of images of the attack
        self.walk_img = walk_img  # The base address of the walk image (without the number)
        self.attack_img = attack_img  # The base address of the attack image (without the number)
        self.side = side  # The side of the castle to which the figure belongs
        self.dic_side_boolean = {'left': True, 'right': False}  # A dictionary that helps to display the character
        self.screen = screen  # The screen object with which we present the image
        self.center_x, self.center_y = get_center_point(self.x, self.y, self.width,
                                                        self.height)  # Character's center, X and Y points
        self.attacked = False  # Is the character attacking

    def show_walk(self):
        string_index, self.index_walking = get_index_string(self.index_walking,
                                                            self.limit_walking)  # The current index of the image of
        # walking in a string and promoting the index in one
        img_name = pygame.image.load(self.walk_img + string_index + '.png')  # Loading the image
        img = pygame.transform.scale(img_name, (self.width, self.height))  # Format the image at the desired size
        self.screen.blit(pygame.transform.flip(img, self.dic_side_boolean[self.side], False), (
            self.x, self.y))  # Displays the image on the screen and rotates the image on the y-axis if necessary
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.hit_box[0], self.hit_box[1] - 20, 50, 10))  # Displays the character's life meter
        pygame.draw.rect(self.screen, (0, 128, 0), (
            self.hit_box[0], self.hit_box[1] - 20, 50 - (5 * (10 - (self.hit_box_health * self.health) / 10)),
            10))  # Displays the character's life meter
        self.hit_box = (self.x + self.width / 3, self.y + 2, 31, 57)  # Reconfiguration of the character's life meter

    def show_attack(self):
        string_index, self.index_attacking = get_index_string(self.index_attacking,
                                                              self.limit_attacking)  # The current index of the image of
        # attacking in a string and promoting the index in one
        img_name = pygame.image.load(self.attack_img + string_index + '.png')  # Loading the image
        img = pygame.transform.scale(img_name,
                                     (self.width_attack, self.height_attack))  # Format the image at the desired size
        if self.type == 'Minotaur':  # Match in case the character is a fan
            self.screen.blit(pygame.transform.flip(img, self.dic_side_boolean[self.side], False),
                             (self.x, self.y - self.height_attack / 2))
        else:  # Match in case the character is a fan
            self.screen.blit(pygame.transform.flip(img, self.dic_side_boolean[self.side], False), (self.x, self.y))
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.hit_box[0], self.hit_box[1] - 20, 50, 10))  # Displays the character's life meter
        pygame.draw.rect(self.screen, (0, 128, 0), (
            self.hit_box[0], self.hit_box[1] - 20, 50 - (5 * (10 - (self.health * self.hit_box_health) / 10)),
            10))  # Displays the character's life meter
        self.hit_box = (self.x + self.width / 3, self.y + 2, 31, 57)  # Reconfiguration of the character's life meter

    def move_to(self, obj):
        # starting point
        x0 = self.x
        y0 = self.y
        angel = angel_between_two_point(self.x, self.y, obj.x, obj.y)
        dis = self.step
        # theta is the angle (in radians) of the direction in which to move
        theta = angel
        delta_x = dis * cos(theta)
        delta_y = dis * sin(theta)
        # new point
        self.x = int(x0 + delta_x)
        self.y = int(y0 + delta_y)
        self.center_x, self.center_y = get_center_point(self.x, self.y, self.width, self.height)

    def attack(self, obj):
        obj.health -= self.power  # Reducing the life of the opponent object
        if obj.health < 0:
            obj.health = 0

    def in_attack_range(self, obj):
        return self.attack_range >= self.distance(obj)

    def distance(self, obj):
        sq1 = (self.center_x - obj.center_x) * (self.center_x - obj.center_x)
        sq2 = (self.center_y - obj.center_y) * (self.center_y - obj.center_y)
        return math.sqrt(sq1 + sq2)

    def __str__(self):
        return 'Type: ', str(self.type), ', x: ', str(self.x), ', y: ', str(self.y)


def get_center_point(x, y, width, height):
    x1 = x
    y1 = y
    x2 = x + width
    y2 = y + height
    angel = angel_between_two_point(x1, y1, x2, y2)
    dis = distance_for_math(x1, y1, x2, y2)
    delta_x = dis * cos(angel)
    delta_y = dis * sin(angel)
    # new point
    center_x = int(x1 + delta_x)
    center_y = int(y1 + delta_y)
    return center_x, center_y


def get_index_string(index, limit):
    if index < 10:
        string_index = '00' + str(index)
    else:
        string_index = '0' + str(index)
    if index < limit:
        index += 1
    else:
        index = 0
    return string_index, index


def angel_between_two_point(xi, yi, xii, yii):
    # point 1
    x1 = xi
    y1 = yi
    # point 2
    x2 = xii
    y2 = yii
    delta_x = x2 - x1
    delta_y = y2 - y1
    return atan2(delta_y, delta_x)


def distance_for_math(xi, yi, xii, yii):
    sq1 = (xi - xii) * (xi - xii)
    sq2 = (yi - yii) * (yi - yii)
    return math.sqrt(sq1 + sq2)
