import requests
from pprint import pprint
from bs4 import BeautifulSoup

sercoplus = {
    'targer': ".product-miniature.js-product-miniature",
    'targer_pagination': '.next.js-search-link'
}

impacto = {
    'targer': ".single-product",
    'targer_pagination': 'ul.pagination li:last-child a[class="page-link"]'
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


def extract_link(item) -> str:
    link_str = ''
    a_tag = item.find('a', href=True)
    product_links = a_tag.get('href') if a_tag else None

    if product_links:
        link_str = f'link_product: {str(product_links)}\n'

    img_tag = item.find('img', src=True)
    image_link = img_tag.get('src') if img_tag else None
            
    if image_link:
        link_str = link_str + f'link_img: {str(image_link)}\n'
        
    return link_str


def get_items(soup: BeautifulSoup, target_group_items: str, target_pagination: str) -> tuple[list, bool]:
    select_items = soup.select(target_group_items)
    items_list = []
    for item in select_items:
        value_item =  item.get_text(strip=True, separator='\n')
        links = extract_link(item)
        value_item =  value_item + '\n' + links
        items_list.append(value_item)
        
    select_pagination = soup.select(target_pagination)
    
    empty_pagination = True if not select_pagination else False
    
    print(empty_pagination, type(empty_pagination))
    return items_list, empty_pagination


def main():
    urlx = 'https://www.impacto.com.pe/catalogo?categoria=Accesorios%20para%20Laptop&c=30&page='
    url = 'https://www.sercoplus.com/266-PromoPlus?page='
    num_page = 1
    empty_pagination = False
    target_group_items = impacto['targer']
    target_pagination = impacto['targer_pagination']
    while not empty_pagination:
        
        new_url = f'{urlx}{num_page}'
        page_result = get_page(new_url)
        data_result, empty_pagination = get_items(page_result, target_group_items, target_pagination)
        
        print(f'link de la pagina: {new_url}')
        
        for data in data_result:
            print(data)
            
        num_page = num_page + 1

if '__main__' == __name__:
    main()