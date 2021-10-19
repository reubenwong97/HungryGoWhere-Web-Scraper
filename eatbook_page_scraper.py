from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd

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

driver = webdriver.Chrome('C:/Users/Reuben/Desktop/chromedriver_win32/chromedriver')

total_pages = 94
page = 1

# Test on single page
url = 'https://eatbook.sg/yi-zi-wei//'
driver.get(url)
header = driver.find_elements_by_xpath("//div[@class='post-header']/h1")[0].text
store = before(header, "Review")
categories = driver.find_elements_by_xpath("//div[@class='post-header']/span[@class='cat']/a")
print(store)
for category in categories:
    if "REVIEW" not in category.text and category.text != "SINGAPOREAN":
        print(category.text.capitalize())
img_url_element = driver.find_elements_by_xpath("//div[@class='post-entry']/p/img")[0].get_attribute("src")
print(img_url_element)
review_element = driver.find_element_by_id("review")
# Possible to find child elements from parent WebElements
score = review_element.find_element_by_xpath("//div[@class='review-total-wrapper']/span").text
review_desc = review_element.find_element_by_xpath("//div[@class='review-desc']")
review_p = review_desc.find_elements_by_tag_name('p')
for element in review_p:
    if "Address" in element.text:
        print(after(element.text, "Address: "))
    elif "Opening hours" in element.text:
        print(after(element.text, "Opening hours: "))
    else:
        pass

driver.close()
driver.quit()

# for page in range(1, total_pages+1):
#     url = 'https://eatbook.sg/category/food-reviews/page/' + str(page) + '/'
#     # navigates to, and waits for page to be fully loaded
#     driver.get(url)
#     assert 'food-reviews' in driver.title


