import requests
from bs4 import BeautifulSoup

def find_links_with_text(url, search_text):
    try:
        # Make a request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all anchor tags
        links = soup.find_all('a')

        # Filter those that contain the search text
        relevant_links = [link['href'] for link in links if link.string and search_text.lower() in link.string.lower()]

        return relevant_links

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    target_url = input("Enter the URL to scrape: ")
    links = find_links_with_text(target_url, "write for us")

    if links:
        print("\nFound the following links with the words 'write for us':")
        for link in links:
            print(link)
    else:
        print("\nNo links found with the words 'write for us'.")

