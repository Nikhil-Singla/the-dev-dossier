## id="svg-drawing-paper"
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
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

opts = FirefoxOptions()
opts.add_argument("--width=1920")
opts.add_argument("--height=1080")
driver = Firefox(options=opts)
driver.get('https://cvdlab.github.io/react-planner/')


input()

actions = ActionChains(driver)

element = driver.find_element(By.ID, "/html/body/div/div[1]/div[1]/div[4]/svg/g/g/g/g/g/g/g[1]/g[1]/line[96]")
driver.execute_script("arguments[0].scrollIntoView(true);", element)
## element.click()
time.sleep(2)

element.click()

input()