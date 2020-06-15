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

    def hold_key(self, note: str, key_or_key_list: Union[str, List]) -> None:
        """Start holding down a key
        """
        if note == SILENCE_NOTE:
            return

        if isinstance(key_or_key_list, list):
            combo = "+".join(key_or_key_list)
            self.currently_held_key = combo
            # print(f'Holding key-combo {combo}')
            keyboard.press(combo)
        else:
            self.currently_held_key = key_or_key_list
            # print(f'Holding single-key {key_or_key_list}')
            keyboard.press(key_or_key_list)

    def process_note(self, note: str):
        key_or_key_list = self.keymap.key_for_note(note)

        if key_or_key_list is not None and key_or_key_list == self.currently_held_key:
            return
        if isinstance(key_or_key_list, list):
            combo = "+".join(key_or_key_list)
            if self.currently_held_key == combo:
                return

        # clean up the key we were just pressing
        self.release_held_key()

        if note == SILENCE_NOTE and self.currently_held_key in MOUSE_KEYS:
            VirtualMouse.clear()
            return

        # If this is a key that should be pressed until the note changes, do so
        if self.keymap.should_hold_key(key_or_key_list):
            print(f'{note}\tHolding down "{key_or_key_list}"')
            self.hold_key(note, key_or_key_list)
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

        key_or_key_list = self.keymap.key_for_note(note)
        if key_or_key_list is None:
            return

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

        if isinstance(key_or_key_list, list):
            combo = "+".join(key_or_key_list)
            print(f'{note}\tKey-combo {combo}')
            keyboard.send(combo)
        else:
            key = key_or_key_list
            print(f'{note}\tPressing "{key}"')
            keyboard.send(key)
