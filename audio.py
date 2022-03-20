from playsound import playsound
from enum import Enum
from pathlib import Path

ROOT = Path('data/audio')

class Sound(Enum):
    '''
    Enum of all sounds
    '''
    CONFIRM = ROOT.joinpath('confirm.wav')
    ERROR = ROOT.joinpath('error.wav')


def play_sound(sound: Sound):
    playsound(sound.value)

if __name__ == '__main__':
    play_sound(Sound.CONFIRM)
    play_sound(Sound.ERROR)
