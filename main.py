import tkinter as tk
from tkinter import ttk
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Listener as KeyboardListener, KeyCode
import threading
import time
import random

mouse_controller = MouseController()

click_key = KeyCode(char='f')
clicking = False
enabled = False
base_cps = 15
jitter_enabled = True

def human_click_loop():
    global clicking
    while True:
        if enabled and clicking:
            # Calculate random delay to mimic human behavior
            interval = 1 / base_cps
            jitter = random.uniform(-0.004, 0.004)  # Small delay randomness
            total_delay = max(0.01, interval + jitter)

            # Randomly move mouse slightly
            if jitter_enabled and random.random() < 0.2:
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
                mouse_controller.move(dx, dy)

            mouse_controller.click(Button.left)
            time.sleep(total_delay)
        else:
            time.sleep(0.01)

def on_press(key):
    global clicking
    if enabled and key == click_key:
        clicking = not clicking
        status = "started" if clicking else "stopped"
        print(f"[+] Auto-clicking {status}.")

def toggle_enabled():
    global enabled
    enabled = not enabled
    status = "ENABLED" if enabled else "DISABLED"
    toggle_button.config(text=f"CPS Booster: {status}")
    print(f"[!] CPS booster {status}")

def update_cps(val):
    global base_cps
    try:
        base_cps = float(val)
    except ValueError:
        base_cps = 15

def update_key():
    global click_key
    key_str = key_entry.get().lower()
    if len(key_str) == 1:
        click_key = KeyCode(char=key_str)
        key_label.config(text=f"Key set to: {key_str.upper()}")
    else:
        key_label.config(text="Invalid key! Use 1 character.")

def toggle_jitter():
    global jitter_enabled
    jitter_enabled = not jitter_enabled
    jitter_button.config(text=f"Jitter: {'ON' if jitter_enabled else 'OFF'}")

# GUI
root = tk.Tk()
root.title("Safe Auto Clicker")
root.geometry("300x240")
root.resizable(False, False)

toggle_button = ttk.Button(root, text="CPS Booster: DISABLED", command=toggle_enabled)
toggle_button.pack(pady=10)

ttk.Label(root, text="Clicks Per Second (CPS):").pack()
cps_slider = ttk.Scale(root, from_=1, to=25, orient='horizontal', command=update_cps)
cps_slider.set(15)
cps_slider.pack()

ttk.Label(root, text="Click key (e.g. F, G, etc.):").pack(pady=(10, 0))
key_entry = ttk.Entry(root)
key_entry.pack()

key_label = ttk.Label(root, text="Current key: F")
key_label.pack()
ttk.Button(root, text="Set Key", command=update_key).pack(pady=5)

jitter_button = ttk.Button(root, text="Jitter: ON", command=toggle_jitter)
jitter_button.pack(pady=5)

# Start background threads
click_thread = threading.Thread(target=human_click_loop, daemon=True)
click_thread.start()

keyboard_listener = KeyboardListener(on_press=on_press)
keyboard_listener.start()

root.mainloop()
