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
import math
import weakref

import pygame

import sge


__all__ = ['StellarClass', 'Mouse']


class StellarClass(object):

    """Class for game objects.

    All StellarClass objects have the following attributes:
        x: The horizontal position of the object in the room, where the
            left edge is 0 and x increases toward the right.
        y: The vertical position of the object in the room, where the
            top edge is 0 and y increases toward the bottom.
        z: The Z-axis position of the object in the room, which
            determines in what order objects are drawn; objects with a
            higher Z value are drawn in front of objects with a lower Z
            value.
        sprite: The sprite currently in use by this object.  Set to None
            for no (visible) sprite.  While it will always be an actual
            Sprite object or None when read, it can also be set to the
            ID of a sprite.
        visible: Whether or not the object should be drawn.
        detects_collisions: Whether or not the object should be involved
            in collisions.
        bbox_x: The horizontal location of the top-left corner of the
            bounding box in relation to x, where 0 is x and bbox_x
            increases toward the right.  If set to None, the value
            recommended by the sprite is used.
        bbox_y: The vertical location of the top-left corner of the
            bounding box in relation to y, where 0 is y and bbox_y
            increases toward the bottom.  If set to None, the value
            recommended by the sprite is used.
        bbox_width: The width of the bounding box in pixels.  If set to
            None, the value recommended by the sprite is used.
        bbox_height: The height of the bounding box in pixels.  If set
            to None, the value recommended by the sprite is used.
        collision_ellipse: Whether or not an ellipse (rather than a
            rectangle) should be used for collision detection.
        collision_precise: Whether or not precise (pixel-perfect)
            collision detection should be used.
        bbox_left: The position of the left side of the bounding box in
            the room (same as x + bbox_x).
        bbox_right: The position of the right side of the bounding box
            in the room (same as bbox_left + bbox_width).
        bbox_top: The position of the top side of the bounding box
            (same as y + bbox_y).
        bbox_bottom: The position of the bottom side of the bounding
            box (same as bbox_top + bbox_height).
        xvelocity: The velocity of the object toward the right.
        yvelocity: The velocity of the object toward the bottom.
        speed: The total (directional) speed of the object.
        move_direction: The direction of the object's movement in
            degrees, with 0 being directly to the right and rotation in
            a positive direction being counter-clockwise.  Default is 0.
        image_index: The animation frame currently being displayed, with
            0 being the first one.
        image_fps: The animation rate in frames per second.  If set to
            None, the value recommended by the sprite is used.
        image_xscale: The horizontal scale factor for the sprite.
        image_yscale: The vertical scale factor for the sprite.
        image_rotation: The rotation of the sprite, with rotation in a
            positive direction being counter-clockwise.
        image_alpha: The alpha value applied to the entire image, where
            255 is the original image, 128 is half the opacity of the
            original image, 0 is fully transparent, etc.
        image_blend: The color to blend with the sprite.  Set to None
            for no color blending.

    The following read-only attributes are also available:
        id: The unique identifier for this object.
        xstart: The initial value of x when the object was created.
        ystart: The initial value of y when the object was created.
        xprevious: The previous value of x.
        yprevious: The previous value of y.

    StellarClass methods:
        collides: Return whether or not this object collides with
            another.
        set_alarm: Set an alarm.
        get_alarm: Return the count on an alarm.
        destroy: Destroy the object.

    StellarClass events are handled by special methods.  The exact
    timing of their calling is implementation-dependent except where
    otherwise noted.  The methods are:
        event_create: Called when the object is created.  It is always
            called after any room start events occurring at the same
            time.
        event_destroy: Destroy event.
        event_step: Called once each frame.
        event_alarm: Called when an alarm counter reaches 0.
        event_animation_end: Called when an animation cycle ends.
        event_key_press: Key press event.
        event_key_release: Key release event.
        event_mouse_move: Mouse move event.
        event_mouse_button_press: Mouse button press event.
        event_mouse_button_release: Mouse button release event.
        event_joystick_axis_move: Joystick axis move event.
        event_joystick_hat_move: Joystick HAT move event.
        event_joystick_button_press: Joystick button press event.
        event_joystick_button_release: Joystick button release event.
        event_close: Close event (e.g. close button).
        event_collision: Middle/default collision event.
        event_collision_left: Left collision event.
        event_collision_right: Right collision event.
        event_collision_top: Top collision event.
        event_collision_bottom: Bottom collision event.

    The following alternative events are executed when the game is
    paused in place of the corresponding normal events:
        event_paused_key_press
        event_paused_key_release
        event_paused_mouse_move
        event_paused_mouse_button_press
        event_paused_mouse_button_release
        event_paused_joystick_axis_move
        event_paused_joystick_hat_move
        event_paused_joystick_button_press
        event_paused_joystick_button_release

    """

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self.xprevious = self._x
        self._x = value
        self._bbox_left = value + self.bbox_x
        self._bbox_right = self.bbox_left + self.bbox_width

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self.yprevious = self._y
        self._y = value
        self._bbox_top = value + self.bbox_y
        self._bbox_bottom = self.bbox_top + self.bbox_height

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value
        if self._pygame_sprite in sge.game._pygame_sprites:
            self._pygame_sprite.kill()
            sge.game._pygame_sprites.add(self._pygame_sprite, layer=self._z)

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value):
        if isinstance(value, sge.Sprite) or value is None:
            self._sprite = value
        else:
            self._sprite = sge.game.sprites[value]

    @property
    def detects_collisions(self):
        return self._detects_collisions

    @detects_collisions.setter
    def detects_collisions(self, value):
        self._detects_collisions = value
        position = None
        for i in xrange(len(sge.game._colliders)):
            if sge.game._colliders[i]() is self:
                position = i
                break

        if self._detects_collisions:
            if position is None:
                sge.game._colliders.append(weakref.ref(self))
        else:
            if position is not None:
                del sge.game._colliders[position]

    @property
    def collision_ellipse(self):
        return self._collision_ellipse

    @collision_ellipse.setter
    def collision_ellipse(self, value):
        if value != self._collision_ellipse:
            self._collision_ellipse = value
            self._set_mask()

    @property
    def collision_precise(self):
        return self._collision_precise

    @collision_precise.setter
    def collision_precise(self, value):
        if value != self._collision_precise:
            self._collision_precise = value
            self._set_mask()

    @property
    def bbox_left(self):
        return self._bbox_left

    @bbox_left.setter
    def bbox_left(self, value):
        self.xprevious = self._x
        self._bbox_left = value
        self._bbox_right = value + self.bbox_width
        self._x = value - self.bbox_x

    @property
    def bbox_right(self):
        return self._bbox_right

    @bbox_right.setter
    def bbox_right(self, value):
        self.xprevious = self._x
        self._bbox_right = value
        self._bbox_left = value - self.bbox_width
        self._x = self.bbox_left - self.bbox_x

    @property
    def bbox_top(self):
        return self._bbox_top

    @bbox_top.setter
    def bbox_top(self, value):
        self.yprevious = self._y
        self._bbox_top = value
        self._bbox_bottom = value + self.bbox_height
        self._y = value - self.bbox_y

    @property
    def bbox_bottom(self):
        return self._bbox_bottom

    @bbox_bottom.setter
    def bbox_bottom(self, value):
        self.yprevious = self._y
        self._bbox_bottom = value
        self._bbox_top = value - self.bbox_height
        self._y = self.bbox_top - self.bbox_y

    @property
    def xvelocity(self):
        return self._xvelocity

    @xvelocity.setter
    def xvelocity(self, value):
        self._xvelocity = value
        self._set_speed()

    @property
    def yvelocity(self):
        return self._yvelocity

    @yvelocity.setter
    def yvelocity(self, value):
        self._yvelocity = value
        self._set_speed()

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value
        self._xvelocity = math.cos(radians(self.move_direction)) * value
        self._yvelocity = math.sin(radians(self.move_direction)) * value

    @property
    def move_direction(self):
        return self._move_direction

    @move_direction.setter
    def move_direction(self, value):
        self._move_direction = value
        self._xvelocity = math.cos(radians(value)) * self.speed
        self._yvelocity = math.sin(radians(value)) * self.speed

    @property
    def image_index(self):
        return self._image_index

    @image_index.setter
    def image_index(self, value):
        if self.sprite is not None:
            self._image_index = value
            while self._image_index >= len(self.sprite._images):
                self._image_index -= len(self.sprite._images)
                self.event_animation_end()
        else:
            self._image_index = 0

    @property
    def image_fps(self):
        return self._fps

    @image_fps.setter
    def image_fps(self, value):
        self._fps = abs(value)
        if self._fps != 0:
            self._frame_time = 1000 / self._fps
            if not self._frame_time:
                # This would be caused by a round-off to 0 resulting
                # from a much too high frame rate.  It would cause a
                # division by 0 later, so this is meant to prevent that.
                self._frame_time = 0.01
        else:
            self._frame_time = None

    def __init__(self, x, y, z, id_=None, sprite=None, visible=True,
                 detects_collisions=True, bbox_x=None, bbox_y=None,
                 bbox_width=None, bbox_height=None, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 image_index=0, image_fps=0, image_xscale=1, image_yscale=1,
                 image_rotation=0, image_alpha=255, image_blend=None,
                 **kwargs):
        """Create a new StellarClass object.

        Arguments set the properties of the object.  See
        StellarClass.__doc__ for more information.

        If bbox_x, bbox_y, bbox_width, or bbox_height is None, the
        respective argument will be determined by the sprite's suggested
        bounding box.

        If ``id`` is None, it will be set to an integer not currently
        used as an ID (the exact number chosen is implementation-
        specific and may not necessarily be the same between runs).

        A game object must exist before an object of this class is
        created.

        """
        # Since the docs say that ``id`` is a valid keyword argument,
        # you should do this to make sure that that is true.
        id_ = kwargs.setdefault('id', id_)

        self.xstart = x
        self.ystart = y
        self.xprevious = x
        self.yprevious = y

        self.sprite = sprite
        self.visible = visible
        self.detects_collisions = detects_collisions
        if self.sprite is not None:
            sprite_bbox_x = self.sprite.bbox_x
            sprite_bbox_y = self.sprite.bbox_y
            sprite_bbox_width = self.sprite.bbox_width
            sprite_bbox_height = self.sprite.bbox_height
        else:
            sprite_bbox_x = 0
            sprite_bbox_y = 0
            sprite_bbox_width = 1
            sprite_bbox_height = 1
        self.bbox_x = bbox_x if bbox_x is not None else sprite_bbox_x
        self.bbox_y = bbox_y if bbox_y is not None else sprite_bbox_y
        self.bbox_width = (bbox_width if bbox_width is not None else
                           sprite_bbox_width)
        self.bbox_height = (bbox_height if bbox_height is not None else
                            sprite_bbox_height)
        self._collision_ellipse = collision_ellipse
        self._collision_precise = collision_precise

        if id_ is not None:
            self.id = id_
        else:
            id_ = 0
            while id_ in sge.game.objects:
                id_ += 1
            self.id = id_

        sge.game.objects[self.id] = self

        self._x = x
        self._y = y
        self._z = z
        self._xvelocity = 0
        self._yvelocity = 0
        self._move_direction = 0
        self._speed = 0
        self.xvelocity = xvelocity
        self.yvelocity = yvelocity
        self._anim_count = 0
        self.image_index = image_index
        self.image_fps = (self.sprite.fps if self.sprite is not None else
                          image_fps)
        self.image_xscale = image_xscale
        self.image_yscale = image_yscale
        self.image_rotation = image_rotation
        self.image_alpha = image_alpha
        self.image_blend = image_blend

        self._alarms = {}

        self._rect = pygame.Rect(self.bbox_x, self.bbox_y, self.bbox_width,
                                 self.bbox_height)
        self._pygame_sprite = _PygameSprite(self)
        self._set_mask()

        self.x = x
        self.y = y
        self.z = z

        self._start_x = self.x
        self._start_y = self.y
        self._start_z = self.z
        self._start_sprite = self.sprite
        self._start_visible = self.visible
        self._start_detects_collisions = self.detects_collisions
        self._start_bbox_x = self.bbox_x
        self._start_bbox_y = self.bbox_y
        self._start_bbox_width = self.bbox_width
        self._start_bbox_height = self.bbox_height
        self._start_collision_ellipse = self.collision_ellipse
        self._start_collision_precise = self.collision_precise

    def collides(self, other, x=None, y=None):
        """Return whether or not this object collides with another.

        ``other`` indicates the object to check for a collision with, or
        the name of said object.  ``other`` can also be a class to check
        for collisions with.

        ``x`` and ``y`` indicate the position to check for collisions
        at.  If unspecified or None, this object's current position will
        be used.

        """
        if isinstance(other, StellarClass):
            others = [other]
        else:
            others = []
            for ref in sge.game._colliders:
                if isinstance(obj(), other):
                    others.append(obj())

        if x is None:
            x = self.x
        if y is None:
            y = self.y

        # Change x and y to be offset values; these are easier to use.
        x -= self.x
        y -= self.y

        for other in others:
            if (self.collision_precise or self.collision_ellipse or
                    other.collision_precise or other.collision_ellipse):
                # Use masks.
                self_rect = pygame.Rect(round(self.bbox_left + x),
                                        round(self.bbox_top + y),
                                        self.bbox_width, self.bbox_height)
                other_rect = pygame.Rect(round(other.bbox_left),
                                         round(other.bbox_top),
                                         other.bbox_width, other.bbox_height)
                collide_rect = self_rect.clip(other_rect)

                self_xoffset = collide_rect.left - self_rect.left
                self_yoffset = collide_rect.top - self_rect.top
                other_xoffset = collide_rect.left - other_rect.left
                other_yoffset = collide_rect.top - other_rect.top

                for a in xrange(collide_rect.w):
                    for b in xrange(collide_rect.h):
                        if (self._hitmask[
                                a + self_xoffset][b + self_yoffset] and
                            other._hitmask[
                                a + other_xoffset][b + other_yoffset]):
                            return True

                return False
                        
            else:
                # Use bounding boxes.
                return (self.bbox_left + x < other.bbox_right and
                        self.bbox_right + x > other.bbox_left and
                        self.bbox_top + y < other.bbox_bottom and
                        self.bbox_bottom + y > other.bbox_top)

    def set_alarm(self, alarm_id, value):
        """Set an alarm.

        Set the alarm with the given ``alarm_id`` with the given
        ``value``.  The alarm will then reduce by 1 each frame until it
        reaches 0 and set off the alarm event with the same ID.
        ``alarm_id`` can be any value.  ``value`` should be a number
        greater than 0.  You can also set ``value`` to None to disable
        the alarm.

        """
        if value is not None:
            self._alarms[alarm_id] = value
        elif alarm_id in self._alarms:
            del self._alarms[alarm_id]

    def get_alarm(self, alarm_id):
        """Return the count on an alarm.

        Get the number of frames before the alarm with ``alarm_id`` will
        go off.  If the alarm has not been set, None will be returned.

        """
        if alarm_id in self._alarms:
            return self._alarms[alarm_id]
        else:
            return None

    def destroy(self):
        """Destroy the object."""
        self.event_destroy()
        self._pygame_sprite.kill()
        del sge.game.objects[self.id]

        for room in sge.game.rooms:
            new_objects = []
            for obj in room.objects:
                if obj is not self:
                    new_objects.append(obj)
            room.objects = tuple(new_objects)

    def event_create(self):
        """Create event.

        Called when the object is created.  It is always called after
        any room start events occurring at the same time.

        """
        pass

    def event_destroy(self):
        """Destroy event."""
        pass

    def event_step(self, time_passed):
        """Step event.

        Called once each frame.  ``time_passed`` is the number of
        milliseconds that have passed during the last frame.

        """
        pass

    def event_alarm(self, alarm_id):
        """Alarm event.

        Called when an alarm counter reaches 0.  ``alarm_id`` is the ID
        of the alarm that was set off.

        """
        pass

    def event_animation_end(self):
        """Animation End event.

        Called when an animation cycle ends.

        """
        pass

    def event_key_press(self, key):
        """Key press event.

        ``key`` is the key that was pressed.

        """
        pass

    def event_key_release(self, key):
        """Key release event.

        ``key`` is the key that was pressed.

        """
        pass

    def event_mouse_move(self, x, y):
        """Mouse move event.

        ``x`` and ``y`` indicate the relative movement of the mouse.

        """
        pass

    def event_mouse_button_press(self, button):
        """Mouse button press event.

        ``button`` is the number of the mouse button that was pressed;
        these numbers may vary by implementation, so MOUSE_BUTTON_*
        constants should be used.

        """
        pass

    def event_mouse_button_release(self, button):
        """Mouse button release event.

        ``button`` is the number of the mouse button that was released;
        these numbers may vary by implementation, so MOUSE_BUTTON_*
        constants should be used.

        """
        pass

    def event_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``axis`` is the number of the axis, where 0 is the
        first axis.  ``value`` is the tilt of the axis, where 0 is in
        the center, -1 is tilted all the way to the left or up, and 1 is
        tilted all the way to the right or down.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``hat`` is the number of the HAT, where 0 is the
        first HAT.  ``x`` and ``y`` indicate the position of the HAT,
        where 0 is in the center, -1 is left or up, and 1 is right or
        down.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_button_press(self, joystick, button):
        """Joystick button press event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``button`` is the number of the button pressed, where
        0 is the first button.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_button_release(self, joystick, button):
        """Joystick button release event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``button`` is the number of the button pressed, where
        0 is the first button.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_collision(self, other):
        """Middle/default collision event."""
        pass

    def event_collision_left(self, other):
        """Left collision event."""
        self.event_collision(other)

    def event_collision_right(self, other):
        """Right collision event."""
        self.event_collision(other)

    def event_collision_top(self, other):
        """Top collision event."""
        self.event_collision(other)

    def event_collision_bottom(self, other):
        """Bottom collision event."""
        self.event_collision(other)

    def event_paused_key_press(self, key):
        """Key press event when paused.

        See StellarClass.event_key_press.__doc__ for more information.

        """
        pass

    def event_paused_key_release(self, key):
        """Key release event when paused.

        See StellarClass.event_key_release.__doc__ for more information.

        """
        pass

    def event_paused_mouse_move(self, x, y):
        """Mouse move event when paused.

        See StellarClass.event_mouse_move.__doc__ for more information.

        """
        pass

    def event_paused_mouse_button_press(self, button):
        """Mouse button press event when paused.

        See StellarClass.event_mouse_button_press.__doc__ for more
        information.

        """
        pass

    def event_paused_mouse_button_release(self, button):
        """Mouse button release event when paused.

        See StellarClass.event_mouse_button_release.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event when paused.

        See StellarClass.event_joystick_axis_move.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event when paused.

        See StellarClass.event_joystick_hat_move.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_button_press(self, joystick, button):
        """Joystick button press event when paused.

        See StellarClass.event_joystick_button_press.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_button_release(self, joystick, button):
        """Joystick button release event when paused.

        See StellarClass.event_joystick_button_release.__doc__ for more
        information.

        """
        pass

    @classmethod
    def create(cls, *args, **kwargs):
        """Create an object of this class in the current room.

        ``args`` and ``kwargs`` are passed to ``cls`` as arguments.
        Calling this class method is the same as:
            sge.game.current_room.add(cls(*args, **kwargs))

        """
        sge.game.current_room.add(cls(*args, **kwargs))

    def _update(self, time_passed, delta_mult):
        # Update this object (should be called each frame).
        # Update the animation frame.
        if self.image_fps:
            self._anim_count += time_passed
            self.image_index += int(self._anim_count // self._frame_time)
            self._anim_count %= self._frame_time

        # Alarms
        for a in self._alarms:
            self._alarms[a] -= delta_mult
            if self._alarms[a] <= 0:
                del self._alarms[a]
                self.event_alarm(a)

        # Movement
        if self.xvelocity or self.yvelocity:
            if self.id != "mouse":
                self.x += self.xvelocity * delta_mult
                self.y += self.yvelocity * delta_mult

            # Detect collisions
            if self.detects_collisions:
                for other_ref in sge.game._colliders:
                    if other_ref() is not None:
                        other = other_ref()
                    else:
                        continue

                    if self.collides(other):
                        xcollision = not self.collides(other, x=self.xprevious)
                        ycollision = not self.collides(other, y=self.yprevious)

                        if xcollision and ycollision:
                            # Corner collision; determine
                            # direction by distance.
                            if self.xvelocity > 0:
                                xdepth = (self.bbox_right - other.bbox_left)
                            else:
                                xdepth = (other.bbox_right - self.bbox_left)

                            if self.yvelocity > 0:
                                ydepth = (self.bbox_bottom - other.bbox_top)
                            else:
                                ydepth = (other.bbox_bottom - self.bbox_top)

                            if xdepth > ydepth:
                                if self.xvelocity > 0:
                                    self.event_collision_right(other)
                                    other.event_collision_left(self)
                                else:
                                    self.event_collision_left(other)
                                    other.event_collision_right(self)
                            else:
                                if self.yvelocity > 0:
                                    self.event_collision_bottom(other)
                                    other.event_collision_top(self)
                                else:
                                    self.event_collision_top(other)
                                    other.event_collision_bottom(self)

                        elif xcollision:
                            # Horizontal collision only.
                            if self.xvelocity > 0:
                                self.event_collision_right(other)
                                other.event_collision_left(self)
                            else:
                                self.event_collision_left(other)
                                other.event_collision_right(self)

                        elif ycollision:
                            # Vertical collision only.
                            if self.yvelocity > 0:
                                self.event_collision_bottom(other)
                                other.event_collision_top(self)
                            else:
                                self.event_collision_top(other)
                                other.event_collision_bottom(self)

                        elif not self.collides(other, self.xprevious,
                                               self.yprevious):
                            # Wedge collision (both vertical and
                            # horizontal collisions).
                            if self.xvelocity > 0:
                                self.event_collision_right(other)
                                other.event_collision_left(self)
                            else:
                                self.event_collision_left(other)
                                other.event_collision_right(self)
                            if self.yvelocity > 0:
                                self.event_collision_bottom(other)
                                other.event_collision_top(self)
                            else:
                                self.event_collision_top(other)
                                other.event_collision_bottom(self)

                        else:
                            # No directional collision; this is
                            # a continuous collision.
                            self.event_collision(other)
                            other.event_collision(self)

    def _set_mask(self):
        # Properly set the hit mask based on the collision settings.
        if self.collision_precise:
            # Mask based on opacity of the current image.
            left = self.bbox_x + self.sprite.origin_x
            right = left + self.bbox_width
            top = self.bbox_y + self.sprite.origin_y
            bottom = top + self.bbox_height

            mask = self.sprite._get_precise_mask(self.image_index)[left:right]
            for i in xrange(len(mask)):
                mask[i] = mask[i][top:bottom]

            self._hitmask = mask
        elif self.collision_ellipse:
            # Elliptical mask based on bounding box.
            self._hitmask = [[False for y in xrange(self.bbox_height)]
                             for x in xrange(self.bbox_width)]
            a = len(self._hitmask) / 2
            b = len(self._hitmask[0]) / 2
            for x in xrange(len(self._hitmask)):
                for y in xrange(len(self._hitmask[x])):
                    if ((x - a) / a) ** 2 + ((y - b) / b) ** 2 <= 1:
                        self._hitmask[x][y] = True
        else:
            # Mask is all pixels in the bounding box.
            self._hitmask = [[True for y in xrange(self.bbox_height)]
                             for x in xrange(self.bbox_width)]

    def _set_speed(self):
        # Set the speed and move direction based on xvelocity and
        # yvelocity.
        self._speed = math.sqrt(self._xvelocity ** 2 + self._yvelocity ** 2)

        if self._yvelocity == 0:
            base_angle = 0
        elif self._xvelocity == 0:
            base_angle = 90
        else:
            base_angle = math.degrees(math.atan(abs(self._yvelocity) /
                                                abs(self._xvelocity)))

        if self._xvelocity < 0 and self._yvelocity < 0:
            self._move_direction += 180
        elif self._xvelocity < 0:
            self._move_direction = 180 - base_angle
        elif self._yvelocity < 0:
            self._move_direction = 360 - base_angle
        else:
            self._move_direction = base_angle

        self._move_direction %= 360

    def _reset(self):
        # Reset the object back to its original state.
        self.x = self._start_x
        self.y = self._start_y
        self.z = self._start_z
        self.sprite = self._start_sprite
        self.visible = self._start_visible
        self.detects_collisions = self._start_detects_collisions
        self.bbox_x = self._start_bbox_x
        self.bbox_y = self._start_bbox_y
        self.bbox_width = self._start_bbox_width
        self.bbox_height = self._start_bbox_height
        self.collision_ellipse = self._start_collision_ellipse
        self.collision_precise = self._start_collision_precise


class Mouse(StellarClass):

    @property
    def x(self):
        if sge.game.current_room is not None:
            mouse_x = self.mouse_x / sge.game._xscale
            mouse_y = self.mouse_y / sge.game._yscale
            for view in sge.game.current_room.views:
                if (view.xport <= mouse_x <= view.xport + view.width and
                        view.yport <= mouse_y <= view.yport + view.height):
                    # We save this value so that if the mouse is in none of
                    # the views, the last known position in a view is used.
                    self._x = mouse_x - view.x
                    break

            return self._x
        else:
            return 0

    @x.setter
    def x(self, value):
        rel_x = (value - self.x) * sge.game._xscale
        self.mouse_x += rel_x

        self.xprevious = self._x
        self._x = value
        self._bbox_left = value + self.bbox_x
        self._bbox_right = self.bbox_left + self.bbox_width

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

        pygame.mouse.set_pos(self.mouse_x, self.mouse_y)

    @property
    def y(self):
        if sge.game.current_room is not None:
            mouse_x = self.mouse_x / sge.game._xscale
            mouse_y = self.mouse_y / sge.game._yscale
            for view in sge.game.current_room.views:
                if (view.xport <= mouse_x <= view.xport + view.width and
                        view.yport <= mouse_y <= view.yport + view.height):
                    # We save this value so that if the mouse is in none of
                    # the views, the last known position in a view is used.
                    self._y = mouse_y - view.y
                    break

            return self._y
        else:
            return 0

    @y.setter
    def y(self, value):
        rel_y = (value - self.y) * sge.game._yscale
        self.mouse_y += rel_y

        self.yprevious = self._y
        self._y = value
        self._bbox_top = value + self.bbox_y
        self._bbox_bottom = self.bbox_top + self.bbox_height

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

        pygame.mouse.set_pos(self.mouse_x, self.mouse_y)

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value):
        if isinstance(value, sge.Sprite) or value is None:
            self._sprite = value
        else:
            self._sprite = sge.game.sprites[value]

        self.set_cursor()

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value
        self.set_cursor()

    def __init__(self):
        self._visible = True
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.mouse_xprevious = self.mouse_x
        self.mouse_yprevious = self.mouse_y
        self.previous_speeds = []
        super(Mouse, self).__init__(0, 0, 0, id='mouse')

    def event_collision(self, other):
        sge.game.event_mouse_collision(other)

    def event_collision_left(self, other):
        sge.game.event_mouse_collision_left(other)

    def event_collision_right(self, other):
        sge.game.event_mouse_collision_right(other)

    def event_collision_top(self, other):
        sge.game.event_mouse_collision_top(other)

    def event_collision_bottom(self, other):
        sge.game.event_mouse_collision_bottom(other)

    def _update(self, time_passed, delta_mult):
        self.update_speed(time_passed)
        super(Mouse, self)._update(time_passed, delta_mult)

    def update_speed(self, time_passed):
        # Update the speed variables.  ``time_passed`` is the number of
        # milliseconds since the last speed update.
        self.previous_speeds.insert(0, (self.mouse_x - self.mouse_xprevious,
                                        self.mouse_y - self.mouse_yprevious,
                                        time_passed))
        time = 0
        num_steps = 0
        total_xvelocity = 0
        total_yvelocity = 0

        for speed in self.previous_speeds:
            time += speed[2]
            if time <= 250:
                num_steps += 1
                total_xvelocity += speed[0]
                total_yvelocity += speed[1]

        self.previous_speeds = self.previous_speeds[:num_steps]

        if num_steps > 0:
            self.xvelocity = total_xvelocity / num_steps
            self.yvelocity = total_yvelocity / num_steps
        else:
            self.xvelocity = 0
            self.yvelocity = 0

        self.mouse_xprevious = self.mouse_x
        self.mouse_yprevious = self.mouse_y
        self.xprevious = self.x
        self.yprevious = self.y

    def set_cursor(self):
        # Set the mouse cursor and visibility state.
        if not sge.game.grab_input:
            pygame.mouse.set_visible(self.visible and self.sprite is None)
        else:
            pygame.mouse.set_visible(False)


