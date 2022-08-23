import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import random

OPTIONS = Options()
PATH_URLS_NEW = os.path.join(os.curdir, 'urls_new')
PATH_DRIVER = os.path.join(os.curdir, 'chromedriver')

OPTIONS.add_argument('--disable-blink-features=AutomationControlled')
OPTIONS.add_experimental_option('useAutomationExtension', False)
OPTIONS.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(PATH_DRIVER, options=OPTIONS)

driver.get('https://us.feelunique.com/body/hand-care/hand-creams')
print("[LOG] loading the page ...")

try:
    cookie_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
        By.ID, 'notice-ok')))
    cookie_btn.click()
    print("[LOG] Click on the cookies button.")
    time.sleep(random.uniform(1, 5))
except:
    pass

while True:
    try:
        more_products_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.CSS_SELECTOR, '#fullcolumn > div.eba-component.loadMoreContainer > div.loadMore > a')))
        driver.execute_script('arguments[0].scrollIntoView(true);', more_products_btn)
        driver.execute_script('arguments[0].click();', more_products_btn)
        print("[LOG] Click on show more products button.")
        time.sleep(random.uniform(1, 5))

    except TimeoutException:
        print("[LOG] There isn't any more products to show.")
        break

    except KeyboardInterrupt:
        print("[LOG] The collect has been interrupted by the user.")
        break

    except:
        break
try:

    url_dicts = []
    time.sleep(5)
    products = driver.find_elements(
        By.CSS_SELECTOR, 'div[class="eba-component eba-product-listing"] div[class="Product"]')
    print("[LOG] Start collecting urls data.")

    for i, product in enumerate(products):
        print('----------------START----------------')
        url_dict = {
            'product_url': None,
            'n_reviews': None,
            'product_name': None,
            'product_price': None,
            'product_mean_rating': None
        }

        try:
            url_dict['product_name'] = product.find_element(By.CLASS_NAME, 'Product-summary').text
            print(url_dict['product_name'])
        except:
            pass

        try:
            product_prices = product.find_element(By.CLASS_NAME, 'Product-price')
            url_dict['product_price'] = product_prices.find_element(By.TAG_NAME, 'span').text

            print(url_dict['product_price'])
        except:
            pass

        try:
            url_dict['product_mean_rating'] = product.find_element(By.CSS_SELECTOR, 'span[data-aggregate-rating]') \
                .get_attribute('data-aggregate-rating')
            print(url_dict['product_mean_rating'])
        except:
            pass

        try:
            url_dict['n_reviews'] = product.find_element(By.CSS_SELECTOR, 'span[class="Rating-count"]') \
                .get_attribute('data-review-count')
            print(url_dict['n_reviews'])
        except:
            pass

        try:
            url_dict['product_url'] = product.find_element(By.CSS_SELECTOR, 'a[class="Product-link thumb "]') \
                .get_attribute('href')
            print(url_dict['product_url'])
        except:
            print("did not execute")
            pass

        url_dicts.append(url_dict)

        print('----------------FINISH----------------')

    with open(os.path.join(
            PATH_URLS_NEW, 'urls_new.json'), 'w', encoding='utf-8') as file_to_dump:
        json.dump(url_dicts, file_to_dump, indent=4, ensure_ascii=False)


except KeyboardInterrupt:
    print("[LOG] The collect has been interrupted by the user.")
    pass

except:
    print("[LOG] There is an error for the current url.")
    pass

print("------start collecting product and reviews data-----")

#try:
    #for url_dict in url_dicts:
        #try:
           #driver.get(url_dict['product_url'])
           #print("[LOG] Loading the page...")
           #time.sleep(random.uniform(1, 5))
        #except:


driver.quit()
