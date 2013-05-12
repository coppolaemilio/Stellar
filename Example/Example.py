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
        


class obj_1(sge.StellarClass):
    def __init__(self, x, y, player=0):
        super(obj_1, self).__init__(x, y, 5, sprite='spr_cancel', collision_precise=True)

class obj_cancel(sge.StellarClass):
    def __init__(self, x, y, player=0):
        super(obj_cancel, self).__init__(x, y, 5, sprite='spr_cancel', collision_precise=True)
    def event_create(self):
        self.velocidad = 3
        
    def event_step(self, time_passed):
        # Limit the circles to inside the room.
        if sge.get_key_pressed('right') :
            self.x+=self.velocidad
        if sge.get_key_pressed('left') :
            self.x-=self.velocidad
        if sge.get_key_pressed('down') :
            self.y+=self.velocidad
        if sge.get_key_pressed('up') :
            self.y-=self.velocidad
        
        for obj in sge.game.current_room.objects:
                    if (obj is not self and isinstance(obj, obj_cristal) and self.collides(obj)):
                        obj.destroy()
        		sge.StellarClass.create(obj_cristal, 32,32)
                        break

class obj_cristal(sge.StellarClass):
    def __init__(self, x, y, player=0):
        super(obj_cristal, self).__init__(x, y, 5, sprite='spr_cristal', collision_precise=True)


game = Game()
# Load sprites
spr_cancel_sprite = sge.Sprite('spr_cancel', transparent=True)
spr_cristal_sprite = sge.Sprite('spr_cristal', transparent=True)
fence_sprite = sge.Sprite('fence', transparent=True)


layers = (sge.BackgroundLayer(fence_sprite, 0, 380, 0, yrepeat=True),)
background = sge.Background(layers, 0xffffff)

circle = obj_cristal(game.width // 2, game.height // 2)
circle1= obj_cancel(20,20)
objects = [circle,circle1]


views = (sge.View(0, 0),)

rm_0 = sge.Room(tuple(objects), views=views, background=background)


game.start()

