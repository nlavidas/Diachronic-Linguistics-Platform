import requests
from bs4 import BeautifulSoup

# Search Project Gutenberg for Argonautica translations
gutenberg_url = 'https://www.gutenberg.org/ebooks/search/?query=Argonautica'
response = requests.get(gutenberg_url)
soup = BeautifulSoup(response.text, 'html.parser')

print('=== GUTENBERG ARGONAUTICA TRANSLATIONS ===')
for result in soup.select('li.booklink'):
    title_elem = result.select_one('span.title')
    author_elem = result.select_one('span.author')
    link_elem = result.select_one('a')
    
    if title_elem and link_elem:
        title = title_elem.get_text(strip=True)
        author = author_elem.get_text(strip=True) if author_elem else 'Unknown'
        link = 'https://www.gutenberg.org' + link_elem['href']
        
        print(f'Title: {title}')
        print(f'Author: {author}')
        print(f'Link: {link}')
        print('---')

print('\n=== SEARCH COMPLETE ===')
