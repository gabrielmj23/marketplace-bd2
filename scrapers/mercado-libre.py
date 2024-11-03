from bs4 import BeautifulSoup
import csv
import re
from Product import Product
from Browser import Browser

MERCADO_LIBRE_BASE_URL = "https://listado.mercadolibre.com.ve/computacion/pc-de-escritorio/computadoras/pc-de-escritorio"
MERCADO_LIBRE_URL_SUFFIX = "_NoIndex_True"
MERCADO_LIBRE_OUTPUT_FILE = r"data/mercado_libre.csv"
# MAX_PRODUCTS = 48
MAX_PRODUCTS = 100000

browser = None

def scrape_single(product_url: str, title: str):
    """
    Scrapes single product data from Mercado Libre product detail
    """
    
    print(f"\nScraping single {product_url}")
    text = browser.get_response_text(product_url)
    soup = BeautifulSoup(text, 'html.parser')

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
        rows = soup.select("tr.andes-table__row.ui-vpp-striped-specs__row")

        for row in rows:
            try:
                key = row.select_one("div.andes-table__header__container").text
                value = row.select_one("span.andes-table__column--value").text
            except:
                continue

            if key == "Marca":
                inner_data["brand"] = value
            elif key == "Tipo de procesador":
                inner_data["cpu"] = value
            elif key == "Tamaño del disco duro":
                inner_data["disk"] = value.replace(" ", "")
            elif key == "RAM":
                inner_data["ram"] = value.replace(" ", "")

        # Attempt to get values from title
        if inner_data["brand"] == "none":
            # Find first brand in title
            for brand in Product.COMMON_BRANDS:
                if brand.lower() in title.lower():
                    inner_data["brand"] = brand
                    break

        if inner_data["disk"] == "none":
            # Find segment of title that is made of 3 digits followed by GB, or 1 digit followed by TB
            match = re.search(r'\b(\d{3}\s?GB|\d\s?TB)\b', title.upper())
            if match:
                inner_data["disk"] = match.group(0).replace(" ", "")

        if inner_data["ram"] == "none":
            # Similar logic to disk
            match = re.search(r'\b(\d{2}\s?GB|\d\s?GB)\b', title.upper())
            if match:
                inner_data["ram"] = match.group(0).replace(" ", "")
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

        for i, url in enumerate(urls):
            # Get the html of the page
            text = browser.get_response_text(url)
            soup = BeautifulSoup(text, 'html.parser')
            
            # Get all product items
            content = soup.find_all('li', class_='ui-search-layout__item')
            
            # Check if there's no content to scrape
            if not content:
                print(f"No content: {url}")
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
                    print(f"{post_url} is included")
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
                inner_data = scrape_single(post_url, title)
                
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

        print("\nDone scraping")

if __name__ == "__main__":
    should_rewrite = input("Reescribir csv? s/n: ")

    print("=== INICIO DE SESIÓN")
    email = input("Ingrese su correo de inicio en MercadoLibre: ")
    browser = Browser(email)

    scrape_data(should_rewrite)
