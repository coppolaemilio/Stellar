# Stellar Game Engine - Pygame 1.9
# Copyright (C) 2012, 2013 Julian Marchant <onpon4@lavabit.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os

import pygame

import sge


__all__ = ['Sound']


class Sound(object):

    """Sound handling class.

    All Sound objects have the following attributes:
        volume: The volume of the sound in percent (0 for no sound, 100
            for max sound).
        balance: The balance of the sound effect on stereo speakers.  A
            value of 0 means centered (an equal amount of play on both
            speakers), -1 means entirely in the left speaker, and 1
            means entirely in the right speaker.  Support for this
            feature in Stellar Game Engine implementations is optional.
            If it is unavailable, all sounds will be played through both
            speakers equally (assuming stereo sound is used).
        max_play: The maximum instances of this sound playing permitted.
            Set to 0 for no limit.

    The following read-only attributes are also available:
        fname: The file name of the sound given when it was created.
            See Sound.__init__.__doc__ for more information.
        length: The length of the sound in milliseconds.
        playing: The number of instances of this sound playing.

    Sound methods:
        Sound.play: Play the sound.
        Sound.stop: Stop the sound.
        Sound.pause: Pause playback of the sound.
        Sound.unpause: Resume playback of the sound if paused.

    """

    @property
    def max_play(self):
        return len(self._channels)

    @max_play.setter
    def max_play(self, value):
        if self._sound is not None:
            value = max(0, value)
            while len(self._channels) < value:
                self._channels.append(sge.game._get_channel())
            while len(self._channels) > value:
                sge.game._release_channel(self._channels.pop(-1))

    @property
    def length(self):
        if self._sound is not None:
            return self._sound.get_length() * 1000
        else:
            return 0

    @property
    def playing(self):
        if self._sound is not None:
            return self._sound.get_num_channels()
        else:
            return 0

    def __init__(self, fname, volume=100, balance=0, max_play=1):
        """Create a new sound object.

        ``fname`` indicates the name of the sound file, to be located in
        one of the directories specified in ``sound_directories``.

        All remaining arguments set the initial properties of the sound.
        See Sound.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        self._sound = None

        if pygame.mixer.get_init():
            for path in sge.sound_directories:
                path = os.path.join(path, fname)
                try:
                    self._sound = pygame.mixer.Sound(path)
                    break
                except pygame.error:
                    pass

        self._channels = []
        self._temp_channels = []
        self.fname = fname
        self.volume = volume
        self.balance = balance
        self.max_play = max_play

    def play(self, loops=0, maxtime=None, fade_time=None):
        """Play the sound.

        ``loops`` indicates the number of extra times to play the sound
        after it is played the first time; set to -1 or None to loop
        indefinitely.  ``maxtime`` indicates the maximum amount of time
        to play the sound in milliseconds; set to 0 or None for no
        limit. ``fade_time`` indicates the time in milliseconds over
        which to fade the sound in; set to 0 or None to immediately play
        the sound at full volume.

        """
        if self._sound is not None:
            if loops is None:
                loops = -1
            if maxtime is None:
                maxtime = 0
            if fade_time is None:
                fade_time = 0

            if self.max_play:
                for channel in self._channels:
                    if not channel.get_busy():
                        channel.play(self._sound, loops, maxtime, fade_time)
                        break
                else:
                    self._channels[0].play(self._sound, loops, maxtime,
                                           fade_time)
            else:
                channel = sge.game._get_channel()
                channel.play(self._sound, loops, maxtime, fade_time)
                self._temp_channels.append(channel)

            # Clean up old temporary channels
            while (self._temp_channels and
                   not self._temp_channels[0].get_busy()):
                sge.game._release_channel(self._temp_channels.pop(0))

    def stop(self, fade_time=None):
        """Stop the sound.

        ``fade_time`` indicates the time in milliseconds over which to
        fade the sound out before stopping; set to 0 or None to
        immediately stop the sound.

        """
        if self._sound is not None:
            self._sound.stop()

    def pause(self):
        """Pause playback of the sound."""
        for channel in self._channels:
            channel.pause()

    def unpause(self):
        """Resume playback of the sound if paused."""
        for channel in self._channels:
            channel.unpause()

    @staticmethod
    def stop_all():
        """Stop playback of all sounds."""
        for i in sge.game.sounds:
            sge.game.sounds[i].stop()    
