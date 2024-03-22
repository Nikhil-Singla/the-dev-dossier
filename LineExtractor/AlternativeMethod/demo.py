import cv2
import os
import numpy as np
import pyautogui
import time 
from selenium import webdriver
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Image file name
image_file = "floor_plan.png"
output_file = "output.png"

# Image file path
image_path = os.path.join(current_dir, image_file)
output_path = os.path.join(current_dir, output_file)


# Check if the image file exists
if not os.path.isfile(image_path):
    raise FileNotFoundError(f"Image file '{image_file}' not found.")

# Uses Canny Edge detection to get in an image path on your PC, and specific variables
# And then writes to on output file with the image that has detected all the edges in a picture
def getWalls(image_path, threshold_area, canny_threshold1, canny_threshold2):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to segment the walls
    _, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Apply Canny edge detection to detect lines
    edges = cv2.Canny(thresholded, canny_threshold1, canny_threshold2)
    
    # Remove small components or noise from the detected lines
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(edges, connectivity=8)
    
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
    cv2.imshow('Original Image', image)
    cv2.imshow('Lines along Walls', dilated)
    cv2.imwrite(output_path, dilated)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
## NO RETURN FUNCTION. ONLY OUTPUT IMAGE CHANGES

# Takes an output file (automatic here) and converts it to greyscale (black and white)
# Then uses erosion to update the output file and removes and overlapping detected edges and borders
# Output file is updated with an image with minimized borders/lines
def reduction(pathToOutput):
    img = cv2.imread(pathToOutput, cv2.IMREAD_GRAYSCALE)

    # Set the desired thickness reduction factor
    thickness_reduction_factor = 9

    # Define the structuring element for erosion
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Perform erosion
    eroded_image = cv2.erode(img, kernel, iterations=thickness_reduction_factor)

    # Display the eroded image [UNDO TO SEE MID RESULT]
    cv2.imshow("Eroded Image", eroded_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(output_path, eroded_image)
## NO RETURN FUNCTION. ONLY OUTPUT IMAGE CHANGES

# Takes the output image as an input after reduction
# Does another run of Canny Edge detection and Hough Line Transform to get the various dimensions of the lines
# Writes them in a variable as the coordinates an d lengths and stuff, and then returns this variable
def detect_line_segments(image_path):
    # Load the image in grayscale
    image = cv2.imread(image_path, 0)

    # Apply Canny edge detection
    edges = cv2.Canny(image, 50, 150, apertureSize=3)

    # Perform Hough Line Transform
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=100, minLineLength=20, maxLineGap=10)

    # Process the detected lines
    dimensions = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            dimensions.append((x1, y1, x2, y2, length, angle))

    return dimensions
## RETURNS A LIST OF DIMENSIONS

# Setting variables for Canny Edge Detection
threshold_area = 90
canny_threshold1 = 10
canny_threshold2 = 10
thickness_reduction_factor = 1

# Call the function to reduce the image to lines and label them
getWalls(image_path, threshold_area, canny_threshold1, canny_threshold2)

# Call the function to remove background elements and retain lines along walls
reduction(output_path)

# Storing the returned dimensions from detect line segments into this variable
line_segments = detect_line_segments(output_path)

list_of_xcor = []
list_of_ycor = []

# Separating out the x and the y coordinates from the stored dimensions for better usability.
for segment in line_segments:
    x1, y1, x2, y2, length, angle = segment
    print(f"Start Point: ({x1}, {y1}), End Point: ({x2}, {y2}), Length: {length}, Angle: {angle}")
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

# Fixed set of clicks that click on + sign on the page, and then click on the wall.
# Works as the dimensions of the webbrowser are fixed and hence the click coordinates don't change
# Trying to get this to work with clicking on elements instead
def selectWall():
    time.sleep(0.20)
    cssSelector_OpenMenu = ".toolbar > div:nth-child(4) > div:nth-child(1) > svg:nth-child(1)"
    cssSelector = "#app > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > svg:nth-child(1) > g:nth-child(2) > g:nth-child(2) > g:nth-child(2) > g:nth-child(1) > rect:nth-child(1)"

    actionChains = ActionChains(driver)

    button = driver.find_element(By.CSS_SELECTOR, cssSelector_OpenMenu)
    actionChains.move_to_element(button).click().perform()
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
for i in range(0,len(coords),2):
    selectWall()
    time.sleep(0.20)
    drawWall(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1])

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