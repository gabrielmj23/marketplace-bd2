import requests
from bs4 import BeautifulSoup
import csv
from Product import Product

MERCADO_LIBRE_BASE_URL = "https://listado.mercadolibre.com.ve/computacion/pc-de-escritorio/computadoras/pc-de-escritorio"
MERCADO_LIBRE_URL_SUFFIX = "_NoIndex_True"
MERCADO_LIBRE_OUTPUT_FILE = r"data/mercado_libre.csv"
MAX_PRODUCTS = 48
#MAX_PRODUCTS = 10000

def scrape_single(product_url: str):
    """
    Scrapes single product data from Mercado Libre product detail
    """
    
    print(f"\nScraping single {product_url}")
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    inner_data = {
        "seller_reputation": "none",
        "brand": "none",
        "cpu": "none",
        "disk": "none",
        "ram": "none",
    }

    # Extract seller reputation
    try:
        inner_data["seller_reputation"] = soup.find('ul', class_="ui-thermometer")["value"]
    except:
        inner_data["seller_reputation"] = "none"

    # Extract table features
    try:
        rows = soup.find_all("tr", class_="andes-table__row")

        for row in rows:
            try:
                key = row.find("div", class_="andes-table__header__container").text
                value = str(row.find("span", class_="andes-table__column--value").text).strip()
            except:
                continue

            if key == "Marca":
                inner_data["brand"] = value
            elif key == "Tipo de procesador":
                inner_data["cpu"] = value
            elif key == "Tamaño del disco duro":
                inner_data["disk"] = value
            elif key == "RAM":
                inner_data["ram"] = value
    except:
        pass

    return inner_data


def scrape_data(should_rewrite: str):
    """
    Scrapes computer data from Mercado Libre listing
    """
    
    # Generate array of listing URLs to explore
    urls = [ MERCADO_LIBRE_BASE_URL + MERCADO_LIBRE_URL_SUFFIX ]
    page_number = 49
    for i in range(0, MAX_PRODUCTS, 49):
        urls.append(f"{MERCADO_LIBRE_BASE_URL}_Desde_{page_number}{MERCADO_LIBRE_URL_SUFFIX}")
        page_number += 48

    # Set up read file
    bool_should_rewrite = should_rewrite == "s"
    if not bool_should_rewrite:
        csv_read_file = open(MERCADO_LIBRE_OUTPUT_FILE, "r")
        reader = csv.DictReader(csv_read_file)
        next(reader)
        existing_lines = list(reader)
    else:
        existing_lines = []
    
    # Set up write mode
    write_mode = "w" if bool_should_rewrite else "a"

    # Set up output file
    with open(MERCADO_LIBRE_OUTPUT_FILE, write_mode, newline='') as csv_write_file:
        writer = csv.DictWriter(csv_write_file, fieldnames=Product.FIELD_NAMES)
        if write_mode == "w":
            writer.writeheader()
        bool_should_rewrite = should_rewrite == "s"
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
                # Extract product URL to check if is included in file
                post_url = post.find("a")["href"]

                is_included = False
                for line in existing_lines:
                    if post_url == line["post_url"]:
                        is_included = True
                        break
                
                if is_included and not bool_should_rewrite:
                    continue

                # Extract basic data from card
                title = post.find('h2').text

                # Skip products with "servidor" or "Servidor" in the title
                if "servidor" in title.lower():
                    continue

        
                if post.find('div', class_='poly-component__shipping'):
                    shipping = True
                else:
                    shipping = False

                price = post.find('div', class_='poly-price__current').find('span', class_='andes-money-amount__fraction').text
                
                try:
                    price_cents = post.find('div', class_='poly-price__current').find('span', class_='andes-money-amount__cents').text
                except:
                    price_cents = "00"

                try:
                    post_rating = post.find('span', class_='poly-reviews__rating').text
                except:
                    post_rating = "none"
                
                try:
                    img_url = post.find("img")["data-src"]
                except:
                    img_url = post.find("img")["src"]

                

                # Extract specific data from product page
                inner_data = scrape_single(post_url)
                
                # Create instance
                product = Product(
                    title,
                    f"{price}.{price_cents}",
                    post_rating,
                    inner_data["seller_reputation"],
                    inner_data["brand"],
                    inner_data["cpu"],
                    inner_data["disk"],
                    inner_data["ram"],
                    post_url,
                    img_url,
                    shipping
                )

                # Add to csv
                writer.writerow(product.to_dict())

        if not has_printed_done:
            print("\nDone scraping")

if __name__ == "__main__":
    should_rewrite = input("Reescribir csv? s/n: ")
    scrape_data(should_rewrite)
