from typing import List, Optional, Union

from config import (
    ESC_NOTE,
    JUMP_NOTE,
    CRAFT_NOTE,
    ATTACK_NOTE,
    STRAFE_UP_NOTE,
    STRAFE_LEFT_NOTE,
    STRAFE_DOWN_NOTE,
    STRAFE_RIGHT_NOTE,
    COMBO_KEYS_TO_NOTES,

    PICK_BLOCK_NOTE,
    PLACE_BLOCK_NOTE,

    MOUSE_UP_NOTE,
    MOUSE_LEFT_NOTE,
    MOUSE_DOWN_NOTE,
    MOUSE_RIGHT_NOTE,
    MOUSE_CLICK_NOTE,

    ONE_NOTE,
    TWO_NOTE,
    THREE_NOTE,
    FOUR_NOTE,
    FIVE_NOTE,
    SIX_NOTE,
    SEVEN_NOTE,
    EIGHT_NOTE,
    NINE_NOTE,
    ZERO_NOTE
)

from mouse import MOUSE_UP_KEY, MOUSE_DOWN_KEY, MOUSE_LEFT_KEY, MOUSE_RIGHT_KEY, MOUSE_CLICK_KEY


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

    def should_hold_key(self, key_or_key_list: Union[str, List]) -> bool:
        """When this key is registered, should it be quickly pressed and released, or held until explicitly released?
        """
        if isinstance(key_or_key_list, List):
            return any(x in self.held_keys for x in key_or_key_list)
        return key_or_key_list in self.held_keys


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
        # When playing Minecraft, we want to hold down the movement keys instead of quickly pressing them.
        held_keys = [' ', 'left', 'down', 'up', 'right', MinecraftMap.key_for_note(ATTACK_NOTE)]
        super().__init__([], [], held_keys=held_keys)

    @classmethod
    def key_for_note(cls, note: str) -> Optional[str]:
        config_keys = {
            ESC_NOTE: 'esc',
            JUMP_NOTE: ' ',
            CRAFT_NOTE: 'e',
            ATTACK_NOTE: 'p',

            PICK_BLOCK_NOTE: 'z',
            PLACE_BLOCK_NOTE: 'i',

            STRAFE_LEFT_NOTE: 'left',
            STRAFE_RIGHT_NOTE: 'right',
            STRAFE_UP_NOTE: 'up',
            STRAFE_DOWN_NOTE: 'down',

            # MOUSE_LEFT_NOTE: MOUSE_LEFT_KEY,
            # MOUSE_RIGHT_NOTE: MOUSE_RIGHT_KEY,
            # MOUSE_UP_NOTE: MOUSE_UP_KEY,
            # MOUSE_DOWN_NOTE: MOUSE_DOWN_KEY,
            # MOUSE_CLICK_NOTE: MOUSE_CLICK_KEY,

            ONE_NOTE: 'a',
            TWO_NOTE: '2',
            THREE_NOTE: '3',
            FOUR_NOTE: '4',
            FIVE_NOTE: '5',
            SIX_NOTE: '6',
            SEVEN_NOTE: '7',
            EIGHT_NOTE: '8',
            NINE_NOTE: '9',
            ZERO_NOTE: '0'
        }
        if note in config_keys:
            return config_keys[note]
        return None


class MarioMap(Keymap):
    def __init__(self):
        # When playing Mario, we want to hold down the movement keys instead of quickly pressing them.
        held_keys = [' ', 'left', 'down', 'up', 'right', MinecraftMap.key_for_note(ATTACK_NOTE)]
        super().__init__([], [], held_keys=held_keys)

    @classmethod
    def key_for_note(cls, note: str) -> Optional[Union[str, List]]:
        config_keys = {
            ESC_NOTE: 'esc',

            STRAFE_LEFT_NOTE: 'left',
            STRAFE_RIGHT_NOTE: 'right',
            STRAFE_UP_NOTE: 'up',
            STRAFE_DOWN_NOTE: 'down',

            ONE_NOTE: 'a',
            TWO_NOTE: '2',
            THREE_NOTE: '3',
            FOUR_NOTE: '4',
            FIVE_NOTE: '5',
            SIX_NOTE: '6',
            SEVEN_NOTE: '7',
            EIGHT_NOTE: '8',
            NINE_NOTE: '9',
            ZERO_NOTE: '0'
        }
        if note in config_keys:
            return config_keys[note]
        if note in COMBO_KEYS_TO_NOTES:
            return COMBO_KEYS_TO_NOTES[note]
        return None
