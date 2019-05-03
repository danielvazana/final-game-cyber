import pygame as pg
import pygame
import sys
import time

pg.init()
COLOR_INACTIVE = pg.Color('navajowhite2')
COLOR_ACTIVE = pg.Color('orange4')
FONT = pg.font.Font(None, 35)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)  # Text box dimensions
        self.color = COLOR_INACTIVE  # Text color
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)  # The text is converted to represent
        self.active = False  # Is the box enabled

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key is not pg.K_RETURN:
                    self.text += event.unicode
                # Re-render the text.
                if len(self.text) > 17:
                    self.txt_surface = FONT.render(self.text[len(self.text) - 17:], True, self.color)
                else:
                    self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen_to_show):
        # Blit the text.
        screen_to_show.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 25))


def show_user_login(sign_in_or_login):
    sign_in_or_login_dic = {'login': 'screens/user_login.png', 'sign in': 'screens/user_sign in.png'}
    pic = sign_in_or_login_dic[sign_in_or_login]
    screen_to_show = build_screen(1440, 759)
    screen_to_show.blit(pygame.image.load(pic), (0, 0))
    pygame.display.flip()
    return screen_to_show


def build_screen(window_width, window_height):
    # Init screen
    pygame.init()
    size = (window_width, window_height)
    screen_to_show = pygame.display.set_mode(size)
    pygame.display.set_caption("Games Of Magic")
    return screen_to_show


def all_the_work(screen_to_show, input_boxes, answer, sign_in_or_login):
    finish_rect = pg.Rect(663, 664, 75, 75)
    clock = pg.time.Clock()
    done = False
    while not done:
        show_answer(screen_to_show, answer, sign_in_or_login)
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if finish_rect.collidepoint(event.pos):
                    done = True
            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            box.update()
        show_user_login(sign_in_or_login)
        for box in input_boxes:
            box.draw(screen_to_show)

        pg.display.flip()
        clock.tick(30)


def show_answer(screen_to_show, answer, sign_in_or_login):
    dic_size = {'login': 50, 'sign in': 35}
    font = pygame.font.SysFont("comicsansms", dic_size[sign_in_or_login])
    text = font.render(answer, True, (255, 69, 0))
    screen_to_show.blit(text, (710 - text.get_width() // 2, 130 - text.get_height() // 2))
    pygame.display.flip()


def quit_pressed():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


def main():
    client_socket = sys.argv[0]
    sign_in_or_login = sys.argv[1]
    input_box1 = InputBox(570, 250, 200, 70)
    input_box2 = InputBox(570, 500, 200, 70)
    input_boxes = [input_box1, input_box2]
    screen_to_show = show_user_login(sign_in_or_login)
    run = True
    answer = ''
    while run:
        quit_pressed()
        all_the_work(screen_to_show, input_boxes, answer, sign_in_or_login)
        if input_box1.text != '' and input_box2.text != '':
            client_socket.send(sign_in_or_login + ';' + input_box1.text + ';' + input_box2.text)
            answer = client_socket.recv(1024)
            if 'ok' == answer:
                run = False
    sys.argv = [input_box1.text, input_box2.text]


if __name__ == '__main__':
    main()
    pg.quit()
