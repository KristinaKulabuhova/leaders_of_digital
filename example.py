import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

def inf_blogger(link, driver):
    driver.get(link)
    driver.implicitly_wait(5) 

    information = {'name': None, 'link': None, 'followers': None, 'photo': None, 'mail': None, 'telephone': None, 'likes': None, 'date_last_post': None}

    information["link"] = link

    name = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/h2").text
    information["name"] = name

    followers = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title")
    information["followers"] = followers

    profile = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]").text
    mail = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', profile)
    telephone = ["".join(phone) for phone in  re.findall('(\+7|8|7).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})', profile)]
    information["mail"] = mail
    information["telephone"] = telephone

    photo = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/div/div/span/img").get_attribute("src")
    information["photo"] = photo

    likes = find_likes(link, driver)
    information["likes"] = likes

    date = last_post(link, driver)
    information["date_last_post"] = date

    return information


def find_likes(link, driver):

    likes = []
    for i in range(1, 11):
        for j in range(1, 4):
            try:
                driver.get(link)
                if i > 4:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/section/main/div/div[3]/div[1]/div/button/div"))).click()
                link_post = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[3]/article/div[1]/div/div[{}]/div[{}]/a".format(i, j)).get_attribute("href")
                driver.get(link_post)
                driver.implicitly_wait(5)
                likes.append(driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/a/span").text)
            except:
                pass
    return likes


def last_post(link, driver):
    driver.get(link)
    driver.implicitly_wait(5)
    link_post = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a").get_attribute("href")
    driver.get(link_post)
    driver.implicitly_wait(5)
    date = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[2]/a/time").get_attribute("datetime")

    return date

def search_bloggers(text):
    list_bloggers = []
    driver.get("https://www.instagram.com/ptuxerman/")
    driver.implicitly_wait(5) 
    elem = driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
    elem.clear()
    elem.send_keys(text)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "-qQT3"))
        )
    finally:
        bloggers = driver.find_elements_by_class_name('-qQT3')
        added = set()

        for i in bloggers:
            href = i.get_attribute("href")
            if "tags" not in href and "locations" not in href and href not in added:
                list_bloggers.append(href)
                added.add(href)
            
    return list_bloggers

#------------начало---------------#

driver = webdriver.Chrome()
driver.get("https://www.instagram.com/accounts/login/")
try:
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label"))
    )
finally:
    password = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label/input")
    password.clear()
    password.send_keys("KristinaKristina")

    login = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[1]/div/label/input")
    login.clear()
    login.send_keys("89851878142")
driver.implicitly_wait(10) 
driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button/div").click()
driver.implicitly_wait(10) 

#----------логирование------------#
#driver.get("https://www.instagram.com/")
#try:
#    elem = WebDriverWait(driver, 10).until(
#        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div"))
#    )
#finally:
#    password = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")
#    password.clear()
#    password.send_keys("KristinaKristina")
#
#    login = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")
#    login.clear()
#    login.send_keys("89851878142")
#driver.implicitly_wait(5) 
#button = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]").click()
#driver.implicitly_wait(10) 
#---------------------------------#

dict = inf_blogger("https://www.instagram.com/ptuxerman/", driver)
driver.close()

for key, value in dict.items():
    print(key, value)

bloggers = search_bloggers("Travel Bloggers")

for elem in bloggers:
    inf_blogger(elem, driver)
#search_bloggers("Путешествие", "test.txt")
#search_bloggers("Travel", "test.txt")
#search_bloggers("Travelling", "test.txt")

