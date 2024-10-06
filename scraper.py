import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.robotparser as robotparser
import time, random

CATALOGSURL = "https://catalogs.buffalo.edu/content.php?catoid=1&navoid=85&utm_source=academics-areasofstudy-page&utm_medium=redirect&utm_term=2023-10-20"

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

def get_websites(url):
    if is_allowed_to_scrape(url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors

            soup = BeautifulSoup(response.text, 'html.parser')

            # Example: Extract all text from <a> tags with class 'block_content_outer'
            elements = soup.find_all('a')

            with open('sites.txt', 'w') as file:
                # Iterate through the elements and print text with hyperlinks
                for element in elements:
                    href = element.get('href')
                    if href and href.startswith('preview_program.php') and element.text.lower().startswith("computer"):
                        text = f"https://catalogs.buffalo.edu/{href}"
                        file.write(f"{text}\n")

        except requests.exceptions.RequestException as e:
            print(f"Error scraping {url}: {e}")
    else:
        print(f"Scraping not allowed for {url}")

def scrapePerSite(url):
    if is_allowed_to_scrape(url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors

            soup = BeautifulSoup(response.text, 'html.parser')

            # Get major title
            majorTitle = soup.find('h1', id="acalog-content").text
            majorTitle = majorTitle.replace(" ", "-") #replace spaces with dashes so it can be made as a file
            majorTitle = majorTitle.replace("/", "_")

            # Find admission criteria
            admissionCriteria = soup.find('ul')

            # Important classes to take
            #! working on this
            importantClasses = soup.find_all('div', _class="custom_leftpad_20")
            print(importantClasses)
            #courseRequirements = 
            
            with open(f"classes/{majorTitle}.txt", "w") as file:
                file.write("Admission Criteria:")
                
                for requirement in admissionCriteria.children:
                    file.write(requirement.text)

        except requests.exceptions.RequestException as e:
            print(f"Error scraping {url}: {e}")
    else:
        print(f"Scraping not allowed for {url}")

def getDataForEachMajor():
    with open("sites.txt", "r") as file:
        for line in file:
            # Investigates each link
            scrapePerSite(line.strip())

            time.sleep(random.randint(1,3))

            #TODO: scrape from each link to get descriptions of each class and stuff

# Get the list of URLs
get_websites(CATALOGSURL)
getDataForEachMajor()