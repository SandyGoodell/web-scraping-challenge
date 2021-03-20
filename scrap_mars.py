from splinter import Browser 
from bs4 import BeautifulSoup 
import pandas as pd 
import requests
import time

def init_browser():
    executable_path = {"executable_path": "C:/Users/sgoodel3/.wdm/drivers/chromedriver/win32/88.0.4324.96/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Scrape NASA MARS NEW SITE #
    # store url #
    url = "https://mars.nasa.gov/news/"
    # visit site
    browser.visit(url)
 
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=10)

    # scrape into soup
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Assign variables #
    news_title = news_soup.find_all('div', class_="list_text")[0]
    news_title = news_title.find(class_ = "content_title").text
    news_p = news_soup.find_all("div", class_="article_teaser_body")[0].text

    print(news_title)
    
    #-----------------------------------------------------------------------------------#
    #JPL MARS SPACE IMAGES - FEATURED IMAGE #

    # store base and image url #
    image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    

    # visit site
    browser.visit(image_url)
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
     
    # Website URL
    image_base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'

    # Get the full image - using the style tag #
    #partial_image_url  = image_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    partial_image_url = image_soup.find('body')
    print(partial_image_url)

    # combine base url with partial url #
    featured_image_url = image_base_url + partial_image_url
    
   

    # method used for closing browser
    browser.quit()
    return

if __name__ == "__main__":
    print(scrape())
        



