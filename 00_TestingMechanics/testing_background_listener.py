from pynput.keyboard import Key, Listener
import win32clipboard

def setClipboard(text):
    win32clipboard.OpenClipboard()

    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(str(text))

    win32clipboard.CloseClipboard()

def getFromClipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()


def on_press(key):
    print('{0} pressed'.format(key))


def on_release(key):
    print('{0} release'.format(key))
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
