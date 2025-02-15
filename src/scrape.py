import requests
from pprint import pprint
from bs4 import BeautifulSoup

headersxd = {
    'targer': ".product-miniature.js-product-miniature",
    'targer_pagination': '.next.js-search-link'
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

def get_items(soup: BeautifulSoup, target: str, target_pagination: str) -> tuple[list, bool]:
    select_items = soup.select(target)
    items_list = []
    for item in select_items:
        value_item =  item.get_text(strip=True, separator='\n')
        items_list.append(value_item)
        
    select_pagination = soup.select(target_pagination)
    
    empty_pagination = True if not select_pagination else False
    
    print(empty_pagination, type(empty_pagination))
    return items_list, empty_pagination


def main():
    urlx = 'https://www.sercoplus.com/545-video-nvidia-geforce-rtx'
    url = 'https://www.sercoplus.com/266-PromoPlus?page='
    num_page = 1
    empty_pagination = False
    target_group_items = '.product-miniature.js-product-miniature'
    target_pagination = '.next.js-search-link'
    while not empty_pagination:
        
        new_url = f'{url}{num_page}'
        page_result = get_page(new_url)
        data_result, empty_pagination = get_items(page_result, target_group_items, target_pagination)
        
        print(f'link de la pagina: {new_url}')
        
        for data in data_result:
            print(data)
            print(type(data), '\n,\n\n')
            
        num_page = num_page + 1

if '__main__' == __name__:
    main()