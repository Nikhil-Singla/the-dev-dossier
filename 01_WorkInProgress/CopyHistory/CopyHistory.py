from pynput.keyboard import Key, Listener
import win32clipboard

COPY = '\x03'
CUT = '\x18'
PASTE = '\x16'

def setClipboard(text):
    '''Opens the clipboard, empties it, and sets the text to the parameter "text".
    
    :param text: Input text that will be replaced to clipboard
    :return: None. The clipboard should be replaced.
    '''
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()

    win32clipboard.SetClipboardText(str(text))

    win32clipboard.CloseClipboard()

def getFromClipboard():
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
    except Exception as e:
        print(f"Error accessing clipboard: {e}")

    finally:
        win32clipboard.CloseClipboard()
    
    return data

def on_press(key):
    print('{0} pressed'.format(key))

def on_release(key):
    print('{0} release'.format(key))

    if key == COPY:
        print(getFromClipboard())

listener = Listener(on_press=on_press, on_release=on_release)

listener.start()
input()
listener.stop()

# print(getFromClipboard())
# setClipboard("Whatever")
# print(getFromClipboard())
