import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse, urljoin

# -------------------------------
# Helper function to clean subcategory names
def clean_subcategory_name(url):
    path_parts = urlparse(url).path.strip('/').split('/')
    raw_name = path_parts[-1]
    clean_name = raw_name.replace('-', ' ').title()
    return clean_name
# -------------------------------

# List of subcategory URLs
urls = [
    'https://hotpoint.co.ke/catalogue/category/fridges-freezers/fridges/4-door/',
    'https://hotpoint.co.ke/catalogue/category/fridges-freezers/fridges/instaview/',
    'https://hotpoint.co.ke/catalogue/category/fridges-freezers/fridges/mini/',
    'https://hotpoint.co.ke/catalogue/category/fridges-freezers/fridges/single-door/',
    'https://hotpoint.co.ke/catalogue/category/fridges-freezers/fridges/double-door/',
    'https://hotpoint.co.ke/catalogue/category/fridges-freezers/fridges/combination/',
    'https://hotpoint.co.ke/catalogue/category/fridges-freezers/fridges/upright/',
    'https://hotpoint.co.ke/catalogue/category/fridges-freezers/fridges/side-by-side/'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

csv_file = 'hotpoint_all_fridges.csv'

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Subcategory', 'Product Name', 'Current Price', 'Original Price', 'Product URL', 'Image URL'])

    for url in urls:
        print(f"Scraping subcategory: {url}")
        page_number = 1
        while True:
            paged_url = url
            if page_number > 1:
                if '?' in url:
                    paged_url = f"{url}&page={page_number}"
                else:
                    paged_url = f"{url}?page={page_number}"

            response = requests.get(paged_url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch page {page_number}: {paged_url} ({response.status_code})")
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.find_all('div', class_='card-body product-card-body')

            if not products:
                break

            subcategory_name = clean_subcategory_name(url)

            for prod in products:
                # Product Name
                name_tag = prod.find('h5', class_='card-title product-card-name')
                name = name_tag.text.strip().replace('\n', ' ') if name_tag else "N/A"

                # Prices
                current_tag = prod.find('span', class_='stockrecord-price-current')
                current_price = current_tag.text.strip().replace('\n', ' ') if current_tag else "N/A"

                old_tag = prod.find('span', class_='stockrecord-price-old')
                old_price = old_tag.text.strip().replace('\n', ' ') if old_tag else "N/A"

                # Product URL
                parent_a = prod.find_parent('a', href=True)
                product_url = urljoin('https://hotpoint.co.ke', parent_a['href']) if parent_a else "N/A"

                # Image URL
                img_tag = prod.find('img', class_='product-card-img')
                image_url = urljoin('https://hotpoint.co.ke', img_tag['src']) if img_tag else "N/A"

                writer.writerow([subcategory_name, str(name), str(current_price), str(old_price), product_url, image_url])

            print(f"  Finished page {page_number} for subcategory {subcategory_name}")
            page_number += 1

print(f"Scraping complete. Data saved to {csv_file}")
