import requests
from bs4 import BeautifulSoup
import re
import argparse

visited = set()  # Keep track of visited URLs

def extract_emails_from_url(url):
    # If the URL was visited, return immediately
    if url in visited:
        return

    visited.add(url)

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        content = response.text

        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()

        # Regular expression to match email addresses
        email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
        emails = set(re.findall(email_regex, text))

        for email in emails:
            print(f"Email: {email} | URL: {url}")

        # Extract and follow internal links
        for link in soup.find_all('a', href=True):
            if link['href'].startswith('/') or url in link['href']:
                # Construct full URL if it's a relative link
                next_url = link['href'] if link['href'].startswith('http') else url + link['href']
                extract_emails_from_url(next_url)

    except requests.RequestException as e:
        print(f"Error fetching URL {url}. Reason: {e}")

if __name__ == "__main__":
    # Get the URL input from the user
    url = input("Enter the URL to scrape for email addresses: ")
    extract_emails_from_url(url)
