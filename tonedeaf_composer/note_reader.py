import collections
from typing import Optional, Union, List

import keyboard

from keymaps import MarioMap
from note_utils import SILENCE_NOTE
from mouse import (
    MOUSE_KEYS,
    MOUSE_LEFT_KEY,
    MOUSE_RIGHT_KEY,
    MOUSE_UP_KEY,
    MOUSE_DOWN_KEY,
    MOUSE_CLICK_KEY,
    VirtualMouse
)


class NoteReader:
    def __init__(self):
        self.ringbuf_size = 10
        self.last_notes = collections.deque(maxlen=self.ringbuf_size)
        self.last_pressed_note = None
        self.keymap = MarioMap()
        self.currently_held_key: Optional[str] = None

    def release_held_key(self):
        """Release the currently held key
        """
        if not self.currently_held_key:

            return
        print(f'Releasing key: {self.currently_held_key}')
        if self.currently_held_key not in MOUSE_KEYS:
            keyboard.release(self.currently_held_key)
        else:
            VirtualMouse.clear()
        self.currently_held_key = None

    def hold_key(self, note: str, key: str) -> None:
        """Start holding down a key
        """
        if note == SILENCE_NOTE:
            return
        self.currently_held_key = key
        keyboard.press(key)

    def process_note(self, note: str):
        key = self.keymap.key_for_note(note)
        if not key:
            print(f'unmapped note {note}')
        if key and key == self.currently_held_key:
            return

        # clean up the key we were just pressing
        self.release_held_key()

        if note == SILENCE_NOTE and self.currently_held_key in MOUSE_KEYS:
            VirtualMouse.clear()
            return

        # If this is a key that should be pressed until the note changes, do so
        if self.keymap.should_hold_key(key):
            print(f'{note}\tHolding down "{key}"')
            self.hold_key(note, key)
            return

        self.last_notes.append(note)
        # should we register this note?
        # If most of the notes in the ringbuffer are the same note, and this note is different from the last detected
        # note, do a state transition
        if self.last_notes.count(note) > 3 and note != self.last_pressed_note:
            # fill the entire buffer with whatever we just registered
            for _ in range(self.ringbuf_size):
                self.last_notes.append(note)
            self.quick_press_key_for_note(note)

    def quick_press_key_for_note(self, note: str):
        self.last_pressed_note = note

        key = self.keymap.key_for_note(note)
        if not key:
        # Mouse keys are handled separately
        if key_or_key_list in MOUSE_KEYS:
            key = key_or_key_list
            print(f'Ignoring mouse event: {key}')
            return

            print(f'got a mouse event: {key}')
            self.currently_held_key = key
            if key == MOUSE_LEFT_KEY:
                VirtualMouse.hold_left()
            elif key == MOUSE_RIGHT_KEY:
                VirtualMouse.hold_right()
            elif key == MOUSE_UP_KEY:
                VirtualMouse.hold_up()
            elif key == MOUSE_DOWN_KEY:
                VirtualMouse.hold_down()
            elif key == MOUSE_CLICK_KEY:
                self.currently_held_key = None
                VirtualMouse.left_click()
            return

        print(f'{note}\tPressing "{key}"')
        keyboard.send(key)
