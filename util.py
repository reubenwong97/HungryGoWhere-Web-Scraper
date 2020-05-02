from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import time

def before(base_str, str_to_find):
    """
    args:
    base_str: main string to be parsed
    str_to_find: trigger string

    returns:
    text before str_to_find
    """
    pos_a = base_str.find(str_to_find)
    if pos_a == -1:
        return ""
    return base_str[0:pos_a]

def after(base_str, str_to_find):
    """
    args:
    base_str: main string to be parsed
    str_to_find: trigger string

    returns:
    text after str_to_find
    """
    # Find and validate first part.
    pos_a = base_str.rfind(str_to_find)
    if pos_a == -1: 
        return ""
    # Returns chars after the found string.
    adjusted_pos_a = pos_a + len(str_to_find)
    if adjusted_pos_a >= len(base_str): 
        return ""
    return base_str[adjusted_pos_a:]

def scroll_to_bottom(driver):
    SCROLL_PAUSE_TIME = 2.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def find_links_imgs(driver):
    links  = driver.find_elements_by_xpath("//article[@class='item restaurant_item']/div/div/h2/a")
    images = driver.find_elements_by_xpath("//article[@class='item restaurant_item']/figure/a/img")
    img_urls = []
    urls = []
    for link in links:
        url = link.get_attribute("href")
        urls.append(url)
    for image in images:
        img_url = image.get_attribute("data-original")
        img_urls.append(img_url)
    # Remove duplicates from partial scrolling
    urls = list(urls)
    return urls, img_urls

def get_granular(driver, data, name):
    spec_exist = False
    open_exist = False
    cuisine_exist = False
    # Selenium parsing
    summary = driver.find_element_by_xpath("//div[@class='module-ibl-summary']")
    stall_name = summary.find_element_by_tag_name("h1").text
    address = summary.find_element_by_tag_name("p").text

    data["Hawker Centre"].append(name)
    data["Stall Name"].append(stall_name)
    data["Address"].append(address)

    # BS4 parsing
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for dl in soup.find_all('dl'):
        text = dl.text
        if "Cuisine" in text:
            cuisine_exist = True
            cuisine = after(text, "Cuisine")
            data["Cuisine"].append(cuisine)
        elif "Opening Hours" in text:
            open_exist = True
            opening = after(text, "Opening Hours")
            data["Opening Hours"].append(opening)
        elif "Specialties" in text:
            spec_exist = True
            specialities = after(text, "Specialties")
            data["Specialties"].append(specialities)
    if not spec_exist:
        data["Specialties"].append("null")
    if not open_exist:
        data["Opening Hours"].append("null")
    if not cuisine_exist:
        data["Cuisine"].append("null")

    # Throw back out for persistence
    return data

def query_gen(name):
    query_name = name.replace(" ", "+")
    return query_name

def validate_page(driver):
    result_header_element = driver.find_element_by_xpath("//div[@class='search-result-head']/span")
    result_text = result_header_element.text
    result_components = result_text.split(" ")
    num_results = int(result_components[0])
    if num_results == 0:
        return False
    return True

#* Example csv
# +----------------------------------+-------------+------------------------+----------+---------------+-------------+
# |            Stall Name            | Food Centre |         Address        | Cuisine  | Opening Hours | Specialties |
# +----------------------------------+-------------+------------------------+----------+---------------+-------------+
# | Value 1                          | Value 2     | 123                    |     10.0 |               |             |
# | Separate                         | cols        | with a tab or 4 spaces | -2,027.1 |               |             |
# | This is a row with only one cell |             |                        |          |               |             |
# +----------------------------------+-------------+------------------------+----------+---------------+-------------+