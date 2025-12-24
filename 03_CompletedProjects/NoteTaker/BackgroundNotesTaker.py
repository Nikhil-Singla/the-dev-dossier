import tkinter as tk
from tkinter import filedialog, Button, RIGHT

# Currently selected output file
selected_file = None

# Select File Dialog Box
def select_file():
    """Function to be called when the button is pressed."""

    global selected_file

    # Open file picker dialog
    selected_file = filedialog.askopenfilename(title="Select a file")
    
    # Update window title if a file was actually selected
    if selected_file:
        root.title("/".join(selected_file.split("/")[-2:]))

    # File dialogs steal focus on Windows; restore it manually
    # Use after() to wait until Tk finishes processing the dialog
    root.after(0, text_widget.focus_set)

# Stop execution if file is missing
def test_selected_file(input_file):
    # Just a simple guard so we don't write to nothing
    return bool(input_file)

# What happens when you press Ctrl+Enter
def on_ctrl_enter(event):
    
    """Handle Ctrl+Enter key press - output to file and clear text"""
    
    # Grab text from widget box
    content = text_widget.get("1.0", "end-1c")
    
    # Only output if there's actual content
    if content.strip():

        # Bail out quietly if no file is selected
        if not test_selected_file(selected_file):
            return "break"

        # Append content to the selected file
        with open(selected_file, "a") as f:
            f.write(content)
            f.write("\n\n")

        # Clear out the text in widget
        text_widget.delete("1.0", tk.END)

    # Prevent default newline behavior
    return "break"

# Create main window
root = tk.Tk()
root.title("Notes")
root.geometry("300x200")
root.attributes('-topmost', True)  # Keep window on top

# Change Frame Color
frame = tk.Frame(root, background="black")
frame.pack(fill=tk.BOTH, expand=True)

# Button to select / change output file
button = Button(frame, text='Select File', command=select_file)
button.pack(side=RIGHT, padx=10)

# Create text widget
text_widget = tk.Text(frame, wrap=tk.WORD, font=("Arial", 12), bg='#232628', fg="white", insertbackground='white')
text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Bind Ctrl+Enter to write-to-file action
text_widget.bind("<Control-Return>", on_ctrl_enter)

# Focus text widget on startup
text_widget.focus_set()

# Start GUI loop
root.mainloop()
