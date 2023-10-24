import requests
from bs4 import BeautifulSoup

def detect_social_media_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        social_media_info = {
            "has_facebook": any('facebook.com' in link['href'] for link in soup.find_all('a', href=True)),
            "has_twitter": any('twitter.com' in link['href'] for link in soup.find_all('a', href=True)),
            "has_linkedIn": any('linkedin.com' in link['href'] for link in soup.find_all('a', href=True)),
            "has_instagram": any('instagram.com' in link['href'] for link in soup.find_all('a', href=True)),
            "has_youtube": any('youtube.com' in link['href'] for link in soup.find_all('a', href=True)),
        }

        return social_media_info

    except requests.RequestException as e:
        return {"error": f"Error fetching URL {url}. Reason: {str(e)}"}

if __name__ == "__main__":
    # Get the URL input from the user
    url = input("Enter the URL to check for social media accounts: ")

    social_media_info = detect_social_media_links(url)

    if "error" in social_media_info:
        print(social_media_info["error"])
    else:
        print("Social Media Information for", url)
        print("Facebook:", social_media_info["has_facebook"])
        print("Twitter:", social_media_info["has_twitter"])
        print("LinkedIn:", social_media_info["has_linkedIn"])
        print("Instagram:", social_media_info["has_instagram"])
        print("YouTube:", social_media_info["has_youtube"])