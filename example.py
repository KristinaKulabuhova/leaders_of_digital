import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

def inf_blogger(link, file_name):
    name = driver.find_element_by_class_name("rhpdm").text
    followers = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title")
    line = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]").text
    match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', line)
    file_name.write(' ' + name + ' ' + followers + ' ' + match + "\n")


def search_bloggers(text, file_name):
    driver.get("https://www.instagram.com/ptuxerman/")
    elem = driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
    elem.clear()
    elem.send_keys(text)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "-qQT3"))
        )
    finally:
        blogger = driver.find_elements_by_class_name('-qQT3')
        file = open(file_name, 'a')
        added = set()

        for i in blogger:
            href = i.get_attribute("href")
            if "tags" not in href and "locations" not in href and href not in added:
                file.write(href)
                inf_blogger(href, "test.txt")
                added.add(href)
            
        
        file.close()

driver = webdriver.Chrome()
driver.get("https://www.instagram.com/accounts/login/")
lement = WebDriverWait(driver, 5)

login = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[1]/div/label/input")
login.clear()
login.send_keys("")

password = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label/input")
password.clear()
password.send_keys("")

button = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]").click()
search_bloggers("Travel Bloggers", "test.txt")
search_bloggers("Путешествие", "test.txt")
search_bloggers("Travel", "test.txt")
search_bloggers("Travelling", "test.txt")
driver.close()
