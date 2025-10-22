import os
import json
import time
import pyautogui
from pynput import mouse

# Assign folder names to store screenshots and mapping data for screenshots to numbers
SAVE_FOLDER = "click_screenshots"
IMAGE_TO_NAME_DICTIONARY_FILE = os.path.join(SAVE_FOLDER, "click_data.json")

# Check for folder location
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Load JSON data or initialize a new container
if os.path.exists(IMAGE_TO_NAME_DICTIONARY_FILE):
    with open(IMAGE_TO_NAME_DICTIONARY_FILE, "r") as oldDictionaryFile:
        currentDictionary = json.load(oldDictionaryFile)
else:
    currentDictionary = {}

# Dynamically get the current highest index to map to, so as to continue assigning higher images.
# ONLY WORKS IF DATA IS NUMERICALLY SEQUENTIAL AND COMPLETE MAPPING IN FILE
def get_next_index():
    if not currentDictionary:
        return 0

    return len(currentDictionary)

startingIndex = get_next_index()

def on_click(x, y, button, pressed):
    global startingIndex, currentDictionary
    
    if pressed:

        # Assign location + folder name to save the screenshot to
        screenshot_path = os.path.join(SAVE_FOLDER, f"{startingIndex}.png")
        
        # Take a screenshot and then save it to this location, name
        pyautogui.screenshot(screenshot_path)
        
        # We need to update dictionary of coordinates to the index of the image file
        currentDictionary[str(startingIndex)] = {"x": x, "y": y}
        
        # Write it to the json file in case of program end.
        with open(IMAGE_TO_NAME_DICTIONARY_FILE, "w") as f:
            json.dump(currentDictionary, f, indent=4)
        
        # Debugging print to console for testing purposes.
        print(f"[+] Saved screenshot #{startingIndex} at ({x}, {y})")
        
        startingIndex += 1

try:
    # Start listening for mouse clicks
    print("Listening for mouse clicks... (Press Ctrl+C to stop)")
    
    listener = mouse.Listener(on_click=on_click)
    listener.start()  # Non-blocking

    while listener.is_alive():
        time.sleep(0.1)  # Keeps the main thread alive

except KeyboardInterrupt:
    print("\nKeyboard interrupt received. Stopping listener.")
    listener.stop()
    listener.join()
