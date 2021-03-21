#!/usr/bin/env python
# coding: utf-8


#import dependencies
# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import pymongo

def init_browser():
    executable_path = {"executable_path": "C:/Users/sgoodel3/.wdm/drivers/chromedriver/win32/88.0.4324.96/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()


    # ### NASA Mars News ###

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    print(html)
    print(news_soup.prettify())

    # Assign variables for what we are scrapping (New's Title and Paragraph)
    # Retrieve the latest news title and paragraph
    news_title = news_soup.find_all('div', class_="list_text")[0]
    news_title = news_title.find(class_="content_title").text
    news_para = news_soup.find_all("div", class_="article_teaser_body")[0].text

    print(news_title)
    print("--------------------------------------------------------------------")
    print(news_para)


    # ### JPL Mars Space Images - Featured Image ###


    image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    time.sleep(10)
    browser.visit(image_url)
    browser.click_link_by_partial_text('FULL IMAGE')


    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    print(html)
    print(image_soup.prettify())


 

    # combine base url with partial url
    # Website Url 
    # image_base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = image_url

    print(url)
    print(featured_image_url)


    # ### Mars Facts ###

    # Scrape table with facts about Mars
    # store full url
    facts_url = 'https://space-facts.com/mars/'
    # read html into df
    table = pd.read_html(facts_url)
    table
    # making the columns
    mars_facts = table[2]
    mars_facts.columns = ["Description", "Value"]
    mars_facts

    # saving as html table format
    mars_html_table = mars_facts.to_html()
    print(mars_html_table)

    mars_html_table = mars_html_table.replace('\n', '')


    # ### Mars Hemispheres ###

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemispheres_url)

    hemispheres_html = browser.html

    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')

    print(hemispheres_soup.prettify())

    hem_img = hemispheres_soup.find_all('div', class_= 'item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Create a For Loop to loop through items stored
    for i in hem_img: 
        # Store title
        title = i.find('h3').text
    
        # Store link that leads to full image website
        part_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + part_img_url)
        
        # HTML Object of individual hemisphere information website 
        part_img_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( part_img_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
        # Show hemisphere_image_urls
        hemisphere_image_urls


    # ### Scrapped Code Dictionary ###


    mars_dict = {
            "news_title": news_title,
            "news_para": news_para,
            "featured_image_url": featured_image_url,
            "fact_table": str(mars_html_table),
            "hemisphere_images": hemisphere_image_urls
        }
    browser.quit()
    print(mars_dict)
    return
init_browser()
scrape()