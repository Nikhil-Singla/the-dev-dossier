# os for file management
import os
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

# Build tuple of (class, file) to turn in
submission_dir = 'Testcase'
dir_list = list(os.listdir(submission_dir))

print(dir_list)

for aFILE in dir_list:
    #Using Chrome to access web
    driver = webdriver.Chrome()
    #Open the website
    driver.get('https://compilers.cool/oracles/o3/')

    time.sleep(1)
    #Find fileupload button
    file_Inputbutton = driver.find_element('name','input')

    file_location = os.path.join(os.getcwd(), "Testcase", aFILE)
    file_Inputbutton.send_keys(file_location)

    time.sleep(1)

    submit_button = driver.find_element(By.XPATH,'//input[@type="submit"]')
    submit_button.click()

    time.sleep(2)
    
    get_source = driver.page_source

    search_text = "OUTPUT FILE"
    x_index = get_source.find(search_text)

    if x_index != -1:
        y = "<br></pre>"
        y_index = get_source.find(y, x_index + len(search_text))
    
        if y_index != -1:   
            result = get_source[x_index + len(search_text):y_index]
            deletion = len('<br><pre style="background:white;overflow:visible;padding-bottom:0px">')
            result = result[deletion::]
        else:
            print("Element y not found after element x.")
    
    else:
        print("Element x not found in the string.")

    outputFILE = aFILE[:len(aFILE)-2:] + "expected"
    # path = os.path.join(os.getcwd(), "/Output/",outputFILE)

    with open(outputFILE, 'w') as f:
        f.write(result)

    search_text = "STDERR"
    x_index = get_source.find(search_text)
    if x_index != -1:
        y = "<br></pre>"
        y_index = get_source.find(y, x_index + len(search_text))
    
        if y_index != -1:   
            result = get_source[x_index + len(search_text):y_index]
            deletion = len('<br><pre style="background:white;overflow:visible">')
            result = result[deletion::]
        else:
            print("Formatting Error")
    else:
        result = ""

    errorFILE = aFILE[:len(aFILE)-2:] + "err.expected"
    # path = os.path.join(os.getcwd(), "/Error/",errorFILE)
    with open(errorFILE, 'w') as f:
        f.write(result)

    driver.close()