# NoteTaker – Background Notes Taker (MVP)

A tiny always-on-top text box to jot quick notes into a selected file while you work in other apps.

## Features
- Always on top: window stays above other apps for quick access.
- Quick append: press Ctrl+Enter to append content to your chosen file.
- Simple input: Enter inserts a newline (default behavior).
- Dark UI: dark frame and text area for low-glare note taking.
- Safe exit on cancel: if no file is selected at launch, the app exits.

## Requirements
- Python 3.8+ (tkinter is included with standard Python on Windows/macOS).

## Setup & Run
```bash
cd 03_CompletedProjects/NoteTaker
python BackgroundNotesTaker.py
```

On launch, you’ll be prompted to select a file. Notes will be appended to that file.

## Usage
- Type your note in the text box.
- Press Ctrl+Enter to append the note to the selected file and clear the box.
- The window remains on top so you can keep it beside other apps.

## Output Format
- Notes are appended with a blank line after each entry for readability.

## Notes & Tips
- Use a plain text file (e.g., .txt) for best results.
- If you cancel the file dialog, the app closes immediately.
- Some full-screen exclusive apps may still cover all windows; borderless/windowed modes work best for always-on-top helpers.

## File Reference
- Main script: `BackgroundNotesTaker.py`
