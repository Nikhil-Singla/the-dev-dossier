import tkinter as tk
from tkinter import messagebox, Toplevel

# ------------------------
# Basic piano behavior
# ------------------------
def play_note(note):
    print(f"Playing note: {note}")

def close_piano(event=None):
    root.destroy()

# ------------------------
# Globals for rebinding
# ------------------------
active_rebind_entry = None   # The Entry widget currently being edited
active_function = None       # The function (e.g., "Play Note 1") being rebound
swap_mode = True             # Swap ON by default
preference_entries = {}      # function_name -> Entry widget

# Function labels (fixed order for Preferences UI)
FUNCTIONS = [
    'Play Note 1',
    'Play Note 2',
    'Play Note 3',
    'Play Note 4',
    'Play Note 5',
    'Play Note 6',
    'Play Note 7',
    'Quit Piano'
]

# Map function -> musical note (only for Play Note 1..7)
function_to_note = {
    'Play Note 1': 'C4',
    'Play Note 2': 'D4',
    'Play Note 3': 'E4',
    'Play Note 4': 'F4',
    'Play Note 5': 'G4',
    'Play Note 6': 'A4',
    'Play Note 7': 'B4'
}

# Initial bindings: function -> key
func_to_key = {
    'Play Note 1': 'a',
    'Play Note 2': 's',
    'Play Note 3': 'd',
    'Play Note 4': 'f',
    'Play Note 5': 'g',
    'Play Note 6': 'h',
    'Play Note 7': 'j',
    'Quit Piano':  'Escape'
}

# Derived at runtime: key -> note (used to play sound/flash)
key_mapping = {}

def rebuild_runtime_bindings():
    """Recompute key -> note mapping from func_to_key."""
    global key_mapping
    key_mapping = {}
    for func, key in func_to_key.items():
        if func in function_to_note:
            # last-one-wins if duplicates exist
            key_mapping[key] = function_to_note[func]

def normalized_key_from_event(event):
    """Return normalized key string from a Tk event."""
    if event.char and event.char.strip():
        return event.char.lower()
    return event.keysym  # e.g., 'Escape', 'space', 'Return'

def set_entry_text_readonly(entry, text):
    """Safely set text in a readonly Entry."""
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, text)
    entry.config(state="readonly")

def start_rebinding(event, function_name):
    """Begin rebinding for a given function (row)."""
    global active_rebind_entry, active_function
    entry = preference_entries[function_name]
    active_rebind_entry = entry
    active_function = function_name
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, "Press a key...")
    entry.focus()

def detect_key(event):
    """Handle a key press inside the Preferences window for rebinding."""
    global active_rebind_entry, active_function, func_to_key

    if not active_rebind_entry or not active_function:
        return

    # Cancel rebinding with Escape
    if event.keysym == "Escape":
        set_entry_text_readonly(active_rebind_entry, func_to_key[active_function])
        active_rebind_entry = None
        active_function = None
        print("Rebinding cancelled.")
        return

    new_key = normalized_key_from_event(event)
    if not new_key:
        return

    old_key = func_to_key[active_function]

    # No change
    if new_key == old_key:
        set_entry_text_readonly(active_rebind_entry, old_key)
        active_rebind_entry = None
        active_function = None
        return

    # Find if another function already uses new_key (first match)
    other_function = None
    for f, k in func_to_key.items():
        if f != active_function and k == new_key:
            other_function = f
            break

    if other_function and swap_mode:
        # --- SWAP KEYS ---
        func_to_key[active_function], func_to_key[other_function] = new_key, old_key

        # Update both UI entries
        set_entry_text_readonly(preference_entries[active_function], new_key)
        set_entry_text_readonly(preference_entries[other_function], old_key)

        print(f"Swapped: '{active_function}' <-> '{other_function}'")
    else:
        # --- ASSIGN NEW KEY (duplicates allowed if swap OFF) ---
        func_to_key[active_function] = new_key
        set_entry_text_readonly(preference_entries[active_function], new_key)
        if other_function and not swap_mode:
            print(f"Duplicate key allowed: '{new_key}' now used by '{active_function}' and '{other_function}'")
        else:
            print(f"Rebound '{active_function}' from '{old_key}' to '{new_key}'")

    # Finish and rebuild runtime maps
    active_rebind_entry = None
    active_function = None
    rebuild_runtime_bindings()

