"""
import requests
from bs4 import BeautifulSoup

#import requests
#from bs4 import BeautifulSoup

url = "https://www.bbc.com/news"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

# Target all <span> tags with class gs-c-promo-heading__title
headlines = soup.find_all("span", class_="sc-9d830f2a-3 eHyegN")

print("Top Headlines:")
for h in headlines[:10]:  # show first 10
    print("-", h.get_text(strip=True))
"""

import requests
from bs4 import BeautifulSoup

url = "https://www.bbc.com/news"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

# Find all <h2> tags with data-testid="card-headline"
headlines = soup.find_all("h2", {"data-testid": "card-headline"})

print("Top Headlines:")
for h in headlines[:10]:  # first 10 headlines
    print("-", h.get_text(strip=True))



import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def scrape_bbc_headlines():
    url = "https://www.bbc.com/news"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch the page:", response.status_code)
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <h2> tags with data-testid="card-headline"
    headlines = soup.find_all("h2", {"data-testid": "card-headline"})

    # Prepare CSV file
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"bbc_headlines_{date_str}.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Headline"])  # Header row

        for h in headlines:
            writer.writerow([h.get_text(strip=True)])

    print(f"Saved {len(headlines)} headlines to {filename}")

# Run the scraper
scrape_bbc_headlines()




import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

def scrape_bbc_headlines():
    url = "https://www.bbc.com/news"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch the page:", response.status_code)
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <h2> tags with data-testid="card-headline"
    headlines = soup.find_all("h2", {"data-testid": "card-headline"})

    if not headlines:
        print("No headlines found.")
        return

    # CSV file path
    filename = "bbc_headlines_log.csv"

    # Check if file exists
    file_exists = os.path.isfile(filename)

    # Open CSV in append mode
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Write header only if file is new
        if not file_exists:
            writer.writerow(["Date", "Headline"])
        
        # Add headlines with current date
        today = datetime.now().strftime("%Y-%m-%d")
        for h in headlines:
            writer.writerow([today, h.get_text(strip=True)])

    print(f"Appended {len(headlines)} headlines to {filename}")

# Run the scraper
scrape_bbc_headlines()
