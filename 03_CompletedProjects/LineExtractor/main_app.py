import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox, FirefoxOptions
from selenium import webdriver
import pyautogui
import numpy as np
import cv2
import os


from flask import Flask, redirect, render_template, request, url_for, send_from_directory

app = Flask(__name__)


threshold_area = 90
canny_threshold1 = 10
canny_threshold2 = 10
thickness_reduction_factor = 1
output_file = "output.png"

# Uses Canny Edge detection to get in an image path on your PC, and specific variables
# And then writes to on output file with the image that has detected all the edges in a picture


def getWalls(image_path, threshold_area, canny_threshold1, canny_threshold2, output_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to segment the walls
    _, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Apply Canny edge detection to detect lines
    edges = cv2.Canny(thresholded, canny_threshold1, canny_threshold2)

    # Remove small components or noise from the detected lines
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        edges, connectivity=8)

    # Create a mask to filter out small components
    mask = np.zeros_like(labels, dtype=np.uint8)
    for label in range(1, num_labels):
        area = stats[label, cv2.CC_STAT_AREA]
        if area > threshold_area:
            mask[labels == label] = 255

    # Apply the mask to retain only the lines along the walls
    result = cv2.bitwise_and(edges, edges, mask=mask)

    # Perform morphological dilation to connect adjacent line segments
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    dilated = cv2.dilate(result, kernel, iterations=1)

    # Display the resulting image [UNDO TO SEE MID RESULT]
    # cv2.imshow('Original Image', image)
    # cv2.imshow('Lines along Walls', dilated)
    cv2.imwrite(output_path, dilated)
    cv2.destroyAllWindows()
# NO RETURN FUNCTION. ONLY OUTPUT IMAGE CHANGES

# Takes an output file (automatic here) and converts it to greyscale (black and white)
# Then uses erosion to update the output file and removes and overlapping detected edges and borders
# Output file is updated with an image with minimized borders/lines


def reduction(pathToOutput, output_path):
    img = cv2.imread(pathToOutput, cv2.IMREAD_GRAYSCALE)

    # Set the desired thickness reduction factor
    thickness_reduction_factor = 9

    # Define the structuring element for erosion
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Perform erosion
    eroded_image = cv2.erode(
        img, kernel, iterations=thickness_reduction_factor)

    # Display the eroded image [UNDO TO SEE MID RESULT]
    # cv2.imshow("Eroded Image", eroded_image)
    cv2.destroyAllWindows()
    cv2.imwrite(output_path, eroded_image)
# NO RETURN FUNCTION. ONLY OUTPUT IMAGE CHANGES

# Takes the output image as an input after reduction
# Does another run of Canny Edge detection and Hough Line Transform to get the various dimensions of the lines
# Writes them in a variable as the coordinates an d lengths and stuff, and then returns this variable


def detect_line_segments(image_path):
    # Load the image in grayscale
    image = cv2.imread(image_path, 0)

    # Apply Canny edge detection
    edges = cv2.Canny(image, 50, 150, apertureSize=3)

    # Perform Hough Line Transform
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi /
                            180, threshold=100, minLineLength=20, maxLineGap=10)

    # Process the detected lines
    dimensions = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            dimensions.append((x1, y1, x2, y2, length, angle))

    return dimensions
# RETURNS A LIST OF DIMENSIONS


# Define a folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
    if 'file' not in request.files:
        print('No file part in the request')
        return redirect(request.url)

    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        print('No selected file')
        return redirect(request.url)

    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], "output.png")

        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Image file not found.")

        # Call the function to reduce the image to lines and label them
        getWalls(filepath, threshold_area, canny_threshold1,
                 canny_threshold2, output_path)

        # Call the function to remove background elements and retain lines along walls
        reduction(output_path, output_path)

        line_segments = detect_line_segments(output_path)
        list_of_xcor = []
        list_of_ycor = []

        # Separating out the x and the y coordinates from the stored dimensions for better usability.
        for segment in line_segments:
            x1, y1, x2, y2, length, angle = segment
            print(
                f"Start Point: ({x1}, {y1}), End Point: ({x2}, {y2}), Length: {length}, Angle: {angle}")
            list_of_xcor.append(x1)
            list_of_ycor.append(y1)
            list_of_xcor.append(x2)
            list_of_ycor.append(y2)

        # Converts from string to int for coordinates
        list_of_xcor = [int(x) for x in list_of_xcor]
        list_of_ycor = [int(y) for y in list_of_ycor]

        # Initialize options for the FIREFOX driver
        opts = FirefoxOptions()
        opts.add_argument("--width=1920")
        opts.add_argument("--height=1080")

        # This option needs to be enabled, and it will remove the GUI, only do it when clicking works without the GUI
        # opts.add_argument("-headless")

        # Initialize the FIREFOX driver. BASICALLY OPENS THE WEB BROWSER
        driver = Firefox(options=opts)
        driver.get('https://cvdlab.github.io/react-planner/')
        driver.switch_to.window(driver.current_window_handle)
        time.sleep(0.20)
        # Fixed set of clicks that click on + sign on the page, and then click on the wall.
        # Works as the dimensions of the webbrowser are fixed and hence the click coordinates don't change
        # Trying to get this to work with clicking on elements instead

        def selectWall():
            time.sleep(0.20)
            pyautogui.click(17, 168)
            time.sleep(0.20)
            pyautogui.click(676, 372)

        # Variable set of clicks that click on the page itself, and then click according to the input coordinates.
        # Trying to get this to work with clicking on elements instead, maybe the canvas itself on the specific coordinates.
        def drawWall(x1, y1, x2, y2):
            pyautogui.click(x1, y1)
            time.sleep(0.20)
            pyautogui.click(x2, y2)
            time.sleep(0.20)
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        # Defining a single variable called coords for both x,y for easier use in code.
        coords = list(map(list, zip(list_of_xcor, list_of_ycor)))

        # Goes over each second element of coord, and then selects the wall, and then calls the drawing wall function
        # Two consecutive elements are the x,y coordinates referencing the start and the end point of a line segment in the output
        # [0] is the start point and 1 is the end point of the very first line segment to be drawn.
        # [0][0] is the x coordinate of the start point and [0][1] is the y coordinate of the start point from above.
        for i in range(0, len(coords), 2):
            selectWall()
            time.sleep(0.20)
            drawWall(coords[i][0], coords[i][1],
                     coords[i+1][0], coords[i+1][1])

        # Fixed set of clicks that click on save button page, and then download the file.
        # Works as the dimensions of the webbrowser are fixed and hence the click coordinates don't change
        # Trying to get this to work with clicking on elements instead, and the save button
        def saveProject():
            time.sleep(0.20)
            pyautogui.click(19, 94)
            time.sleep(0.20)
            pyautogui.click(1053, 592)
            time.sleep(0.20)

        # Actually calling the project
        saveProject()

        # Wait for 5 seconds before exiting.
        time.sleep(5)
        driver.quit()

        print('File uploaded:', filename)

        return render_template('hello.html', filename=filename)

    else:

        print('Request for hello page received with no file -- redirecting')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)