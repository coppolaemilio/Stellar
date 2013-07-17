#!/usr/bin/env python

import sge
import os
#Imports


#Paths
sge.image_directories = [os.path.join('Sprites'),os.path.join('Backgrounds')]
sge.font_directories = [os.path.join('Fonts')]
sge.sound_directories = [os.path.join('Sounds')]
sge.music_directories = [os.path.join('Sounds')]


#Game Class
class Game(sge.Game):
    def event_key_press(self, key):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()
        
# Add Stellar objects



game = Game()
# Load sprites

# Rooms


game.start()

