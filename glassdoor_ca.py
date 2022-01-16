# -*- coding: utf-8 -*-
"""
Created on Sat Jan 6, 2022

author: Zhigang Nan
url: https://github.com/jamesnan/scraping-glassdoor-selenium
"""

import csv
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import warnings
warnings.filterwarnings('ignore')

DEBUG = False
DEBUG_CITY_NUM = 3        # number of cities for debug
DEBUG_CARD_NUMBERS = 3    # number of job cards per page for debug
DEBUG_PAGES_PER_CITY = 3  # duplicated results after page 7
PROMPT = False      
global driver

def login(accout):
    global driver

    with open(accout) as f:
        lines=f.readlines()
        my_email=lines[0].strip()
        my_password=lines[1].strip()

    for counter in range(3):
        try:
            driver.find_element_by_class_name("d-none.d-lg-block.p-0.LockedHomeHeaderStyles__signInButton").click()
            print("loging button clicked")
        except Exception as e:
            print("Login exception:" +str(e)) 
        
        try:    
            userEmail = driver.find_element_by_id('userEmail')
            userEmail.send_keys(my_email)
            userEmail.send_keys(Keys.RETURN)
            sleep(1)
        except Exception as e:
            print("userEmail exception:" +str(e))
            
        try: 
            password = driver.find_element_by_id('userPassword')
            password.send_keys(my_password)
            password.send_keys(Keys.RETURN)
            sleep(1)
            break
        except Exception as e:
            print("password exception:" +str(e))

    try:
        driver.find_element_by_name('submit').click()
        print("submit button clicked")
    except Exception as e:
        print("Submit exception:" + str(e))



def get_job_info(job_card):
    """Extract job data from single card"""

    global driver
    
    collected_successfully = False
            
    while not collected_successfully:
        try:
            job_title = job_card.find_element_by_xpath('.//a[@data-test="job-link"]').text
            company_name = job_card.find_element_by_xpath('.//div[2]/div[1]/a/span').text
            location = job_card.find_element_by_xpath('.//div[2]/div[2]/span').text
            collected_successfully = True
        except:
            time.sleep(3)

    try:
        salary_estimate = job_card.find_element_by_xpath('.//span[@data-test="detailSalary"]').text
    except NoSuchElementException:
        salary_estimate = "" #You need to set a "not found value. It's important."
    
    try:
        rating = job_card.find_element_by_xpath('.//div[1]/span').text
    except NoSuchElementException:
        rating = ""    
 
    #Printing for debugging
    if DEBUG:
        print("----------------Job card information----------------")
        print("Job Title: {}".format(job_title))
        print("Company Name: {}".format(company_name))
        print("Location: {}".format(location)) 
        print("Salary Estimate: {}".format(salary_estimate))
        print("Rating: {}".format(rating))
        print("--------------------------------------------------------")   
        
   
    try:
        driver.find_element_by_xpath('.//div[@data-item="tab" and @data-tab-type="overview"]/sapn').click()
    except NoSuchElementException:  # some job postings do not have the "Company" tab.
        job_description=""
        size = ""
        founded = ""
        type_of_ownership = ""
        industry = ""
        sector = ""
        revenue = ""
        website = ""

    try:
        job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text.replace("\n", " ")
    except:
        job_description= ""
        
    try:
        size = driver.find_element_by_xpath('.//div[@id="EmpBasicInfo"]//span[text()="Size"]//following-sibling::*').text
    except NoSuchElementException:
        size = ""
    
    try:
        founded = driver.find_element_by_xpath('.//div[@id="EmpBasicInfo"]//span[text()="Founded"]//following-sibling::*').text
    except NoSuchElementException:
        founded = ""
        
    try:
        type_of_ownership = driver.find_element_by_xpath('.//div[@id="EmpBasicInfo"]//span[text()="Type"]//following-sibling::*').text
    except NoSuchElementException:
        type_of_ownership = ""  
    try:
        industry = driver.find_element_by_xpath('.//div[@id="EmpBasicInfo"]//span[text()="Industry"]//following-sibling::*').text
    except NoSuchElementException:
        industry = ""  
    try:
        sector = driver.find_element_by_xpath('.//div[@id="EmpBasicInfo"]//span[text()="Sector"]//following-sibling::*').text
    except NoSuchElementException:
        sector = ""
    try:
        revenue = driver.find_element_by_xpath('.//div[@id="EmpBasicInfo"]//span[text()="Revenue"]//following-sibling::*').text
    except NoSuchElementException:
        revenue = ""

    try:
        website =  driver.find_element_by_xpath('//div[@id="EmpBasicInfo"]/div[2]/div/a').get_attribute("href").strip()
    except NoSuchElementException:    
        website = ""
    
    #Printing for debugging
    if DEBUG:
        print("----------------Company Detail----------------")    
        print("Job Description: {}".format(job_description[:500]))
        print("Size: {}".format(size))
        print("Founded: {}".format(founded))
        print("Type of Ownership: {}".format(type_of_ownership))
        print("Industry: {}".format(industry))
        print("Sector: {}".format(sector))
        print("Revenue: {}".format(revenue))
        print("website: {}".format(website))
        print("--------------------------------------------------------")    

    return (job_title, salary_estimate,job_description,rating, company_name, location,size,
            founded,type_of_ownership,industry,sector,revenue,website)    


