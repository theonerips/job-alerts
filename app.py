import requests
from bs4 import BeautifulSoup
import time
import os
import telegram

# Set your Telegram bot token and channel name here
telegram_bot_token = "5279527836:AAEmhztDGSbznzvuOVmezu5qHRy55haUvKs"
channel_name = "@jobnotifications012"

# Initialize the Telegram bot
bot = telegram.Bot(token=telegram_bot_token)

# Create a function to scrape job postings
def scrape_jobs():
    # URL of the job postings page(s)
    urls = [
        "https://www.indeed.com/q-data-scientist-jobs.html",
        "https://www.linkedin.com/jobs/search/?keywords=python%20developer",
        "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBox&typedKeyword=data+scientist&sc.keyword=data+scientist&locT=C&locId=1147436&jobType=",
    ]

    # Loop through each URL
    for url in urls:
        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the job listings on the page
        if "indeed" in url:
            job_listings = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})
        elif "linkedin" in url:
            job_listings = soup.find_all('li', {'class': 'jobs-search__result-item'})
        elif "glassdoor" in url:
            job_listings = soup.find_all('li', {'class': 'react-job-listing'})

        # Loop through each job listing and extract the job title, company, location, and link
        for job_listing in job_listings:
            if "indeed" in url:
                job_title = job_listing.find('a', {'class': 'jobtitle'}).text.strip()
                job_company = job_listing.find('span', {'class': 'company'}).text.strip()
                job_location = job_listing.find('div', {'class': 'location'}).text.strip()
                job_link = "https://www.indeed.com" + job_listing.find('a')['href']
            elif "linkedin" in url:
                job_title = job_listing.find('h3', {'class': 'job-result-card__title'}).text.strip()
                job_company = job_listing.find('h4', {'class': 'job-result-card__subtitle'}).text.strip()
                job_location = job_listing.find('span', {'class': 'job-result-card__location'}).text.strip()
                job_link = job_listing.find('a')['href']
            elif "glassdoor" in url:
                job_title = job_listing.find('a', {'class': 'jobLink'}).text.strip()
                job_company = job_listing.find('div', {'class': 'jobHeader'}).find('span').text.strip()
                job_location = job_listing.find('span', {'class': 'jobLocation'}).text.strip()
                job_link = "https://www.glassdoor.com" + job_listing.find('a')['href']

            job_message = f"New job posting:\n\nTitle: {job_title}\nCompany: {job_company}\nLocation: {job_location}\nLink: {job_link}"
            
            # Send the job message to the Telegram channel
            bot.send_message(chat_id=channel_name, text=job_message)

            # Add a delay of 1 second between each job notification to avoid spamming the channel
            time.sleep(1)

# Run the scrape_jobs() function
scrape_jobs()
