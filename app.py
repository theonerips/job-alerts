import requests
from bs4 import BeautifulSoup
import os
import time
import telegram

# Set up Telegram bot
bot = telegram.Bot(token=os.environ['TELEGRAM_TOKEN'])
chat_id = os.environ['TELEGRAM_CHAT_ID']

# Set up job posting platforms
urls = [
    'https://www.indeed.com/jobs?q=python&l=',
    'https://www.linkedin.com/jobs/search/?keywords=python&location=',
    'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=python&sc.keyword=python&locT=&locId=&jobType='
]

# Define function to scrape job postings from a URL
def scrape_jobs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    job_listings = soup.find_all('div', class_='jobsearch-SerpJobCard')
    jobs = []
    for job in job_listings:
        title = job.find('a', class_='jobtitle').text.strip()
        company = job.find('span', class_='company').text.strip()
        location = job.find('span', class_='location').text.strip()
        link = 'https://www.indeed.com' + job.find('a')['href']
        jobs.append({
            'title': title,
            'company': company,
            'location': location,
            'link': link
        })
    return jobs

# Scrape job postings from each URL and send them to Telegram channel
while True:
    for url in urls:
        jobs = scrape_jobs(url)
        for job in jobs:
            message = f"{job['title']} at {job['company']} in {job['location']}\n{job['link']}"
            bot.send_message(chat_id=chat_id, text=message)
    time.sleep(86400)  # Wait 24 hours before scraping again
