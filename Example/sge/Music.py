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

import pygame

import sge


__all__ = ['Music']


class Music(object):

    """Music handling class.

    Music is mostly the same as sound, but only one can be played at a
    time.

    All Music objects have the following attributes:
        volume: The volume of the music in percent (0 for no sound, 100
            for max sound).
        balance: The balance of the music on stereo speakers.  A value
            of 0 means centered (an equal amount of play on both
            speakers), -1 means entirely in the left speaker, and 1
            means entirely in the right speaker.  Support for this
            feature in Stellar Game Engine implementations is optional.
            If it is unavailable, all music will be played through both
            speakers equally (assuming stereo sound is used).

    The following read-only attributes are also available:
        fname: The file name of the music given when it was created.
            See Music.__init__.__doc__ for more information.
        length: The length of the music in milliseconds.
        playing: Whether or not the music is playing.
        position: The current position (time) on the music in
            milliseconds.

    Music methods:
        Music.play: Play the music.
        Music.queue: Queue the music for playback.
        Music.stop: Stop the music.
        Music.pause: Pause playback of the music.
        Music.unpause: Resume playback of the music if paused.

    """

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = min(value, 100)

        if self.playing:
            pygame.mixer.music.set_volume(value / 100)

    @property
    def length(self):
        return self._length

    @property
    def playing(self):
        return sge.game._music is self and pygame.mixer.music.get_busy()

    @property
    def position(self):
        if self.playing:
            return self._start + pygame.mixer.music.get_pos()
        else:
            return 0

    def __init__(self, fname, volume=100, balance=0):
        """Create a new music object.

        ``fname`` indicates the name of the sound file, to be located in
        one of the directories specified in ``music_directories``.

        All remaining arguments set the initial properties of the music.
        See Music.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        self.fname = fname
        self.volume = volume
        self.balance = balance
        self._timeout = None
        self._fade_time = None
        self._start = 0

        self._full_fname = None
        if pygame.mixer.get_init():
            for path in sge.music_directories:
                path = os.path.join(path, fname)
                if os.path.isfile(path):
                    self._full_fname = path
                    break

    def play(self, start=0, loops=0, maxtime=None, fade_time=None):
        """Play the music.

        If music was already playing when this is called, it will be
        stopped.

        ``start`` indicates the number of milliseconds from the
        beginning to start at.  ``loops`` indicates the number of extra
        times to play the sound after it is played the first time; set
        to -1 or None to loop indefinitely.  ``maxtime`` indicates the
        maximum amount of time to play the sound in milliseconds; set to
        0 or None for no limit.  ``fade_time`` indicates the time in
        milliseconds over which to fade the sound in; set to 0 or None
        to immediately play the music at full volume.

        """
        if self._full_fname is not None:
            if not self.playing:
                pygame.mixer.music.load(self._full_fname)

            if loops is None:
                loops = -1

            sge.game._music = self
            self._timeout = maxtime
            self._fade_time = fade_time

            if self._fade_time > 0:
                pygame.mixer.music.set_volume(0)

            if self.fname.lower().endswith(".mod"):
                # MOD music is handled differently in Pygame: it uses
                # the pattern order number rather than the time to
                # indicate the start time.
                self._start = 0
                pygame.mixer.music.play(loops, start)
            else:
                self._start = start
                try:
                    pygame.mixer.music.play(loops, start / 1000)
                except NotImplementedError:
                    pygame.mixer.music.play(loops)

    def queue(self, start=0, loops=0, maxtime=None, fade_time=None):
        """Queue the music for playback.

        This will cause the music to be added to a list of music to play
        in order, after the previous music has finished playing.

        See Music.play.__doc__ for information about the arguments.

        """
        sge.game._music_queue.append((self, start, loops, maxtime, fade_time))

    def stop(self, fade_time=None):
        """Stop the music.

        ``fade_time`` indicates the time in milliseconds over which to
        fade the sound out before stopping; set to 0 or None to
        immediately stop the music.

        """
        if self.playing:
            if fade_time:
                pygame.mixer.music.fadeout(fade_time)
            else:
                pygame.mixer.music.stop()

    def pause(self):
        """Pause playback of the music."""
        if self.playing:
            pygame.mixer.music.pause()

    def unpause(self):
        """Resume playback of the music if paused."""
        if self.playing:
            pygame.mixer.music.unpause()

    @staticmethod
    def clear_queue():
        """Clear the music queue."""
        sge.game._music_queue = []

    @staticmethod
    def stop_all():
        """Stop playback of any music and clear the queue."""
        for i in sge.game.music:
            sge.game.music[i].stop()

        Music.clear_queue()