class _PygameSprite(pygame.sprite.DirtySprite):

    # Handles drawing in this implementation.
    #
    # Scaling is handled transparently in the update method, which is
    # always called before drawing.  Everything else is the
    # responsibility of StellarClass, including animation (the current
    # frame is grabbed from the _image attribute of the parent object).

    def __init__(self, parent, *groups):
        # See pygame.sprite.DirtySprite.__init__.__doc__.  ``parent``
        # is a StellarClass object that this object belongs to.
        super(_PygameSprite, self).__init__(*groups)
        self.parent = weakref.ref(parent)
        self.image = pygame.Surface((1, 1))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x_offset = 0
        self.y_offset = 0

    def update(self):
        if self.parent() is not None:
            parent = self.parent()
            if parent.sprite is not None:
                new_image = parent.sprite._get_image(
                    parent.image_index, parent.image_xscale,
                    parent.image_yscale, parent.image_rotation,
                    parent.image_alpha, parent.image_blend)
                if self.image is not new_image:
                    self.must_redraw = False
                    self.image = new_image
                    self.dirty = 1

                    if parent.image_rotation % 90 != 0:
                        # Be prepared for size adjustment
                        rot_size = self.image.get_size()
                        reg_size = parent.sprite._get_image(
                            parent.image_index, parent.image_xscale,
                            parent.image_yscale).get_size()
                        self.x_offset = (rot_size[0] - reg_size[0]) // 2
                        self.y_offset = (rot_size[1] - reg_size[1]) // 2
                    else:
                        self.x_offset = 0
                        self.y_offset = 0

                if self.visible != self.parent().visible:
                    self.visible = int(self.parent().visible)
                    self.dirty = 1

                self.update_rect(parent.x, parent.y, parent.z, parent.sprite)
            else:
                self.image = pygame.Surface((1, 1))
                self.image.set_colorkey((0, 0, 0))
                self.dirty = 1
        else:
            self.kill()

    def update_rect(self, x, y, z, sprite):
        # Update the rect of this Pygame sprite, based on the SGE sprite
        # and coordinates given.  This involves creating "proxy"
        # one-time sprites for multiple views if necessary.
        views = sge.game.current_room.views
        if (len(views) == 1 and views[0].xport == 0 and views[0].yport == 0 and
                views[0].width == sge.game.width and
                views[0].height == sge.game.height):
            # There is only one view that takes up the whole screen, so
            # we don't need to worry about it.
            x = x - views[0].x - sprite.origin_x
            y = y - views[0].y - sprite.origin_y
            new_rect = self.image.get_rect()
            new_rect.left = (round(x * sge.game._xscale) - self.x_offset +
                             sge.game._x)
            new_rect.top = (round(y * sge.game._yscale) - self.y_offset +
                            sge.game._y)

            if self.rect != new_rect:
                self.rect = new_rect
                self.dirty = 1
        else:
            # There is something more complicated.  Have to account for
            # the possibility of edges or multiple appearances.
            original_used = False
            self.dirty = 1
            real_x = x
            real_y = y
            for view in views:
                x = real_x - view.x - sprite.origin_x + view.xport
                y = real_y - view.y - sprite.origin_y + view.yport
                w = max(1, self.image.get_width())
                h = max(1, self.image.get_height())
                new_rect = self.image.get_rect()
                new_rect.left = (round(x * sge.game._xscale) - self.x_offset +
                                 sge.game._x)
                new_rect.top = (round(y * sge.game._yscale) - self.y_offset +
                                sge.game._y)
                inside_view = (x >= view.xport and
                               x + w <= view.xport + view.width and
                               y >= view.yport and
                               y + h <= view.yport + view.height)
                within_view = (x + w >= view.xport and
                               x <= view.xport + view.width and
                               y + h >= view.yport and
                               y <= view.yport + view.height)

                if not original_used and inside_view:
                    original_used = True
                    if self.rect == new_rect:
                        self.dirty = 0
                    else:
                        self.rect = new_rect
                elif within_view:
                    if inside_view:
                        img = self.image
                        rect = new_rect
                    else:
                        # Make a cut-off version of the sprite and
                        # adjust the rect accordingly.
                        if x < view.xport:
                            cut_x = view.xport - x
                            x = view.xport
                            w -= cut_x
                        else:
                            cut_x = 0

                        if x + w > view.xport + view.width:
                            w -= (x + w) - (view.xport + view.width)

                        if y < view.yport:
                            cut_y = view.yport - y
                            y = view.yport
                            h -= cut_y
                        else:
                            cut_y = 0

                        if y + h > view.yport + view.height:
                            h -= (y + h) - (view.yport + view.height)

                        x = round(x * sge.game._xscale) - self.x_offset
                        y = round(y * sge.game._yscale) - self.y_offset
                        cut_x = round(cut_x * sge.game._xscale)
                        cut_y = round(cut_y * sge.game._yscale)
                        w = round(w * sge.game._xscale)
                        h = round(h * sge.game._yscale)
                        cut_rect = pygame.Rect(cut_x, cut_y, w, h)
                        img = self.image.subsurface(cut_rect)
                        rect = pygame.Rect(x, y, w, h)

                    # Create proxy one-time sprite
                    proxy = _PygameOneTimeSprite(img, rect)
                    sge.game._pygame_sprites.add(proxy, layer=z)

            if not original_used:
                self.image = pygame.Surface((1, 1))
                self.image.set_colorkey((0, 0, 0))


class _PygameOneTimeSprite(pygame.sprite.DirtySprite):

    # A regular DirtySprite that only displays once, and then destroys
    # itself.

    def __init__(self, image, rect, *groups):
        super(_PygameOneTimeSprite, self).__init__(*groups)
        self.image = image
        self.rect = rect
        self.dirty = 1

    def update(self):
        if not self.dirty:
            self.kill()
