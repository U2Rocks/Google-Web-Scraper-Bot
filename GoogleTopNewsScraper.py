import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

# use selenium to open dynamic page
url = 'https://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)
page = driver.page_source
driver.close()


# get top google news page and parse html
soup = BeautifulSoup(page, 'html.parser')

# get main body of html content that holds news stories
news_block = soup.find(class_='lBwEZb BL5WZb xP6mwf')


# find all sub-content containers
news_containers = news_block.find_all(class_='VDXfz')

print(news_containers)

# use loops to extract relevant links
link_expression = './[a-zA-Z]+/[a-zA-Z0-9=;:%-]+'
relevant_links_raw = []
for item in news_containers:
    working_item = re.compile(r'./[a-zA-Z]+/[a-zA-Z0-9=;:%-]+')
    item_result = working_item.search(str(item))
    relevant_links_raw.append(item_result.group())

print(relevant_links_raw)

# add google context to make links valid for selenium and place in new list
relevant_links = []
for link in relevant_links_raw:
    corrected_link = link[1:]
    new_link = 'https://news.google.com' + corrected_link
    relevant_links.append(new_link)

print(relevant_links)
# loop through relevant links and find the corresponding first h1 and h2 tags from the pages
title_list = []
for link in relevant_links:
    test_page = requests.get(link)
    soup2 = BeautifulSoup(test_page.text, 'html.parser')
    article_title = soup2.find('h1')
    if article_title == []:
        article_title = soup2.find('h2')
    if article_title == []:
        article_title = soup2.find(class_='style-scope ytd-video-primary-info-renderer')
    url_working = re.compile(r'(?<=\>).*(?=\<)')
    try:
        url_result = url_working.search(str(article_title))
        title_list.append(url_result.group())
    except AttributeError:
        url_result = "No result"
        title_list.append(url_result)


print(title_list)

# put data into dataframe for checking errors

news_story_chart = pd.DataFrame({
     'URLS': relevant_links,
     'Article Titles': title_list
 })

# put data into a csv file
# news_story_chart.to_csv('Daily Headlines')






# put lists into a pandas data frame

# output a result to check final result

# put result of info scrape into csv file

random_variable = 2

