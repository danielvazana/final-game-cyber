import pygame
from math import sin, cos, pi
from math import atan2, pi
import math


class Castle(object):

    def __init__(self, x, y, side, screen, start_index):
        self.x = x  # Position of the castle on axis X.
        self.y = y  # Position of the castle on axis Y.
        self.width = 300  # The image's length
        self.height = 237  # The height of the image of the castle
        self.start_health = 250  # The amount of life with which the castle begins
        self.health = self.start_health  # The current amount of life of the castle
        self.hit_box_health = float(100) / float(self.start_health)  # Calculate for the view of the castle's life
        self.hit_box = (self.x + 50, self.y + 11, 29, 52)  # The life gauge of the castle
        self.side = side  # The side of the castle
        self.img_castle = 'Castle/png/Asset '  # The base address of the image (without the number)
        self.start_index = start_index  # The image of the number of the current castle
        self.dic_side_boolean = {'left': True, 'right': False}  # A dictionary that helps to display the castle
        self.screen = screen  # The screen object with which we present the image
        self.center_x, self.center_y = get_center_point(self.x, self.y, self.width, self.height,
                                                        self.side)  # Castle's center, X and Y points

    def show(self):
        # For each third of the life of the castle will represent another castle situation
        if self.health >= (self.start_health / 3) * 2:
            img_c = pygame.image.load(
                self.img_castle + str(self.start_index) + '.png')  # Loading the image(Best condition)
            img = pygame.transform.scale(img_c, (self.width, self.height))  # Format the image at the desired size
            self.screen.blit(pygame.transform.flip(img, self.dic_side_boolean[self.side], False), (self.x, self.y))
            # Displays the image on the screen and rotates the image on the y-axis if necessary
        elif self.health >= self.start_health / 3:
            img_c = pygame.image.load(
                self.img_castle + str(self.start_index + 1) + '.png')  # Loading the image(Fair condition)
            img = pygame.transform.scale(img_c, (300, 237))  # Format the image at the desired size
            self.screen.blit(pygame.transform.flip(img, self.dic_side_boolean[self.side], False), (
                self.x, self.y))  # Displays the image on the screen and rotates the image on the y-axis if necessary
        else:
            img_c = pygame.image.load(
                self.img_castle + str(self.start_index + 2) + '.png')  # Loading the image(Poor condition)
            img = pygame.transform.scale(img_c, (300, 175))  # Format the image at the desired size
            self.screen.blit(pygame.transform.flip(img, self.dic_side_boolean[self.side], False), (
                self.x,
                self.y + 62))  # Displays the image on the screen and rotates the image on the y-axis if necessary
        if self.side is 'left':
            pygame.draw.rect(self.screen, (255, 0, 0),
                             (self.hit_box[0] + 150, self.hit_box[1] - 20, 100, 10))  # Displays the castle's life meter
            pygame.draw.rect(self.screen, (139, 76, 57), (
                self.hit_box[0] + 150, self.hit_box[1] - 20, 50 - (5 * (10 - (self.health * self.hit_box_health) / 5)),
                10))
        else:
            pygame.draw.rect(self.screen, (255, 0, 0),
                             (self.hit_box[0], self.hit_box[1] - 20, 100, 10))  # Displays the castle's life meter
            pygame.draw.rect(self.screen, (54, 100, 139), (
                self.hit_box[0], self.hit_box[1] - 20, 50 - (5 * (10 - (self.health * self.hit_box_health) / 5)),
                10))
        self.hit_box = (self.x + 17, self.y + 2, 31, 57)  # Reconfiguration of the castle's life meter

    def __str__(self):
        return "side :" + str(self.side) + ", x :" + str(self) + ', y :' + str(self.y)


def get_center_point(x, y, width, height, side):
    x1 = x
    y1 = y
    x2 = x + width
    y2 = y + height
    angel = angel_between_two_point(x1, y1, x2, y2)
    dis = distance(x1, y1, x2, y2)
    delta_x = dis * cos(angel)
    delta_y = dis * sin(angel)
    # new point
    center_x = int(x1 + delta_x)
    center_y = int(y1 + delta_y)
    if side == 'left':
        center_x -= width / 2
    return center_x, center_y


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


def distance(xi, yi, xii, yii):
    sq1 = (xi - xii) * (xi - xii)
    sq2 = (yi - yii) * (yi - yii)
    return math.sqrt(sq1 + sq2)
