from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import csv
from threading import Thread
from math import ceil

PATH = ChromeDriverManager().install()


def get_filtred_results_links(driver,links,csv_columns,csv_file,witing_time):
    filtred_links = []
    for link in links:
        try:
            driver.get(link)
            #sleep(witing_time)
            wait = WebDriverWait(driver, 15)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.result_genes')))
            cards = driver.find_elements_by_css_selector(".result_genes a")
            for card in cards :
                gene_quality = float(card.find_element_by_css_selector(".purity_score span").text.replace("%",""))
                if gene_quality>=95:
                    pure_gene_link = card.get_attribute('href') 
                    name = card.find_element_by_css_selector("#search_result_container h3").text
                    hp = card.find_element_by_css_selector(".hp").text
                    speed = card.find_element_by_css_selector(".speed").text
                    skill = card.find_element_by_css_selector(".skill").text 
                    morale = card.find_element_by_css_selector(".morale").text 
                    stats = "(" + hp + "," + speed + "," + skill + "," + morale + ")"
                    meta_score = card.find_element_by_css_selector(".ability_score span").text 
                    classes = card.find_elements_by_css_selector("td")
                    class_ = classes[2].get_attribute("class")
                    id = int(re.search(r'\d+', pure_gene_link).group())
                    result = {"id":id,"name":name,"links":pure_gene_link,"stats(hp,speed,skil,morale)":stats,"Meta Score":meta_score,"class":class_}
                    print(result)
                    try:
                        with open(csv_file, 'a', encoding="utf-8") as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                            writer.writerow(result)
                    except IOError:
                        print("I/O error")
                    filtred_links.append(pure_gene_link)
        except:
            continue
    driver.quit()



def multi_threading(cards, csv_columns, csv_file, threads_number,waiting_time):
    cards_per_thread = len(cards) // threads_number
    threads = []
    for n in range(threads_number - 1):
        start = n * cards_per_thread
        end = start + cards_per_thread
        driver = Chrome(PATH)
        thread = Thread(target=get_filtred_results_links, args=[driver, cards[start:end], csv_columns, csv_file,waiting_time])
        thread.start()
        threads.append(thread)
    start = (n + 1) * cards_per_thread
    driver = Chrome(PATH)
    last_thread = Thread(target=get_filtred_results_links, args=[driver, cards[start:], csv_columns, csv_file,waiting_time])
    last_thread.start()
    threads.append(last_thread)
    for thread in threads:
        thread.join()

    
