from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.webdriver.support.select import Select
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import csv
from threading import Thread
from helpful_functions import *
from math import ceil
import pandas as pd
import numpy as np

def selenium_spider():
    PATH = ChromeDriverManager().install()
    driver = Chrome(PATH)
    wait = WebDriverWait(driver, 15)
    ##########   Filters (you can change the vallues as you want) ########

    Maximum_Breed_count = '0'
    Minimum_Purity      = '6'

    ##############################


    url = "https://axie.zone/finder?search=breed_count:"+str(Maximum_Breed_count)+";purity:"+str(Minimum_Purity)+";page:{};view_genes"

    # avoid cookies
    try:
        driver.get(url.format(str(1)))
        #sleep(3)      # sleep(1) = wait 1 second , you can change it if the server slow
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.result_genes')))
        cookies = driver.find_element_by_css_selector("#hide_cookiebanner")
        cookies.click()
    except:
        print("the server is slow please try again or change the sleep time value in line 1")


    # get the total of Axies found
    try:
        #sleep(7)
        all_axies = int(driver.find_element_by_css_selector(".search_result_count").text) 
    except:
        print("Error while Insert filters: the server is slow , please try agin ,or change the sleep time value in line 2")
    driver.quit()

    # get all pages links

    links = [url.format(i) for i in range(ceil(all_axies/12))]    # ceil(all_axies/12)
    print("--------------------------------------------")
    print("all axies: ",all_axies)
    print("pages: ",len(links))
    print("---------------------------------------------")



    #store the filtred results
    csv_file = 'filtred_data.csv'
    csv_columns = ["id","name","links","stats(hp,speed,skil,morale)","Meta Score","class"]
    try:
        with open(csv_file, 'w', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
    except IOError:
        print("I/O error")
    # Apply filter to the results
    # you can change it if the server slow (value is in second)
    waiting_time = 3
    threads_number = 10
    multi_threading(links,csv_columns,csv_file,threads_number,waiting_time)

    #match the results


    df = pd.read_csv("filtred_data.csv")
    prices = pd.read_csv("prices.csv")
    prices = prices.drop_duplicates(subset="id")
    prices['id'] = prices['id'].map(lambda x: int(x))
    df['id']     = df['id'].map(lambda x: int(x))

    filtred_ids = df['id'].values
    all_ids = prices['id'].values

    prices_ = []
    for id in filtred_ids:
        if id in all_ids:
            idx = np.where(all_ids == id)[0][0]
            prices_.append(prices['price'].values[idx])
        else:
            idx = None
            prices_.append(idx)
        
    df['price'] = np.array(prices_)


    df = df.sort_values('price')
    df.to_csv("final_out.csv",index=False)



        
    '''

    links = pd.read_csv("demo.csv")["links"].tolist()

    csv_file = 'data.csv'
    csv_columns = ["links","price"]

    try:
        waiting_time = 2   # you can change it if the server slow (value is in second)
        threads_number = 6
        multi_threading_data(links,csv_columns,csv_file,threads_number,waiting_time)
    except:
        print("the server is slow please try again or change the waiting time value in line 3")

    '''




