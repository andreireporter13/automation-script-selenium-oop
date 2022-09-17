# new script with Selenium and OOP;
#
############################################################################
#
#
# Author: Andrei C. Cojocaru
# Linkedin: https://www.linkedin.com/in/andrei-cojocaru-985932204/
# Facebook: https://www.facebook.com/webautomation.romania
# Tiktok: https://www.tiktok.com/@n0hacker_reporter13
# Twitter: https://twitter.com/andrei_reporter
# Youtube: https://www.youtube.com/channel/UCgx_Y9OHi5KPVzLJo9setxw/featured
# GitHub: https://github.com/andreireporter13
# Website: https://webautomation.ro/
# 
# 
############################################################################

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
# 
from selenium.webdriver.common.by import By
# 
from bs4 import BeautifulSoup
#
from fake_useragent import UserAgent
from time import sleep
#
import random
import pandas as pd
import csv


# global variable - link from book's site:
SITE_LINK = 'https://www.publi24.ro/'


# create a new class for my new script;
class AdsFinder:
    '''
    class create for gather sale data from libris.ro and another information
    '''


    def __init__(self, search_keyword: str, nr_pages: int, driver_path=Service(executable_path="/home/n0_hacker/Documents/telegram_bot/geckodriver")):

        # path to driver;
        self.driver_path = driver_path

        # atributes for search
        self.search_keyword = search_keyword
        self.nr_pages = nr_pages

        # set options;
        options = webdriver.FirefoxOptions()
        options.set_preference("general.useragent.override", UserAgent().random)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.headless = False # WebDriver off = True, on = False

        # open browser here;
        self.driver = webdriver.Firefox(service=self.driver_path, options=options)
        self.driver.get(SITE_LINK)
        
        # set another important attributes for this class;
        self.collected_data = []

        # call function gather_data and save_data_to_csv
        self.gather_data()
        sleep(1)
        self.save_data_to_csv()
    
    
    # acces site and search by keyword;
    def gather_data(self):

        '''
        This method for gather important data sale from publi24.ro
        '''
        
        sleep(1)

        try:
            # start search ads on publi24.ro;
            search_input = self.driver.find_element(By.ID, 'keyword').send_keys(self.search_keyword)
            button_click = self.driver.find_element(By.ID, 'btn-search').click()

            # search data with bs4
            for page in range(1, self.nr_pages + 1):
                print(f'Scraper collect data from page {page}!')

                new_soup = BeautifulSoup(self.driver.page_source, 'lxml')
                data_from_page = new_soup.findAll('div', class_='listing-data')

                # gather data with function;
                for data in data_from_page:

                    try: 
                        link = data.find('a', class_='maincolor').get('href')
                    except: 
                        link = '-'

                    try: 
                        title = data.find('a', class_='maincolor').text.strip()
                    except: 
                        title = '-'

                    try: 
                        price = data.find('div',
                                class_='large-4 medium-5 large-text-right medium-text-right columns prices').find('strong', 
                                class_='price maincolor').text.strip()
                    except:
                        price = '-'

                    try: 
                        location = data.find('label', class_='article-location').findAll('span')[0].text.strip()
                    except:
                        location = '-'
            
                    try: 
                        data_post = data.find('div', class_='small-12 columns bottom').find('label', 
                                    class_='article-date').text.strip()
                    except:
                        data_post = '-'

                    try: 
                        article_details = data.find('div', class_='small-12 columns bottom').find('label', 
                                            class_='article-details').text.strip()
                    except:
                        article_details = '-'

                    
                    # save data to class atribue self.collected_data
                    self.collected_data.append([link, title, price, location, data_post, article_details])

                # click to the next page
                sleep(random.randint(1, 3))
                
                next_page_button = new_soup.find('ul', class_='pagination radius').findAll('li')[-1].find('a').get('href')
                self.driver.get(next_page_button)
                sleep(random.randint(2, 5))

        except Exception as ex: 
            print(ex)

        finally: 
            # set time for sleep, driver working; 
            sleep(1)
            self.driver.quit()

    
    # save data to csv
    def save_data_to_csv(self): 

        header = ['link', 'title', 'price', 'location', 'data_post', 'article_details']
        df = pd.DataFrame(self.collected_data, columns=header)
        df.to_csv(f'{self.search_keyword}_publi24_data.csv', encoding='utf8')
        print('Done! CSV-file saved!')
    

# the engine of code;
if __name__ == "__main__":

    # data input()
    keyword_input = input('Scrie un cuvant cheie pentru a cauta pe publi24.ro: ')
    integer_input = input('Cate pagini vrei sa razuiesti? (Limita este 3 pagini): ')

    try:

        if 0 < int(integer_input) < 4: 
            if integer_input.isdigit(): 
                ads = AdsFinder(keyword_input, int(integer_input))
        else: 
            if int(integer_input) < 1: 
                print('Ai pus o valoare mai mica sau egala cu 0!')
            else: 
                print('Ai pus o valoare mai mare decat 3!')

    except:
        print('Ai introdus semne gresite!')
            