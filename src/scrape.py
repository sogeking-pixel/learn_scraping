import requests
from pprint import pprint
from bs4 import BeautifulSoup

headersxd = {
    'targer': ".product-miniature.js-product-miniature"
}

struct_data = {
    'name': '.product-name',
    'url_product': '.product-cover-link',
    'price_dollar': '.price.product-price.currency2',
    'url_img': None,
    'stock':'.price.product-price.stock-mini',
    'is_discount':None,
    'value_discount':None,
    'type_discount':None,
}

def get_page(url: str):
    response = requests.get(url=url)
    if response.status_code != 200:
        return
    if response.url != url:
        return
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def get_items(soup: BeautifulSoup, target: str, struct_data: dict) -> list:
    select_items = soup.select(target)
    items_list = []
    for item in select_items:
        value_item =  item.get_text(strip=True, separator='\n')
        
        items_list.append(value_item)
    return items_list


def main():
    urlx = 'https://www.sercoplus.com/545-video-nvidia-geforce-rtx'
    url = 'https://www.sercoplus.com/266-PromoPlus'
    target = '.product-miniature.js-product-miniature'
    page_result = get_page(url)
    data_result = get_items(page_result, target, struct_data)
    for data in data_result:
        print(data)
        print(type(data), '\n,\n\n')

if '__main__' == __name__:
    main()