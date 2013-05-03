#!/usr/bin/env python

import sge
import os
#Imports


#Paths
sge.image_directories = [os.path.join('Sprites'),os.path.join('Backgrounds')]
sge.font_directories = [os.path.join('Fonts')]
sge.sound_directories = [os.path.join('Sound')]
sge.music_directories = [os.path.join('Sound')]


#Game Class
class Game(sge.Game):
    def event_key_press(self, key):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()
        

#spr_cancel

class obj_0(sge.StellarClass):

    def __init__(self, x, y, player=0):
        super(obj_0, self).__init__(x, y, 5, 'spr_cancel', collision_precise=True)
        self.player = player



#spr_cristal

class obj_cristal(sge.StellarClass):

    def __init__(self, x, y, player=0):
        super(obj_cristal, self).__init__(x, y, 5, 'spr_cristal', collision_precise=True)
        self.player = player





    def event_create(self):

        

        #"This is the creation event"

        self.image_alpha = 200
        self.image_blend = 'white'

    def event_step(self, time_passed):

        

        left_key = ['left', 'a', 'j', 'kp_4'][self.player]
        right_key = ['right', 'd', 'l', 'kp_6'][self.player]
        up_key = ['up', 'w', 'i', 'kp_8'][self.player]
        down_key = ['down', 's', 'k', 'kp_5'][self.player]
        
        self.xvelocity = (sge.game.get_key_pressed(right_key) -
                                  sge.game.get_key_pressed(left_key))
        self.yvelocity = (sge.game.get_key_pressed(down_key) -
                                  sge.game.get_key_pressed(up_key))
        
        self.x += self.xvelocity
        self.y += self.yvelocity
        
        # Limit the circles to inside the room.
        if self.bbox_left < 0:
            self.bbox_left = 0
        elif self.bbox_right >= sge.game.current_room.width:
            self.bbox_right = sge.game.current_room.width - 1
        if self.bbox_top < 0:
            self.bbox_top = 0
        elif self.bbox_bottom >= sge.game.current_room.height:
            self.bbox_bottom = sge.game.current_room.height - 1
        



game = Game()
# Load sprites
spr_cancel_sprite = sge.Sprite('spr_cancel', transparent=True)
spr_cristal_sprite = sge.Sprite('spr_cristal', transparent=True)
fence_sprite = sge.Sprite('fence', transparent=True)


layers = (sge.BackgroundLayer(fence_sprite, 0, 380, 0, yrepeat=True),)
background = sge.Background(layers, 0xffffff)

circle = obj_cristal(game.width // 2, game.height // 2)
circle1= obj_0(20,20)
objects = [circle,circle1]


views = (sge.View(0, 0),)

rm_0 = sge.Room(tuple(objects), views=views, background=background)


game.start()

