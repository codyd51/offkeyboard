from typing import List


class Keymap:
    def __init__(self, notes: List[str], keys: List[str], held_keys: List[str] = None):
        self.keymap = dict(zip(notes, keys))
        if not held_keys:
            held_keys = []
        self.held_keys = held_keys

    def key_for_note(self, note: str):
        if note not in self.keymap:
            return None
        return self.keymap[note]

    def should_hold_key(self, key: str) -> bool:
        """When this key is registered, should it be quickly pressed and released, or held until explicitly released?
        """
        return key in self.held_keys


class Keymap1(Keymap):
    def __init__(self):
        notes = [
            'E2', 'F2', 'F#2', 'G2', 'G#2',
            'A2', 'A#2', 'B2', 'C3', 'C#3',
            'D3', 'D#3', 'E3', 'F3', 'F#3',
            'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4'
        ]
        keys = [
            'E', 'T', 'A', 'O', 'I',
            'N', 'S', 'R', 'H', 'D',
            'L', 'U', 'C', 'M', 'F',
            ' ', '\n', '.', ',', 'Y', 'W', 'G', 'P', 'B', 'V', 'K', 'X', 'Q'
        ]
        super().__init__(notes, keys)


class Keymap2(Keymap):
    def __init__(self):
        notes = [
            'E2', 'F2', 'F#2', 'G2', 'G#2',
            'A2', 'A#2', 'B2', 'C3', 'C#3',
            'D3', 'D#3', 'E3', 'F3', 'F#3',
            'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4'
        ]
        keys = [
            ###--|1|--|2|--|3|--|4|
            'A', 'B', 'P', ' ', '\n', 'G', 'W', 'V', 'I', 'X', 'Q', '.', ','
                                                                         'O', 'U', 'C', 'M', 'F',
            'N', 'S', 'R', 'K', 'D',
            'E', 'T', 'Y', 'L', 'H',
            #                                   Usable to here
        ]
        keys = [
            ###--|1|--|2|--|3|--|4|
            'E', 'T', 'Y', 'L', 'H',
            'N', 'S', 'R', 'K', 'D',
            'O', 'U', 'E', 'M', 'F',
            'A', 'B', 'P', ' ', '\n', 'G', 'W', 'V', 'I', 'X', 'Q', '.', ','
            #                                   Usable to here
        ]
        # keyboards for sale

        keys = [x.lower() for x in keys]
        super().__init__(notes, keys)
    pass


class MinecraftMap(Keymap):
    def __init__(self):
        notes = [
            'E2', 'F2', 'F#2', 'G2', 'G#2',
            'A2', 'A#2', 'B2', 'C3', 'C#3',
            'D3', 'D#3', 'E3', 'F3', 'F#3',
            'G3', 'G#3', 'A3', 'A#3', 'B3', 'Cd', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4'
        ]
        keys = [
            ' ', 'left', 'down', 'up', 'right',
            'e', '', '', '', '',
            'esc', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', ''
        ]
        # When playing Minecraft, we want to hold down the movement keys instead of quickly pressing them.
        held_keys = [' ', 'left', 'down', 'up', 'right']
        super().__init__(notes, keys, held_keys=held_keys)
