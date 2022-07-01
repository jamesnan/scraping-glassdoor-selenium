# Scraping Glassdoor.ca

Web scraping job listing  of top Canada cities  from "Glassdoor.ca" with Python and Selenium.

* By using Selenium, we can search by job title and city to get the WebElement of job listing page for each city, then go through each sub page and job card to retrieve job information. 
* With each job, I got the following:  Job title,Salary Estimation, Job Description, Rating, Company, Location, Size, Founded Date, Type of Ownership, Industry, Sector, Revenue, Website
* Scrapped information will be saved save in a csv file for data analysis.
         
## Build with 
* Python: Version 3.7  
* Packages: selenium, csv, time

## Chromedriver
* To run Selenium tests on Chrome, we need to download <b><i>chromedriver.exe</i></b>  from [here](https://chromedriver.chromium.org/downloads).
* Then add the chromedriver path to the environment, or use <i>driver = webdriver.Chrome(executable_path="chrome path")</i>.
         
## Reference: 
* https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905  
* https://github.com/arapfaik/scraping-glassdoor-selenium                      
