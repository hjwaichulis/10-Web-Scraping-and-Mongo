from splinter import Browser
from bs4 import BeautifulSoup as bs
import os
import pandas as pd
import time
import requests
from urllib.parse import urlsplit

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_data = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    # mars_data["news_title"] = soup.find("div", class_="content-title").text()
    # mars_data["news_p"] = soup.find("div", class_="article_teaser_body").text()
    news_title = soup.find("div", class_="content-title")
    news_p = soup.find("div", class_="article_teaser_body").text
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p
    # Images
    image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image)


    # image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # browser.visit(image)
    # url = "{0.scheme}://{0.netloc}/".format(urlsplit(image))
    # xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"
    # results = browser.find_by_xpath(xpath)
    # img = results[0]
    # img.click()
    # html_image = browser.html
    # soup = bs(html_image, "html.parser")
    # img_url = soup.find("img", class_="fancybox-image")["src"]
    full_url = "https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA23384_hires.jpg" 

    mars_data["featured_image_url"] = full_url 
    # Weather
    url_mars_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_mars_weather)
    html_mars_weather = browser.html
    soup = bs(html_mars_weather, "html.parser")

    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_data["mars_weather"] = mars_weather
    # Mars Facts
    url_mars_facts = "https://space-facts.com/mars/"
    mars1 = pd.read_html(url_mars_facts)
    mars1 = pd.read_html(url_mars_facts)
    mars_df = mars1[1]
    mars_df.columns = ["Parameter", "Values"]
    mars_df.set_index(["Parameter"])
    mars_html = mars_df.replace("\n", "")
    mars_html = mars_df.to_html()
    mars_data["fact_table"] = mars_html

    # Hemispheres
    hemisphere_image_urls = []

    ##Valles
    valles_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced')
    response = requests.get(valles_url)
    soup = bs(response.text, 'html.parser')
    valles_marineris_img = soup.find_all('div', class_="wide-image-wrapper")
    for img in valles_marineris_img:
        img = img.find('li')
        full_image = img.find('a')['href']
        valles_marineris_title = soup.find('h2', class_='title').text
        valles_marineris_hemisphere = {"Title": valles_marineris_title, "url": full_image}
        hemisphere_image_urls.append(valles_marineris_hemisphere)
    ##Cerberus
    cerberus_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced')
    response = requests.get(cerberus_url)
    soup = bs(response.text, 'html.parser')
    cerberus_img = soup.find_all('div', class_="wide-image-wrapper")
    for img in cerberus_img:
        img = img.find('li')
        full_image = img.find('a')['href']
        cerberus_title = soup.find('h2', class_='title').text
        cerberus_hemisphere = {"Title": cerberus_title, "url": full_image}
        hemisphere_image_urls.append(cerberus_hemisphere)
    ##Schiaparelli
    schiaparelli_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced')
    response = requests.get(schiaparelli_url)
    soup = bs(response.text, 'html.parser')
    schiaparelli_img = soup.find_all('div', class_="wide-image-wrapper")
    for img in schiaparelli_img:
        img = img.find('li')
        full_image = img.find('a')['href']
        schiaparelli_title = soup.find('h2', class_='title').text
        schiaparelli_hemisphere = {"Title": schiaparelli_title, "url": full_image}
        hemisphere_image_urls.append(schiaparelli_hemisphere)
    ##Syrtis
    syrtis_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced')
    response = requests.get(syrtis_url)
    soup = bs(response.text, 'html.parser')
    syrtis_img = soup.find_all('div', class_="wide-image-wrapper")
    for img in syrtis_img:
        img = img.find('li')
        full_image = img.find('a')['href']
        syrtis_title = soup.find('h2', class_='title').text
        syrtis_hemisphere = {"Title": syrtis_title, "url": full_image}
        hemisphere_image_urls.append(syrtis_hemisphere)
    mars_data["hemisphere_image"] = hemisphere_image_urls



    return mars_data
