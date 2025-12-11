import requests
from bs4 import BeautifulSoup

url = "https://wwww.iamnandaha.co.ke"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# Find all <h2> tags with data-testid="card-headline"
headlines = soup.find_all("h2", {"data-testid": "card-headline"})

#Different websites will have different header formatting

print('Top Headlines: ')
for h in headlines[:10]:
    print('->', h.get_text(strip=True))







#SCRAPE BBC HEADLINES AND SAVE THEM TO A FILE

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
def scrap_bbc_headlines():
    

    url = 'https://linkedin.com'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    if response.status_code !=200:
        print(f'Failed to load page: {response.status_code}')
        return
    headlines = soup.find_all('h2', {"data-testid": "card-headline"})

    #prepare csv file to store the headlines
    #date_str = datetime.now().strftime("%Y-%m-%d")
    #the below returns the current time and date and formats the string
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f'bbc_headlines_{date_str}.csv'

    with open(filename, mode='w', newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Headline'])

        for h in headlines:
            writer.writerow(h.get_text(strip=True))

    print(f'Saved {len(headlines)} headlines to {filename}')

scrap_bbc_headlines()





