import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import Counter
import re
import os

# This is only used for the home page

def get_top_keywords(url, top_n=10):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Get text from specific tags
    text_list = []
    title = soup.find('title')
    if title:
        text_list.append(title.get_text())
    h1_tags = soup.find_all('h1')
    h2_tags = soup.find_all('h2')
    description = soup.find('meta', attrs={'name': 'description'})
    
    for h1 in h1_tags:
        text_list.append(h1.get_text())
    for h2 in h2_tags:
        text_list.append(h2.get_text())
    if description:
        text_list.append(description.get('content', ''))
    
    # Tokenize the text content and convert to lowercase
    all_text = ' '.join(text_list).lower()
    words = re.findall(r'\w+', all_text)
    
    # Create phrases of length 2 to 10
    phrases = []
    for length in range(2, 11):
        phrases += [' '.join(words[i:i+length]) for i in range(len(words)-length+1)]
    
    # Count occurrences of these phrases
    counter = Counter(phrases)

    # Extract domain-related words from the URL
    parsed_url = urlparse(url)
    domain_related_words = re.findall(r'\w+', parsed_url.netloc + parsed_url.path)
    
    # Filter out phrases with more than 10 words and phrases containing words related to the URL
    cleaned_phrases = [(phrase, count) for phrase, count in counter.most_common() if (all(domain_word not in phrase for domain_word in domain_related_words) and len(phrase.split()) <= 10)]
    
    return cleaned_phrases[:top_n]

if __name__ == "__main__":
    # Get the URL input from the user
    url = input("Enter the URL to analyze: ")
    
    # Call the function and get the top keywords
    top_keywords = get_top_keywords(url)
    
    if top_keywords:
        print(f"Top Keywords for {url}:")
        for keyword, count in top_keywords:
            print(f"{keyword}: {count}")
    else:
        print("No top keywords found.")
