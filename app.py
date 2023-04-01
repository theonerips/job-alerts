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

# Create a function to scrape Digital Vision job postings
def scrape_jobs():
    # URL of the job postings page
    url = "https://www.digitalvision.com/careers/"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the job listings on the page
    job_listings = soup.find_all('div', {'class': 'job-item'})

    # Loop through each job listing and extract the job title, location, and link
    for job_listing in job_listings:
        job_title = job_listing.find('h3', {'class': 'job-title'}).text.strip()
        job_location = job_listing.find('span', {'class': 'job-location'}).text.strip()
        job_link = job_listing.find('a')['href']
        job_message = f"New job posting on Digital Vision:\n\nTitle: {job_title}\nLocation: {job_location}\nLink: {job_link}"
        
        # Send the job message to the Telegram channel
        bot.send_message(chat_id=channel_name, text=job_message)

        # Add a delay of 1 second between each job notification to avoid spamming the channel
        time.sleep(1)

# Run the scrape_jobs() function
scrape_jobs()
