import tkinter as tk
from tkinter import filedialog

# Select File Dialog Box
selected_file = filedialog.askopenfilename(title="Select a file")

# Testing/Debugging
# if selected_file:
#     print(selected_file)
# else:
#     exit()

# Stop execution if file is missing
if not selected_file:
    exit()

# What happens when you press Ctrl+Enter
def on_ctrl_enter(event):
    
    """Handle Ctrl+Enter key press - output to file and clear text"""
    
    # Grab text from widget box
    content = text_widget.get("1.0", "end-1c")
    
    # Only output if there's actual content  
    if content.strip():  

        # Write to the selected file in append, and add a newline at the end.
        with open(selected_file, "a") as f:
            f.write(content)
            f.write('\n\n')

        # Debugging grabbed text
        # print(text)
        
        # Clear out the text in widget
        text_widget.delete("1.0", tk.END)
    
    # Prevent default behavior
    return "break"  

# Create main window
root = tk.Tk()
root.title("Notes")
root.geometry("300x200")
root.attributes('-topmost', True)  # Keep window on top

# Change Frame Color
frame = tk.Frame(root, background="black")
frame.pack(fill=tk.BOTH, expand=True)

# Create text widget
text_widget = tk.Text(frame, wrap=tk.WORD, font=("Arial", 12), bg = '#232628', fg="white")
text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Bind keys
text_widget.bind("<Control-Return>", on_ctrl_enter)

# Focus on text widget
text_widget.focus()

# Start GUI loop
root.mainloop()
