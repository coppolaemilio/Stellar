import pygame
import os 
import sys
import math
from keys import *

def set_icon(icon):
    pygame.display.set_icon(icon)

def set_caption(string):
    pygame.display.set_caption(string)


ODIN_DIR = os.path.dirname(__file__)
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
set_icon(pygame.image.load(os.path.join(ODIN_DIR, "icon.png")))
set_caption("Caption")

screen_size = (640, 480)
screen = pygame.display.set_mode(screen_size)
FPS = 60
fps_clock = pygame.time.Clock()
room_height = 0
room_width = 0
draw_color = (0,0,0)
# Instantiate 16 point Courier font to draw text.
my_font = pygame.font.SysFont("Courier", 16)

class Object(object):
    def __init__(self, x, y):
        super(Object, self).__init__()
        self.x = x
        self.y = y
        self.mask = pygame.Rect(32, 32, 32, 32)

    def event_create(self):
        pass

    def event_update(self):
        self.mask.x = self.x
        self.mask.y = self.y 

    def event_step(self):
        pass

    def event_draw(self):
        draw_sprite(self.sprite_index, 0, self.x, self.y)

    def event_collision(self, other=None):
        pass

class Room(object):
    def __init__(self):
        super(Room, self).__init__()

    def event_create(self):
        pass
    def event_step(self):
        pass
    def event_draw(self):
        screen.fill(self.background_color)

########################
# Resources management #
########################
sprites_group = []
objects_group = []

def create_sprite(sprite_name, alpha=0):
    if alpha == 0:
        spr = pygame.image.load(os.path.join("sprites", sprite_name)).convert()
    else:
        spr = pygame.image.load(os.path.join("sprites", sprite_name)).convert_alpha()
    sprites_group.append(spr)
    return spr


##################
# Draw Functions #
##################
def draw_sprite(sprite, subimg, x, y):
    screen.blit(sprite, (x,y))

def draw_set_color(color):
    global draw_color
    draw_color = color

def draw_text(x, y, string):
    global draw_color
    the_text = my_font.render(string, True, draw_color)
    screen.blit(the_text, (x, y))


def instance_create(obj, x, y):
    i = obj(x, y)
    objects_group.append(i)
    return i

def instance_destroy(self):
    objects_group.remove(self)

key_check = []
def keyboard_check(what_key):
    global key_check
    try:
        if key_check[what_key]:
            return True
    except:
        return False


##################
# Room Functions #
##################
current_room = Room()
def change_room(room):
    del objects_group[:]
    global current_room
    current_room = room()
    current_room.create_event()
    current_room.background_color
    for instance in objects_group:
        instance.event_create()

def room_restart():
    del objects_group[:]
    global current_room
    current_room.background_color
    current_room.create_event()
    for instance in objects_group:
        instance.event_create()
    



#####################
# Collision engine  #
#####################

def doRectsOverlap(rect1, rect2):
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        # Check if a's corners are inside b
        if ((isPointInsideRect(a[0], a[1], b)) or
            (isPointInsideRect(a[0], a[3], b)) or
            (isPointInsideRect(a[2], a[1], b)) or
            (isPointInsideRect(a[2], a[3], b))):
            return True
    return False

def isPointInsideRect(x, y, rect):
    if x > rect[0]-1 and x < rect[2]-1 and y > rect[1]-1 and y < rect[3]-1:
        return True
    else:
        return False

def distance_to_object(a, b):
    return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)

def distance_to_point(a, x, y):
    return math.sqrt((a.x-x)**2 + (a.y-y)**2)    


def place_empty(x, y):
    #Returns whether the instance placed at position (x,y) meets nobody
    return True
    objRect = pygame.Rect(x, y, 1, 1)
    if objRect.collidepoint(x, y):
        return False
    return True

    #for other in objects_group:
    #    if x > other.x-1 and x<other.x+32 and y> other.y-1 and y<other.y+32:
    #        return False
    #return True


##################
# Game Settings  #
##################
cr_none = False
def window_set_cursor(state):
    if state:
        pygame.mouse.set_visible(True)
    else:
        pygame.mouse.set_visible(False)

def window_set_fullscreen(state):
    if state:
        screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(screen_size)


##################
# Game Functions #
##################

def game_end():
    pygame.quit()
    sys.exit()

##################
# Game Loop      #
##################

def start_game(start_room):
    global current_room
    current_room = start_room()
    current_room.create_event()
    for instance in objects_group:
        instance.event_create()
    while True:
        current_room.event_draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_end()
            global key_check
            key_check = pygame.key.get_pressed()

        for instance in objects_group:
            instance.event_step()
            instance.event_update()
            instance.event_collision()
            instance.event_draw()

        pygame.display.flip()
        fps_clock.tick(FPS)