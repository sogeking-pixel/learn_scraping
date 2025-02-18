import requests
from bs4 import BeautifulSoup
import json


def get_page(url: str):
    response = requests.get(url=url)
    if response.status_code != 200:
        print(f'status code is {response.status_code}')
        return
    if response.url != url:
        print(f'url is diferent, original: {url}, response: {response.url}')
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


def get_items(soup: BeautifulSoup, target_group: str, target_pagination: str) -> tuple[list, bool]:
    select_items = soup.select(target_group)
    items_list = []
    for item in select_items:
        value_item =  item.get_text(strip=True, separator='\n')
        links = extract_link(item)
        value_item =  value_item + '\n' + links
        items_list.append(value_item)
        
    select_pagination = soup.select(target_pagination)
    
    empty_pagination = True if not select_pagination else False
    
    return items_list, empty_pagination

def get_link():
    pass

def get_items_custom(soup: BeautifulSoup, target_group: str, target_pagination: str, target_item: dict)->tuple[list,bool]:
    select_items = soup.select(target_group)
    items_list = []
    
    for item in select_items:
        items_data = {}
        for key, target in target_item.items():
            selector = target.get("selector")
            attribute = target.get("attribute") 

            value_element = item.select_one(selector)
            
            if not value_element:
                items_data[key] = None
                continue

            if attribute:
                items_data[key] = value_element.get(attribute)
                continue
            
            items_data[key] = value_element.get_text(strip=True, separator='\n')

            
        items_list.append(items_data)
        
    select_pagination = soup.select(target_pagination)
    
    empty_pagination = True if not select_pagination else False
    
    return items_list, empty_pagination



def save_data_json(name_file: str, data: list)->None:
    with open(name_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    print('se guardo:/')
