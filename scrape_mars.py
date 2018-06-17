import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver


# Initialize browser
def init_browser():
    executable_path = {"executable_path": "C:\Program Files (x86)\Chromedriver\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


# Function to scrape our mars data
def scrape_info():
    browser = init_browser()

    # declare a URL variable to visit the nasa news page and visit that URL.  Pause for 2 seconds to allow the page to fully load.
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(2)

    #Scrape the data into BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Find the title and text for the most recent article
    title = soup.find(class_='content_title')
    text = soup.find(class_='rollover_description_inner')
    news_title = title.text
    news_text = text.text
    print(news_title)
    print(news_text)

    # Visit the following URL, scrape the data into BS to be discected.  
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    browser.visit(url)

    # Declare a partial URL to be used later
    beginning_url = 'https://www.jpl.nasa.gov'

    # Design an XPATH selector to grab the featured image from the page
    xpath = '//a[@class="button fancybox"]'
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()

    # Scrape the browser into soup and use soup to find the full resolution image of mars
    # Save the image url to a variable called `img_url`
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_url = soup.find("img", class_="fancybox-image")["src"]

    # Use the partial URL from earlier to combine it with the other partial URL.  
    featured_image_url = beginning_url + img_url

    # Declare our new URL as twitter, visit the page, and scrape the data into BS.
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the most recent tweet and store it in a variable
    tweet = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather = tweet.text
    
    #Declare another new URL for mars facts and read the tables on the page using pandas.
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    
    # Store the data in a dataframe for later
    facts_df = tables[0]
    facts_df.columns = ["Classification", "Fact"]
    facts_df.set_index('Classification', inplace=True)
    facts_df.to_html('table.html')
    facts_df

    # Declare another URL to get enhanced images of the 4 hemispheres of mars.  Scrape the data into BS to get links to the enhanced images.
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    base_url = "https://astrogeology.usgs.gov"

    # Locate the individual URL for each hemisphere and store them in the img_url list to be iterated through.
    hemispheres = soup.find_all("div", class_="item")
    img_url = []
    for h in hemispheres:
        img_url.append(h.a["href"])
    
    # loop through the img_url list, go to each link, scrape the data into soup, and locate the title and hyperlink for each 
    # enhanced image.  Then store the information as a dictionary.

    hemisphere_image_urls = []

    for hemi in img_url:
        url = base_url + hemi
        browser.visit(url)
        time.sleep(2)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all(class_="downloads")
        link = links[0].ul
        interum_links = []
        header = soup.find(class_="title")
        hemi_title = header.text
        print(hemi_title)
        for x in link:
            interum_links.append(x)
        full_link = interum_links[1].a["href"]
        print(full_link)
        print("-"*40)
        hemisphere_image_urls.append({"title": hemi_title, "img_url": full_link})
    
    # store it all in a dictionary
    combined = {"news_title": news_title,
                      "news_text": news_text,
                      "featured_image_url": featured_image_url,
                      "mars_weather": mars_weather,
                      "hemisphere_image_urls": hemisphere_image_urls,
                      "facts_df": facts_df}
    
    return combined