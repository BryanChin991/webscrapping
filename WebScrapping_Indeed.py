from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time

delays = [7, 4, 6, 2, 10, 19]
delay = np.random.choice(delays)

def UrlParsing(value):
    url = f'https://malaysia.indeed.com/jobs?q=data+scientist&l=Selangor&start={value}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    print(f'url page {value/10} data request status: {data.status_code}\n')

    return soup

def webScrapping(soup):
    jobs_list = []
    for jobs in soup.find_all('div', class_='job_seen_beacon'):
        description_list = []

        for items in jobs.find('h2', class_='jobTitle').find_all('span'):
           if items.string != 'new':
               title = items.string

        company_name = jobs.find('span', class_='companyName').string
        location = jobs.find('div', class_='companyLocation').string

        try:
            salary = jobs.find('span', class_='salary-snippet').string
        except:
            salary = None

        try:
            rating = jobs.find('span', class_='ratingNumber').find('span').text
        except:
            rating=None

        for li in jobs.find('div', class_='job-snippet').find_all('li'):
            description_list.append(li.text)

        # print(title, company_name, location, salary, rating, description_list)
        # print('-'*100)

        jobs_dict = {'Title':title,
                      'Company Name':company_name,
                      'Location':location,
                      'Salary':salary,
                      'Rating': rating,
                      'Descriptions': ' '.join(description_list)}

        jobs_list.append(jobs_dict)
    return jobs_list

all_jobs = pd.DataFrame()
for v in range(80, 100, 10):
    link = UrlParsing(v)
    new_jobs = webScrapping(link)
    all_jobs = all_jobs.append(new_jobs, ignore_index=True)

print(all_jobs.head(), 'total length: ', len(all_jobs))
all_jobs.to_csv('jobs_list_004.csv', index=False)
