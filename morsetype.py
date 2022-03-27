# Adam Rilatt
# 25 March 2022
# Morse Typer

from threading import Thread
import keyboard
import time
import sys

SWAP_CODE = 'ctrl+`'
MORSE_KEY = 'space'
WPM = 15
DITS_BETWEEN_LETTERS = 2
DITS_BETWEEN_WORDS = 10

MORSE_GLYPHS = {
    '.-'    : 'a',
    '-...'  : 'b',
    '-.-.'  : 'c',
    '-..'   : 'd',
    '.'     : 'e',
    '..-.'  : 'f',
    '--.'   : 'g',
    '....'  : 'h',
    '..'    : 'i',
    '.---'  : 'j',
    '-.-'   : 'k',
    '.-..'  : 'l',
    '--'    : 'm',
    '-.'    : 'n',
    '---'   : 'o',
    '.--.'  : 'p',
    '--.-'  : 'q',
    '.-.'   : 'r',
    '...'   : 's',
    '-'     : 't',
    '..-'   : 'u',
    '...-'  : 'v',
    '.--'   : 'w',
    '-..-'  : 'x',
    '-.--'  : 'y',
    '--..'  : 'z'
}

# ============================================================================ #
# http://www.kent-engineers.com/codespeed.htm
dit_length_s = 1.2 / WPM

exit_program = False
morse_mode   = False
key_down     = False

morse_start = 0
morse_end   = 0
character_queue = []

def morse_timeouts():

    global exit_program
    global morse_start
    global morse_end
    global key_down

    interpreted_character = False

    while not key_down:

        time_since_last_tx = time.time() - morse_end

        # Gap of 3 is a space
        if interpreted_character and time_since_last_tx >= DITS_BETWEEN_WORDS * dit_length_s:
            keyboard.send('space')
            break

        # Gap of 1 is a character separator
        elif not interpreted_character and time_since_last_tx >= DITS_BETWEEN_LETTERS * dit_length_s:

            # Remove the Morse
            for character in character_queue:
                keyboard.send('backspace')

            morse_string = ''.join(character_queue)
            if morse_string in MORSE_GLYPHS.keys():
                keyboard.send(MORSE_GLYPHS[morse_string])

            character_queue.clear()
            interpreted_character = True



def on_press(key):

    global exit_program

    if key.name == 'esc':
        exit_program = True
        return

def morse_down(key):

    global morse_mode
    global morse_start
    global key_down

    if morse_mode and not key_down:
        morse_start = key.time
        key_down = True

    elif not morse_mode:
        keyboard.press('space')


def morse_up(key):

    global morse_mode
    global morse_start
    global morse_end
    global key_down

    if morse_mode:

        morse_end = key.time
        key_down = False

        duration = morse_end - morse_start

        if duration > dit_length_s:
            keyboard.send('-')
            character_queue.append('-')
        else:
            keyboard.send('.')
            character_queue.append('.')

        # Check whether the character / word has ended
        t = Thread(target = morse_timeouts, args = ())
        t.start()

    else:
        keyboard.release('space')

# Exit the program by pressing Escape and then toggling Morse Mode.
keyboard.on_press(on_press)

# Morse bindings
keyboard.on_press_key  (MORSE_KEY, morse_down, suppress = True)
keyboard.on_release_key(MORSE_KEY, morse_up,   suppress = True)

while not exit_program:

    keyboard.wait(SWAP_CODE)
    morse_mode = not morse_mode
