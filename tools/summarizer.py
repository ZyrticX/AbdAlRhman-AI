
from bs4 import BeautifulSoup
import requests

def summarize_page(url):
    try:
        # Fetch the content from the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract titles and meaningful paragraphs
        titles = [t.get_text(strip=True) for t in soup.find_all(['h1', 'h2', 'h3'])]
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if len(p.get_text(strip=True)) > 50]

        # Combine the content
        content = "\n".join(titles[:5] + paragraphs[:5])
        summary = f"🗞️ Main headlines and content:\n{content}"

        return summary

    except Exception as e:
        return f"⚠️ An error occurred while summarizing the page: {e}"

