#This file was generated with Stellar
import os, sys
from odin import *

#Scripts ------------------------------
def test_script(argument0=None, arugment1=None, argument2=None):
    # This is an example script
    print "hello world"
    print "it works!"


#Sprites -------------------------------
spr_wall = create_sprite("spr_wall.png")
spr_player = create_sprite("spr_player.png")
spr_coin = create_sprite("spr_coin.png", 1)

#Objects ------------------------------
class obj_coin(Object):
    visible = True
    sprite_index = spr_coin

class obj_wall(Object):
    visible = True
    sprite_index = spr_wall

class obj_player(Object):
    visible = True
    sprite_index = spr_player

    def event_create(self):
        self.speed = 2

    def event_step(self):
        self.xprevious = self.x
        self.yprevious = self.y
        obj = obj_coin
        for other in objects_group:
            if other.__class__ == obj:
                if distance_to_object(self, other)<16:
                    instance_destroy(other)

        if keyboard_check(vk_right):
            if place_empty(self.x+1+32, self.y):
                self.x += self.speed
        if keyboard_check(vk_left):
            if place_empty(self.x-1, self.y):
                self.x -= self.speed
        if keyboard_check(vk_up):
            if place_empty(self.x, self.y-1):
                self.y -= self.speed
        if keyboard_check(vk_down):
            if place_empty(self.x, self.y+1+32):
                self.y += self.speed

        if keyboard_check(pygame.K_r):
            room_restart()


    def event_collision(self, obj = obj_wall):
        for other in objects_group:
            if other.__class__ == obj:
                if self.mask.colliderect(other.mask):
                    self.x = self.xprevious
                    self.y = self.yprevious



#Rooms --------------------------------
class room_1(Room):
    width = 640
    background_color = (150, 100, 150)
    height = 480
    def create_event(self):
        level = [
            "WWWWWWWWWWWWWWWWWWWW",
            "W                  W",
            "W  E      WWWWWW   W",
            "W    WWW   ccccW   W",
            "W   W        WWWW  W",
            "W WWW  WWWW        W",
            "W   W     W W      W",
            "W   W     W   WWW WW",
            "W   WWW  WW   W W  W",
            "W     W   W   W W  W",
            "WWW   W   WWWWW W  W",
            "W W   WW     WWW   W",
            "W W   W            W", 
            "W     W        W   W",
            "WWWWWWWWWWWWWWWWWWWW",
        ]
        x = y = 0
        for row in level:
            for col in row:
                if col == "W":
                    instance_create(obj_wall, x, y)
                if col == "E":
                    instance_create(obj_player, x, y)
                if col == "c":
                    instance_create(obj_coin, x+9, y+9)
                x += 32
            y += 32
            x = 0

    def draw_event(self):
        screen.fill(self.background_color)


#Game Start ---------------------------
start_game(room_1)
