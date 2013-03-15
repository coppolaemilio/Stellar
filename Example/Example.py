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
        

class Circle(sge.StellarClass):
    def __init__(self, x, y, player=0):
        super(Circle, self).__init__(x, y, 5, 'circle', collision_precise=True)
        self.player = player

    def event_create(self):
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
circle_sprite = sge.Sprite('circle', transparent=True)
fence_sprite = sge.Sprite('fence', transparent=True)
fence112_sprite = sge.Sprite('fence112', transparent=True)


#testeandocosaslocas
#testeandocosaslocas
#testeandocosaslocas
#testeandocosaslocas
#testeandocosaslocas

layers = (sge.BackgroundLayer(fence_sprite, 0, 380, 0, yrepeat=False),)
background = sge.Background(layers, 0xffffff)

circle = Circle(game.width // 2, game.height // 2)
objects = [circle]

views = (sge.View(0, 0),)

rm_0 = sge.Room(tuple(objects), views=views, background=background)


game.start()

