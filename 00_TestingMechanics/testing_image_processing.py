import os
import time
import cv2
import numpy as np
import pyautogui

from selenium import webdriver
from selenium.webdriver import Firefox, FirefoxOptions, ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.action_builder import ActionBuilder

# ---------- Constants ----------
URL = 'https://cvdlab.github.io/react-planner/'
CSS_OPEN_MENU = ".toolbar > div:nth-child(4) > div:nth-child(1) > svg:nth-child(1)"
CSS_WALL_FIRST = "#app > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(3)"
CSS_WALL_NEXT = "#app > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(3)"
CSS_GRID = "#app > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > svg:nth-child(1) > g:nth-child(2) > g:nth-child(2) > g:nth-child(2) > g:nth-child(1) > rect:nth-child(1)"
CSS_SAVE_BTN = ".toolbar > div:nth-child(2) > div:nth-child(1) > svg:nth-child(1) > path:nth-child(1)"

# ---------- Setup ----------
def setup_driver():
    opts = FirefoxOptions()
    opts.add_argument("--width=4000")
    opts.add_argument("--height=4000")
    opts.add_argument('--headless')
    driver = Firefox(options=opts)
    driver.get(URL)
    driver.implicitly_wait(10)
    return driver

driver = setup_driver()
actionChains = ActionChains(driver)

# ---------- Screenshot Initial State ----------
def take_screenshot(filename='screenie.png'):
    time.sleep(1)
    driver.save_screenshot(filename)

take_screenshot()

# ---------- File Paths ----------
current_dir = os.path.dirname(os.path.abspath(__file__))
image_file = "floor_plan.png"
output_file = "output.png"
image_path = os.path.join(current_dir, image_file)
output_path = os.path.join(current_dir, output_file)

if not os.path.isfile(image_path):
    raise FileNotFoundError(f"Image file '{image_file}' not found.")

# ---------- Image Processing ----------
def getWalls(image_path, threshold_area, canny_threshold1, canny_threshold2):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(thresholded, canny_threshold1, canny_threshold2)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(edges, connectivity=8)
    mask = np.zeros_like(labels, dtype=np.uint8)

    for label in range(1, num_labels):
        if stats[label, cv2.CC_STAT_AREA] > threshold_area:
            mask[labels == label] = 255

    result = cv2.bitwise_and(edges, edges, mask=mask)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    dilated = cv2.dilate(result, kernel, iterations=1)
    cv2.imwrite(output_path, dilated)

def reduction(pathToOutput):
    img = cv2.imread(pathToOutput, cv2.IMREAD_GRAYSCALE)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    eroded_image = cv2.erode(img, kernel, iterations=9)
    cv2.imwrite(output_path, eroded_image)

def detect_line_segments(image_path):
    image = cv2.imread(image_path, 0)
    edges = cv2.Canny(image, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=100, minLineLength=20, maxLineGap=10)
    dimensions = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            dimensions.append((x1, y1, x2, y2, length, angle))

    return dimensions

threshold_area = 90
canny_threshold1 = 10
canny_threshold2 = 10

getWalls(image_path, threshold_area, canny_threshold1, canny_threshold2)
reduction(output_path)
line_segments = detect_line_segments(output_path)

list_of_xcor, list_of_ycor = [], []
for segment in line_segments:
    x1, y1, x2, y2, length, angle = segment
    print(f"Start Point: ({x1}, {y1}), End Point: ({x2}, {y2}), Length: {length}, Angle: {angle}")
    list_of_xcor += [x1, x2]
    list_of_ycor += [y1, y2]

coords = list(map(list, zip(list_of_xcor, list_of_ycor)))

# ---------- Selenium Automation ----------
def selectWall(i):
    button = driver.find_element(By.CSS_SELECTOR, CSS_OPEN_MENU)
    actionChains.move_to_element(button).click().perform()
    time.sleep(0.20)
    cssSelector_Wall = CSS_WALL_NEXT if i != 0 else CSS_WALL_FIRST
    button = driver.find_element(By.CSS_SELECTOR, cssSelector_Wall)
    actionChains.move_to_element(button).click().perform()

def drawWall(x1, y1, x2, y2):
    button = driver.find_element(By.CSS_SELECTOR, CSS_GRID)
    Offset_X1, Offset_Y1 = x1 - 1500, y1 - 1000
    Offset_X2, Offset_Y2 = x2 - 1500, y2 - 1000
    actionChains.move_to_element_with_offset(button, Offset_X1, Offset_Y1).click()
    actionChains.move_to_element_with_offset(button, Offset_X2, Offset_Y2).click()
    actionChains.send_keys(Keys.ESCAPE).perform()

for i in range(0, len(coords), 2):
    selectWall(i)
    time.sleep(0.20)
    drawWall(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1])

def saveProject():
    time.sleep(0.20)
    button = driver.find_element(By.CSS_SELECTOR, CSS_SAVE_BTN)
    actionChains.move_to_element(button).click().perform()
    time.sleep(0.20)
    driver.switch_to.alert.accept()

saveProject()
time.sleep(1)
print("clicked")
driver.quit()
