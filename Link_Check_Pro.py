import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys
import os

def get_links(url):
    """Fetch all links from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.RequestException as e:
        print(f"Failed to retrieve the page: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    full_links = [urljoin(url, link) for link in links]
    return full_links

def check_link_status(url):
    """Check the HTTP status of the given URL."""
    try:
        response = requests.get(url)
        return response.status_code
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")
        return None

def process_url(url, available_file, unavailable_file):
    """Process a single URL: get links and check their status."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    print(f"\nProcessing {url}")
    domain = urlparse(url).netloc.split('.')[0]  # Extract domain name
    print("Links to check:")
    links = get_links(url)
    for link in links:
        print(link)
        status = check_link_status(link)
        if status == 200:
            available_file.write(f"{link} (status 200)\n")
        else:
            unavailable_file.write(f"{link} (status {status})\n")

def main():
    if len(sys.argv) != 2 and (len(sys.argv) != 3 or sys.argv[1] != '-f'):
        print("Usage: python check_links.py <website_url> or python check_links.py -f <file_with_urls>")
        return

    with open('available_links.txt', 'w') as available_file, open('unavailable_links.txt', 'w') as unavailable_file:
        if sys.argv[1] == '-f':
            file_path = sys.argv[2]
            if not os.path.isfile(file_path):
                print(f"File not found: {file_path}")
                return

            with open(file_path, 'r') as file:
                urls = file.read().splitlines()
                for url in urls:
                    process_url(url.strip(), available_file, unavailable_file)
        else:
            base_url = sys.argv[1]
            process_url(base_url, available_file, unavailable_file)

if __name__ == "__main__":
    main()

