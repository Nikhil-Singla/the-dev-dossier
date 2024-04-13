from selenium import webdriver
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.by import By
import time 

# Initialize options for the FIREFOX driver
opts = FirefoxOptions()
opts.add_argument("--width=4000")
opts.add_argument("--height=4000")
opts.add_argument('--headless')

# This option needs to be enabled, and it will remove the GUI, only do it when clicking works without the GUI
# opts.add_argument("-headless") 

# Initialize the FIREFOX driver. BASICALLY OPENS THE WEB BROWSER
driver = Firefox(options=opts)
driver.get('https://cvdlab.github.io/react-planner/')

driver.implicitly_wait(10) # gives an implicit wait for 10 seconds

# xPath = "/html/body/div/div[1]/aside[1]/div[4]/div/svg/path"
cssSelector_OpenMenu = ".toolbar > div:nth-child(4) > div:nth-child(1) > svg:nth-child(1)"
cssSelector = "#app > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > svg:nth-child(1) > g:nth-child(2) > g:nth-child(2) > g:nth-child(2) > g:nth-child(1) > rect:nth-child(1)"

actionChains = ActionChains(driver)

button = driver.find_element(By.CSS_SELECTOR, cssSelector_OpenMenu)
actionChains.move_to_element(button).click().perform()

cssSelector_Wall = "#app > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(3)"
button = driver.find_element(By.CSS_SELECTOR, cssSelector_Wall)
actionChains.move_to_element(button).click().perform()

cssSelector_Grid = "#app > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > svg:nth-child(1) > g:nth-child(2) > g:nth-child(2) > g:nth-child(2) > g:nth-child(1) > rect:nth-child(1)"
button = driver.find_element(By.CSS_SELECTOR, cssSelector_Grid)
actionChains.move_to_element_with_offset(button, 1, 1)

actionChains.click()
actionChains.move_to_element_with_offset(button, 100, 100)
actionChains.click()
##actionChains.move_to_element_with_offset(button, -1500, -1000)


cssSelector_Save = ".toolbar > div:nth-child(2) > div:nth-child(1) > svg:nth-child(1)"
button = driver.find_element(By.CSS_SELECTOR, cssSelector_Save)

actionChains.perform()
webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

time.sleep(1)

driver.save_screenshot('screenie.png')

cssSelector_Save = ".toolbar > div:nth-child(2) > div:nth-child(1) > svg:nth-child(1) > path:nth-child(1)"
button = driver.find_element(By.CSS_SELECTOR, cssSelector_Save)
actionChains.move_to_element(button).click().perform()

driver.switch_to.alert.accept()

##driver.find_element(By.CSS_SELECTOR, cssSelector).click()
print("clicked")
time.sleep(1)

driver.close()