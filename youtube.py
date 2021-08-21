import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

def searching(text, driver, count):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"container\"]"))
        )
    finally:
        search = driver.find_element_by_xpath("//*[@id=\"search\"]")
        search.send_keys("travel")
        driver.find_element_by_xpath("//*[@id=\"search-icon-legacy\"]").click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/div/ytd-toggle-button-renderer/a/tp-yt-paper-button"))).click()                            
    driver.implicitly_wait(5) 
    driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[2]/ytd-search-filter-renderer[2]/a/div").click()
    channels = []
    for i in range(1, count):
        added = set()
        link = driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-renderer[{}]/div/div[2]/a".format(i)).get_attribute("href")
        if link not in added:
            channels.append(link)
            added.add(link)
            print(link)
    return channels

driver = webdriver.Chrome()
driver.get("https://www.youtube.com/")
searching("travel", driver, 10)

