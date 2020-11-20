import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    
    #NASA Mars News - latest headline with paragraph
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    time.sleep(6.0)
    
    html_news = browser.html
    soupy = bs(html_news, 'lxml')
    
    time.sleep(6.0)
    
    title = soupy.find('div', class_="bottom_gradient").h3.text
    para = soupy.find('div', class_="article_teaser_body").text
    date = soupy.find('div', class_="list_date").text
    
    #JPL Mars Space Images - feature image  
    #set search url
    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # set base feature image url
    base_img_url ='https://www.jpl.nasa.gov/spaceimages/images/largesize/'

    browser.visit(url_img)
    time.sleep(6.0)
    
    html_img = browser.html
    soupimg = bs(html_img, 'lxml')
    
    time.sleep(2.0)
    
    # retrieve current Featured Mars Image
    image_find = soupimg.find('a', class_='button fancybox')['data-fancybox-href']
    image_pg = (f'{url_img}{image_find}')
    
    # get feature id by it's string position and make feature img url
    jpg = 'hires.jpg'
    end=len(image_find)-6
    start1= image_find.find("z")
    start=start1+3
    img_id=image_find[start:end]
    feature_image_url = f'{base_img_url}{img_id}{jpg}'
    
    #visit next page for feature image
    browser.visit(image_pg)
    time.sleep(6.0)
    
    image_name = soupimg.find('a', class_='button fancybox')['data-title']
    image_desc = soupimg.find('a', class_='button fancybox')['data-description']
    
    #Mars Facts - what facts table
    url_facts = 'https://space-facts.com/mars/'
    time.sleep(2.0)
    
    table = pd.read_html(url_facts)
    
    mars_facts_df = table[2]
    mars_facts_df.columns = ["","Mars"]
    mars_facts_df.set_index("Mars", inplace=True)
    
    mars_html_table = mars_facts_df.to_html()

    
    # Mars Hemispheres - image urls with titles:
    url_hem = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #set base url to append hemi image download tif file name to
    base_hemi_url='https://astropedia.astrogeology.usgs.gov/download'
    browser.visit(url_hem)
    
    time.sleep(2.0)

    html_hem = browser.html
    souphem = bs(html_hem, 'lxml')
    
    time.sleep(2.0)
    
    # loop to gather all full res hemisphere img urls
    start_url = 'https://astrogeology.usgs.gov'
    hemisphere_image_urls = []

    # Retrieve the parent divs for all articles
    results_all = souphem.find('div', class_='collapsible results')
    hemispheres = results_all.find_all('div', class_='item')

    # loop over results to get hemi title and img url
    for hemi in hemispheres:
        # scrape the link hemi title
        title_hemi = hemi.find('div', class_='description').h3.text
        # scrape the link to hemi img
        img_url = hemi.find('div', class_='description').a["href"]
        #get end of url for tif download file
        start_hemi = img_url.find("p/")+1
        end_hemi = len(img_url)
        for_tif=img_url[start_hemi:end_hemi]
        img_hemi_url=f'{base_hemi_url}{for_tif}.tif/full.jpg'
    
    time.sleep(20.0)
    
    # make title and img_url into dict and store in list
    hemi_dict = {}
    hemi_dict['title'] = title_hemi
    hemi_dict['img_url'] = img_hemi_url
    
    hemisphere_image_urls.append(hemi_dict)
    time.sleep(15.0)
        
    # Creat a dictionary that holds all the scraped data
    mars_scrpd = {}
    mars_scrpd["news_title"] = title
    mars_scrpd["news_paragraph"] = para
    mars_scrpd["news_date"] = date
    mars_scrpd["feature_image_url"] = feature_image_url
    mars_scrpd["feature_image_name"] = image_name
    mars_scrpd["feature_image_described"] = image_desc
    mars_scrpd["mars_facts"] = mars_html_table
    mars_scrpd["hemisphere_image_urls"] = hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()

    return mars_scrpd



