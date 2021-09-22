import requests
from bs4 import BeautifulSoup
import pandas as pd

def WebScrape(value):
    url = f'https://www.airbnb.com/s/Kuala-Lumpur-Malaysia/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=november&flexible_trip_dates%5B%5D=october&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&place_id=ChIJ0-cIvSo2zDERmWzYQPUfLiM&federated_search_session_id=1d3ecc1b-6b72-4615-9d78-c2e7fcd1c8a9&pagination_search=true&items_offset={value}&section_offset=3'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52'}
    r = requests.get(url, headers)
    print(f'Request {value} status code', r.status_code, '\n')
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

web = WebScrape(10)
for hotel in web.find_all('div', class_='_fhph4u'):
    all_list = []
    for info in hotel.find_all('div', class_='_gig1e7'):
        data = {}
        descriptions = []

        try:
            title = info.find('div', class_='_1xzimiid').text
        except:
            title = ''

        try:
            subtitle = info.find('span', class_='_1whrsux9').text
        except:
            subtitle = ''

        for details in info.find_all('div', class_='_3c0zz1'):
            for d in details.find_all('span', class_='_3hmsj'):
                descriptions.append(d.text)

        try:
            rating = info.find('span', class_='_10fy1f8').text
        except:
            rating = ''

        try:
            price = info.find('span', class_='_krjbj').text
        except:
            price = ''

        data = {
            'Room type': title,
            'Name': subtitle,
            'Descriptions': ', '.join(descriptions),
            'Rating': rating,
            'Price': price
        }
        all_list.append(data)

df = pd.DataFrame()
# print(all_list)
df = df.append(all_list, ignore_index=True)
print(df)
df.to_csv('Abnb_listings_1.csv', index=False)