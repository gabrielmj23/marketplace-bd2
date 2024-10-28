import requests
from bs4 import BeautifulSoup
import pandas as pd

MERCADO_LIBRE_BASE_URL = "https://listado.mercadolibre.com.ve/computacion/pc-de-escritorio/computadoras/pc-de-escritorio"
MERCADO_LIBRE_URL_SUFFIX = "_NoIndex_True"
MAX_PRODUCTS = 48
#MAX_PRODUCTS = 10000

def scrape_single(product_url: str):
    """
    Scrapes single product data from Mercado Libre product detail
    """
    
    print(f"\nScraping single {product_url}")
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        seller_reputation = soup.find('ul', class_="ui-thermometer")["value"]
    except:
        seller_reputation = "none"

    return {
        "seller_reputation": seller_reputation
    }


def scrape_data():
    """
    Scrapes computer data from Mercado Libre listing
    """
    
    # Generate array of listing URLs to explore
    urls = [ MERCADO_LIBRE_BASE_URL + MERCADO_LIBRE_URL_SUFFIX ]
    page_number = 49
    for i in range(0, MAX_PRODUCTS, 49):
        urls.append(f"{MERCADO_LIBRE_BASE_URL}_Desde_{page_number}{MERCADO_LIBRE_URL_SUFFIX}")
        page_number += 48

    data = []
        
    # Iterate over each url
    has_printed_done = False
    for i, url in enumerate(urls):

        # Get the html of the page
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
            
        # Get all product items
        content = soup.find_all('li', class_='ui-search-layout__item')
        
        # Check if there's no content to scrape
        if not content:
            print("\nDone scraping")
            has_printed_done = True
            break

        print(f"\nScraping page {i + 1} with url: {url}")
        
        for post in content:
            # Extract basic data from card
            title = post.find('h2').text

            price = post.find('div', class_='poly-price__current').find('span', class_='andes-money-amount__fraction').text
            
            try:
                price_cents = post.find('div', class_='poly-price__current').find('span', class_='andes-money-amount__cents').text
            except:
                price_cents = "00"

            try:
                post_rating = post.find('span', class_='poly-reviews__rating').text
            except:
                post_rating = "none"

            post_url = post.find("a")["href"]

            try:
                img_url = post.find("img")["data-src"]
            except:
                img_url = post.find("img")["src"]

            # Extract specific data from product page
            inner_data = scrape_single(post_url)
            
            # Save in dictionary
            post_data = {
                "title": title,
                "price": f"{price}.{price_cents}",
                "rating": post_rating,
                "post_url": post_url,
                "img_url": img_url            
            }
            post_data.update(inner_data)
            
            data.append(post_data)
        
    if not has_printed_done:
        print("\nDone scraping")

    export_to_csv(data)

def export_to_csv(data):
    """
    Exports list of products to a csv
    """
    
    df = pd.DataFrame(data)
    df.to_csv(r"data/mercado_libre.csv")
    print("\nDone exporting")

if __name__ == "__main__":
    scrape_data()