def get_url(job, city):
    """Generate url from position and location"""
    global driver
    
    jobTitle = driver.find_element_by_id("sc.keyword")
    print("jobTitle=" +str(jobTitle))
    jobTitle.send_keys(Keys.CONTROL + Keys.BACKSPACE *5) 
    jobTitle.send_keys(job)
    sleep(1)

    location = driver.find_element_by_id("sc.location")
    print("location=" +str(location))  
    location.send_keys(Keys.CONTROL + Keys.BACKSPACE *5) # location.clear()
    location.send_keys(city)
    sleep(1)    
    
    try:
        driver.find_element_by_xpath('//*[@id="scBar"]/div/button').click()
        print("search clicked")
        sleep(2)
        return (driver.current_url )
    except Exception as e:
        print("search button exception:" +str(e))

    return (driver.current_url )


def close_prompt():
    global PROMPT
    global driver
    
    try:      
        prompt = driver.find_element_by_id('JAModal') 
        if prompt.text == "":
            print('func close_promt(), prompt.text ==""') 
            return 
        print('func close_promt(): found promt') 
    except Exception as e:
        print('func close_promt(), exeption: ' +str(e))    
        return

    try:
        prompt.find_element_by_class_name('SVGInline.modal_closeIcon').click()
        print(' x out worked')
    except Exception as e:
        print(' x out failed ' +str(e))            
    PROMPT = True


def get_page_records(cards):
    """Extract all cards from the page"""
    global driver
    scraped_jobs = []
   
    if DEBUG: # 3 cards for testing
        cards = cards[: DEBUG_CARD_NUMBERS]

    for card in cards:
        try: 
            card.click()
            sleep(2)
            
            print("click on the card, then check & close promt")
            if PROMPT == False:
                close_prompt()

            sleep(1)
            record = get_job_info(card) 
            scraped_jobs.append(record)
        except Exception as e:
            print('page excption ' +str(e))   
        
    return(scraped_jobs)


def extract_job_from_city(job, city):
    global driver

    url = get_url(job, city)
    sleep(1)
    
    driver.get(url)
    print("extract_job_from_city: "+str(city)+ " url="+str(url))
    print("extract_job_from_city: "+str(city)+ " start page->" + str(driver.current_url))
    
    scraped_jobs =[]
    pages_per_city = 7  # get duplicates after first 7 pages
    
    if DEBUG:
        pages_per_city =  DEBUG_PAGES_PER_CITY 

    # extract the job data
    for page in range(1, pages_per_city):  
        print("get record from page " + str(page)) 
        job_cards = driver.find_elements_by_class_name("react-job-listing")                                            
        scraped_jobs += get_page_records(job_cards)

        try:
            driver.find_element_by_xpath('//li[not(@disabled)]/a[@data-test="pagination-next"]').click()
            sleep(3)

            print("click next page->" + str(driver.current_url)+", then check & close promt")
            if PROMPT == False:
                close_prompt()
            sleep(1)
        except Exception as e:
            print("pagination-next exeption" +str(e))                    
            break
            
    print("No Next Page:")              
    return (scraped_jobs)                                          
        

def save_data_to_file(records):
    """Save data to csv file"""
    if DEBUG:
        output_file= 'glassdoor_debug.csv'
    else:
        output_file= 'glassdoor.csv'
        
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Job Title', 'Salary Estimation','Job Description', 'Rating','Company', 'Location',  'Size',
                         'Founded Date','Type of Ownership','Industry','Sector','Revenue','Website'])
        writer.writerows(records)


def main(job, num_of_cities):
    global driver
   
    driver = webdriver.Chrome()
    driver.maximize_window()
    url= "https://www.glassdoor.ca/"
    driver.get(url)
    sleep(3)
    
    login('account.txt')
    
    print("initial url=" +str(url))
    print("initial driver.current_url=" +str(driver.current_url) )
    
    if DEBUG:
        num = DEBUG_CITY_NUM
    else:
        num = num_of_cities
        
    """Extract salary data from top canada cities"""
    # get the list of largest us cities
    with open('100_canada_city.csv', newline='') as f:
        reader = csv.reader(f)
        # a reader typically returns each row as a list
        cities = [city for row in reader for city in row]
        cities = cities[:num]     
        
    # extract job_data data for each city
    scraped_jobs = []
    for city in cities:
        result = []
        print ("scraping city="+str(city))
        result = extract_job_from_city(job, city)
        print ("scraping city completed")
        if result:
            scraped_jobs += result
            
    # close driver and save records
    driver.quit()
    save_data_to_file(scraped_jobs)  
    print ("The End")

if __name__ == "__main__":
    main('Data Scientist',10)       
