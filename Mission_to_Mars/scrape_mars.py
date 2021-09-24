
#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import requests
import pandas as pd

#Splinter Setup

def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

#for scrape_mars and MongoDB scrape

    mars_data={}

    #URL of website to scrape
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    soup = bs(browser.html, 'lxml')

    time.sleep(2)


    #Create BeautifulSoup Object
    mars_html = browser.html
    mars_soup = bs(mars_html, "html.parser")


    #View html content from page
    results = mars_soup.find('div', class_='list_text')
    print(results)

    #Scrape the Mars News Site and collect the latest News Title and Paragraph Text.
    news_title = results.find('div', class_='content_title')
    news_title= news_title.text.strip()

    print(f'News Title: {news_title}')

    #Scrape the Mars News Site and collect the latest News Title and Paragraph Text.
    news_p = results.find('div', class_='article_teaser_body')
    news_p = news_p.text.strip()

    print(f'Paragraph Text: {news_p}')

    #URL of website to scrape
    featured_im_url = "https://spaceimages-mars.com/"
    browser.visit(featured_im_url)

    time.sleep(2)

    #Create BeautifulSoup Object
    html = browser.html
    image_soup = bs(html, "html.parser")

    #View html content from page and find featured image
    featured_image_url = image_soup.find_all('img')[1]['src']
    featured_image_url = featured_im_url + featured_image_url
    print(f'Featured Image: {featured_image_url}')

    #URL of website to scrape
    facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(facts_url)

    time.sleep(2)

    #use read html function to scrape data from page using pandas
    tables = pd.read_html(facts_url)
    tables

    df = tables[1]
    df.columns=['Description', 'Value']

    df.head(9)

    df_html=df.to_html()
    print(df_html)


    #URL of website to scrape
    hemisphere_url = "https://marshemispheres.com/"
    browser.visit(hemisphere_url)
    time.sleep(2)

    #Create BeautifulSoup Object
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, "html.parser")

    #list to store items image header and image
    hemis_list=[]

    #find html items
    hemisphere_view=hemisphere_soup.find('div', class_='collapsible results')
    image_select=hemisphere_view.find_all('div',class_='item')


    #loop through to gather items into dict. 
    for x in image_select:
        hemisphere = x.find('div', class_="description")
        title = hemisphere.h3.text
    
        hemi_link = hemisphere.a["href"]
        browser.visit(hemisphere_url + hemi_link)
    
        pic_html = browser.html
        pic_soup = bs(pic_html, 'html.parser')
    
        pic_url = pic_soup.find('li').a['href']

    #Dictionary creation
    hemis_dict={'title': title,'img_url': hemisphere_url+pic_url}
    
    #append to add urls    
    hemis_list.append(hemis_dict)

    print(hemis_list)

    browser.quit()

    return scrape

if __name__ == "__main__":
    scrape_info = scrape()
    print(scrape_info)

