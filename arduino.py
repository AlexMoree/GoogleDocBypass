import tkinter as tk
from tkinter import scrolledtext, messagebox
import serial
import time
import random
import threading

# --- Settings ---
arduino_port = "COM5"  # Change this to your Arduino port
baud_rate = 9600
wpm = 150
chars_per_sec = 150 * 5 / 60  # approx 9 chars/sec
base_delay = 1 / chars_per_sec
error_rate = 0.05  # 15% typo
letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,./;\'[]\\`~!@#$%^&*()_+-={}:"<>?| \n'

# Expanded QWERTY adjacency map
adjacent_keys = {
    # letters
    'a': ['q','w','s','z'],
    'b': ['v','g','h','n'],
    'c': ['x','d','f','v'],
    'd': ['s','e','r','f','c','x'],
    'e': ['w','s','d','r'],
    'f': ['d','r','t','g','v','c'],
    'g': ['f','t','y','h','b','v'],
    'h': ['g','y','u','j','n','b'],
    'i': ['u','j','k','o'],
    'j': ['h','u','i','k','n','m'],
    'k': ['j','i','o','l','m'],
    'l': ['k','o','p',';'],
    'm': ['n','j','k',','],
    'n': ['b','h','j','m'],
    'o': ['i','k','l','p'],
    'p': ['o','l',';','['],
    'q': ['w','a'],
    'r': ['e','d','f','t'],
    's': ['a','w','e','d','x','z'],
    't': ['r','f','g','y'],
    'u': ['y','h','j','i'],
    'v': ['c','f','g','b'],
    'w': ['q','a','s','e'],
    'x': ['z','s','d','c'],
    'y': ['t','g','h','u'],
    'z': ['a','s','x'],

    # numbers
    '1': ['2','q'],
    '2': ['1','3','q','w'],
    '3': ['2','4','w','e'],
    '4': ['3','5','e','r'],
    '5': ['4','6','r','t'],
    '6': ['5','7','t','y'],
    '7': ['6','8','y','u'],
    '8': ['7','9','u','i'],
    '9': ['8','0','i','o'],
    '0': ['9','o','p'],

    # punctuation
    ',': ['m','.','k'],
    '.': [',','/','l'],
    '/': ['.',';'],
    ';': ['l','p','\''],
    '\'': [';','['],
    '[': ['p',']','\''],
    ']': ['[','\\'],
    '\\': [']'],
    '-': ['0','=','_'],
    '=': ['-','+'],
    '_': ['-','='],
    '+': ['=','-'],
    '`': ['1','~'],
    '~': ['`','1'],
    '!': ['@','1'],
    '@': ['!','#','2'],
    '#': ['@','$','3'],
    '$': ['#','%','4'],
    '%': ['$','^','5'],
    '^': ['%','&','6'],
    '&': ['^','*','7'],
    '*': ['&','(','8'],
    '(': ['*',')','9'],
    ')': ['(','0'],
    '?': ['/',','],
    ':': [';','"'],
    '"': [':',';'],

    # space and newline
    ' ': [' ', '.'],
    '\n': ['\n']
}
# --- Functions ---
def human_typing(ser, text):
    """
    Send text to Arduino one character at a time,
    simulating human typing with random typos and corrections.
    """
    for char in text:
        lower_char = char.lower()

        # --- Introduce a typo occasionally ---
        if (
            random.random() < error_rate
            and lower_char in adjacent_keys
            and char not in ['\n', '\r']
        ):
            typo = random.choice(adjacent_keys[lower_char])
            if char.isupper():
                typo = typo.upper()

            # Type the wrong key
            ser.write(typo.encode('utf-8'))
            ser.flush()
            time.sleep(base_delay * random.uniform(0.8, 1.2))

            # Backspace to "fix" it
            ser.write(b'\b')
            ser.flush()
            time.sleep(base_delay * random.uniform(0.8, 1.2))

        # --- Type the intended character ---
        ser.write(char.encode('utf-8'))
        ser.flush()
        time.sleep(base_delay * random.uniform(0.8, 1.2))

def send_to_arduino(text):
    try:
        ser = serial.Serial(arduino_port, baud_rate)
        time.sleep(2)  # wait for Arduino to reset

        for char in text:
            lower_char = char.lower()

            # --- Optional human typing error simulation ---
            if (
                random.random() < error_rate
                and lower_char in adjacent_keys
                and char not in ['\n', '\r']
            ):
                # pick a nearby key as a typo
                typo = random.choice(adjacent_keys[lower_char])
                if char.isupper():
                    typo = typo.upper()

                # type the wrong key first
                ser.write(typo.encode('utf-8'))
                ser.flush()
                time.sleep(base_delay * random.uniform(0.8, 1.2))

                # backspace to "fix" it
                ser.write(b'\b')
                ser.flush()
                time.sleep(base_delay * random.uniform(0.8, 1.2))

            # --- send the intended character ---
            ser.write(char.encode('utf-8'))
            print(char, end='', flush=True)
            ser.flush()

            # small delay between characters (human-like pacing)
            time.sleep(base_delay * random.uniform(0.8, 1.2))

        ser.close()
        messagebox.showinfo("Done", "Essay typed successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to send to Arduino:\n{e}")


def on_send_click():
    essay_text = text_box.get("1.0", tk.END).strip()
    if not essay_text:
        messagebox.showwarning("Empty", "Please enter an essay first!")
        return

    # Run typing in a separate thread to avoid freezing the GUI
    threading.Thread(target=send_to_arduino, args=(essay_text,), daemon=True).start()
# --- GUI ---
root = tk.Tk()
root.title("Arduino Human Typing Simulator")

# Text box
text_box = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
text_box.pack(padx=10, pady=10)

# Send button
send_button = tk.Button(root, text="Type my Essay", command=on_send_click)
send_button.pack(pady=10)

root.mainloop()