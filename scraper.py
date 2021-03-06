import re
import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def inf_blogger(link, driver):
    driver.get(link)
    
    profile = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]").text.lower()

    is_russia = re.findall("[а-яА-Я]+", profile) 
    for word in ['travel', 'russia', 'samara', 'journey', 'traveler']:
        if word in profile or len(is_russia) != 0 :  
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

            find_likes_views(link, driver, information)

            date = last_post(link, driver)
            information["date_last_post"] = date

            return information
        else:
            return

def find_likes_views(link, driver, information):
    likes = []
    views = []

    for i in range(1, 5): 
        for j in range(1, 4):
            driver.get(link)

            if i > 4:
                driver.implicitly_wait(10)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
            link_post = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[3]/article/div[1]/div/div[{}]/div[{}]/a".format(i, j)).get_attribute("href")
            driver.get(link_post)

            try: 
                WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/a/span")))
                like = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/a/span").text
                likes.append(like)
            except:
                view = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/span/span").text
                views.append(view)

                driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/span").click()
                like = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/div[4]/span").text
                likes.append(like)

    information["likes"] = likes
    information["views"] = views


def last_post(link, driver):
    driver.get(link)

    link_post = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a").get_attribute("href")
    
    driver.get(link_post)
    date = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[2]/a/time").get_attribute("datetime")

    return date



def search_bloggers(text, driver, count):
    list_bloggers = []

    all_inf_bloggers = []
    driver.get("https://www.instagram.com/explore/")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input"))).send_keys(text)
    driver.implicitly_wait(10)
    bloggers = driver.find_elements_by_class_name('-qQT3')
    driver.implicitly_wait(10)
    added = set()
  
    for i in bloggers:
        if count != 0:
            count = count - 1
            href = i.get_attribute("href")
            if "tags" not in href and "locations" not in href and href not in added:
                list_bloggers.append(href)
                added.add(href)
    
    for bloger in list_bloggers:
        all_inf_bloggers.append(inf_blogger(bloger, driver))
        print(all_inf_bloggers)

    return all_inf_bloggers



def init_scraper(login, password):
    driver = webdriver.Chrome()
    driver.implicitly_wait(60)

    options = Options()
    options.add_argument("user-data-dir=/tmp/auto")
    driver = webdriver.Chrome(chrome_options=options)

    if not os.path.isfile('auth_ok'):
        driver.get("https://www.instagram.com/accounts/login/")

        try:
            elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label")))

            login = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[1]/div/label/input").send_keys(login)
            password = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label/input").send_keys(password)  

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button/div"))).click()

        except:
            login = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input").send_keys(login)
            password = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input").send_keys(password)

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]"))).click()
    return driver
