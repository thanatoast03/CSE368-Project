import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.robotparser as robotparser
import time, random

def is_allowed_to_scrape(url, user_agent='*'):
    # Parse the domain to get the base URL for robots.txt
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

    # Create a RobotFileParser object
    rp = robotparser.RobotFileParser()
    rp.set_url(base_url)
    rp.read()  # Read the robots.txt

    # Check if the URL is allowed
    return rp.can_fetch(user_agent, url)

def scrape_website(url):
    if is_allowed_to_scrape(url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors

            soup = BeautifulSoup(response.text, 'html.parser')

            # Example: Extract all text from <a> tags with class 'block_content_outer'
            elements = soup.find_all('a')

            with open('sitesToParse.txt', 'w') as file:
                # Iterate through the elements and print text with hyperlinks
                for element in elements:
                    href = element.get('href')
                    if href and href.startswith('preview_program.php'):
                        text = f"https://catalogs.buffalo.edu/{href}"
                        file.write(f"{text}\n")

        except requests.exceptions.RequestException as e:
            print(f"Error scraping {url}: {e}")
    else:
        print(f"Scraping not allowed for {url}")

# List of websites to scrape
urls = [
    "https://catalogs.buffalo.edu/content.php?catoid=1&navoid=85&utm_source=academics-areasofstudy-page&utm_medium=redirect&utm_term=2023-10-20"
]

# Loop through the list of URLs
for url in urls:
    scrape_website(url)

    #! UB please don't kick me out
    # Fixed delay
    time.sleep(1)  # Wait for 1 second between requests

    # Randomized delay (between 1 and 3 seconds)
    time.sleep(random.uniform(1, 3))