def toggle_swap():
    global swap_mode
    swap_mode = not swap_mode
    if swap_button:
        swap_button.config(text=f"Swap Mode: {'ON' if swap_mode else 'OFF'}")

def show_preferences():
    global preference_entries, swap_button
    preference_entries = {}

    pref_window = Toplevel(root)
    pref_window.title("Preferences - Key Bindings")

    # Detect key presses in the Preferences window for rebinding
    pref_window.bind("<KeyPress>", detect_key)

    tk.Label(pref_window, text="Keyboard Shortcuts", font=("Arial", 14, "bold")).pack(pady=10)

    frame = tk.Frame(pref_window)
    frame.pack(pady=10)

    # Headers
    tk.Label(frame, text="Key", font=("Arial", 12, "bold"), width=15).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(frame, text="Function", font=("Arial", 12, "bold"), width=20).grid(row=0, column=1, padx=10, pady=5)

    # Rows in fixed function order
    for i, func in enumerate(FUNCTIONS, start=1):
        key = func_to_key[func]
        entry = tk.Entry(frame, width=15, justify="center")
        entry.insert(0, key)
        entry.config(state="readonly")
        entry.grid(row=i, column=0, padx=10, pady=5)

        # save and bind
        preference_entries[func] = entry
        entry.bind("<Button-1>", lambda e, f=func: start_rebinding(e, f))

        tk.Label(frame, text=func, width=20).grid(row=i, column=1, padx=10, pady=5)

    # Swap toggle
    swap_button = tk.Button(pref_window, text=f"Swap Mode: {'ON' if swap_mode else 'OFF'}", command=toggle_swap)
    swap_button.pack(pady=10)

    # Fit to content
    pref_window.update_idletasks()
    width = frame.winfo_reqwidth() + 40
    height = frame.winfo_reqheight() + 120
    pref_window.geometry(f"{width}x{height}")

# ------------------------
# Main window + menu
# ------------------------
root = tk.Tk()
root.title("Piano")
root.geometry("900x300")
root.configure(bg="gray")

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Preferences", command=show_preferences)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=close_piano)
menu_bar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Simple Piano App\nCreated with Tkinter"))
menu_bar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menu_bar)

# ------------------------
# Piano keys UI
# ------------------------
octaves = [4, 5]
white_notes_base = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
black_notes_base = ['C#', 'D#', '', 'F#', 'G#', 'A#', '']

white_keys = [note + str(o) for o in octaves for note in white_notes_base]
black_keys = [n + str(o) if n != '' else '' for o in octaves for n in black_notes_base]

white_frame = tk.Frame(root, bg="gray")
white_frame.pack(side="bottom", fill="x")

white_buttons = {}
for note in white_keys:
    btn = tk.Button(white_frame, text=note, width=6, height=10, bg="white",
                    command=lambda n=note: play_note(n))
    btn.pack(side="left", padx=1)
    white_buttons[note] = btn

black_positions = [0.05, 0.15, 0, 0.35, 0.45, 0.55, 0] * len(octaves)
for i, note in enumerate(black_keys):
    if note != '':
        btn = tk.Button(root, text=note, width=4, height=6, bg="black", fg="white",
                        command=lambda n=note: play_note(n))
        btn.place(relx=black_positions[i] + (i // 7) * 0.5, rely=0.05)

# ------------------------
# Keyboard handling
# ------------------------
def key_press_main(event):
    key = normalized_key_from_event(event)

    # Quit key (dynamic)
    if key == func_to_key['Quit Piano']:
        close_piano()
        return

    # Note keys
    if key in key_mapping:
        note = key_mapping[key]
        play_note(note)
        if note in white_buttons:
            btn = white_buttons[note]
            btn.config(bg="lightblue")
            root.after(200, lambda: btn.config(bg="white"))

root.bind("<KeyPress>", key_press_main)

# Build initial mapping
rebuild_runtime_bindings()

root.mainloop()
