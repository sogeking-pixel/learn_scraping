import requests
from bs4 import BeautifulSoup
from bs4 import Tag
from scrape import get_page, save_data_json

level_list = [
    'ul.products.flex li div a',
    'ul.products.flex li div a']

def get_urls(soup, target: str, prefix = None)->list:
    a_tags = soup.select(target)
    urls = []
    for a_tag in a_tags:
        url = a_tag.get('href')
        print(url)
        url = prefix + url if not url.startswith('http') and prefix else url
        urls.append(url)
    return urls
    

def backtracking_fake(url:str)->list:
    urls=[url]
    prefix = 'https://www.memorykings.pe'
    for level in level_list:
        aux = []
        for url in urls:
            soup = get_page(url)
            news_urls = get_urls(soup, level, prefix)
            aux.extend(news_urls)
        urls = aux
    return urls


def main():
    url = 'https://www.memorykings.pe/productos'
    urls = backtracking_fake(url)
    print(urls)
    save_data_json('urls.json', urls)
    

if __name__ == '__main__':
    main()