#This file was generated with Stellar
import os, sys
from odin import *

#Scripts ------------------------------
def test_script(argument0=False, arugment1=False, argument2=False):
    # This is an example script
    print "hello world"
    print "it works!"


#Sprites -------------------------------
spr_wall = create_sprite("spr_wall.png")
spr_player = create_sprite("spr_player.png")

#Objects ------------------------------
class obj_wall(Object):
    visible = True
    sprite_index = spr_wall

class obj_test(Object):
    visible = True
    sprite_index = spr_wall

class obj_player(Object):
    visible = True
    sprite_index = spr_player
    def create_event(self):
        self.speed = 2
    def event_step(self):
        if keyboard_check(vk_right):
            self.x += self.speed
        if keyboard_check(vk_left):
            self.x -= self.speed
        if keyboard_check(vk_up):
            self.y -= self.speed
        if keyboard_check(vk_down):
            self.y += self.speed
        if keyboard_check(pygame.K_r):
            change_room(room_2)
        
        if keyboard_check(vk_w):
            test_script()
        else:
            self.speed = 2


#Rooms --------------------------------
class room_1(Room):
    width = 640
    background_color = (100, 100, 150)
    height = 480
    def create_event(self):
        for x in xrange(0,10):
            instance_create(obj_wall, x*32,0)
        instance_create(obj_player, 32,32)
    def draw_event(self):
        screen.fill(self.background_color)


#Game Start ---------------------------
start_game(room_1)