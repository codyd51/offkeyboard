import collections
from typing import Optional

import keyboard

from keymaps import MinecraftMap
from note_utils import SILENCE_NOTE


class NoteReader:
    def __init__(self):
        self.ringbuf_size = 10
        self.last_notes = collections.deque(maxlen=self.ringbuf_size)
        self.last_pressed_note = None
        self.keymap = MinecraftMap()
        self.currently_held_key: Optional[str] = None

    def release_held_key(self):
        """Release the currently held key
        """
        if not self.currently_held_key:
            return
        print(f'Releasing key: {self.currently_held_key}')
        keyboard.release(self.currently_held_key)
        self.currently_held_key = None

    def hold_key(self, key: str) -> None:
        """Start holding down a key
        """
        if key == SILENCE_NOTE:
        if note == SILENCE_NOTE:
            return
        self.currently_held_key = key
        keyboard.press(key)

    def process_note(self, note: str):
        key = self.keymap.key_for_note(note)
        if key == self.currently_held_key:
            return

        # clean up the key we were just pressing
        self.release_held_key()

        # If this is a key that should be pressed until the note changes, do so
        if self.keymap.should_hold_key(key):
            print(f'{note}\tHolding down "{key}"')
            self.hold_key(key)
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
            return

        print(f'{note}\tPressing "{key}"')
        keyboard.send(key)
