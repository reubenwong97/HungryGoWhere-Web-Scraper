from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from util import scroll_to_bottom, find_links_imgs, get_granular, query_gen, validate_page
from gov_parser import get_hawker_names
from collections import defaultdict
import pandas as pd

# Cheat list exists for names stored differently in HungryGoWhere and data.gov.sg's database
# cheat_list = ['Tanglin Halt Market', 'Tekka Market', 'Tiong Bahru Market', 'Zion Riverside Food Centre']

driver = webdriver.Chrome('C:/Users/Reuben/Desktop/chromedriver_win32/chromedriver')
data = defaultdict(list)
base_url = 'https://www.hungrygowhere.com/building/'
gov_api_url = 'https://data.gov.sg/api/action/datastore_search?resource_id=8f6bba57-19fc-4f36-8dcf-c0bda382364d&limit=107'
hawker_names = get_hawker_names(gov_api_url)

for hawker_centre_name in hawker_names:
    query_name = query_gen(hawker_centre_name)
    query_url = base_url + query_name + '/'

    driver.get(query_url)
    if validate_page(driver):
        scroll_to_bottom(driver)
    else:
        continue

    detailed_links, img_urls = find_links_imgs(driver)
    data["Images"].extend(img_urls)

    for detailed_link in detailed_links:
        driver.get(detailed_link)
        # Collect for persistence
        data = get_granular(driver, data, hawker_centre_name)
    
    for key in data:
        print(key, len(data[key]))

    hawkerDf = pd.DataFrame.from_dict(data) 
    hawkerDf.to_csv('hawker_final.csv', index=False)

