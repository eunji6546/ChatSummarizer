import selenium 
from selenium import webdriver 

# Using chrome to access web 
driver = webdriver.Chrome(executable_path='./chromedriver') 

# Implicit wait 
driver.implicitly_wait(3)

# Open the website 
driver.get('http://speller.cs.pusan.ac.kr/PnuWebSpeller') 

input_form = driver.find_element_by_name('text1').send_keys('hi man')
driver.find_element_by_id('btnCheck').click()
