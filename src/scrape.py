import requests
from bs4 import BeautifulSoup
from bs4 import Tag
import json
import re


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

def clear_space_line(text: str) -> str:
    return text.replace(" ", "").replace("\n", "")


def get_symbol_value(symbol_expression: str, text: str) -> tuple[str, str] | tuple[None, None]:
    pattern = rf"({symbol_expression}).*?((\d{{1,3}}(?:(?:,\d{{3}})+(?:\.\d{{2}})?)|(?:(?:\.\d{{3}})+(?:,\d{{2}})?)|\d+(?:(,|\.)\d{{2}})?))"
    match = re.search(pattern, text)
    if not match:
        return None, None
    return match.group(1), match.group(2)


def get_data(value_element: Tag, key: str) -> dict:
    if key == "value_discount":
        result = {
            "is_discount": False,
            "value_discount": None,
            "type_discount": None
        }
        if not value_element:
            return result

        value_text = clear_space_line(value_element.get_text(strip=True, separator='\n'))
        symbol, discount_value = get_symbol_value(r'\$|\%', value_text)
        result["is_discount"] = True
        result["value_discount"] = discount_value
        result["type_discount"] = "dollar" if symbol == '$' else ("porcent" if symbol == '%' else None)
        return result

    def parse_text(elem: Tag, regex: str = None) -> str | None:
        if not elem:
            return None
        text = clear_space_line(elem.get_text(strip=True, separator='\n'))
        if regex:
            _, value = get_symbol_value(regex, text)
            return value
        return text

    if key == "price_dollar":
        return {key: parse_text(value_element, r'\$')}
    elif key == "price_soles":
        return {key: parse_text(value_element, r'S/')}
    elif key == "stock":
        if not value_element:
            return {key: None}
        text = clear_space_line(value_element.get_text(strip=True, separator='\n'))
        match = re.search(r'(<|>|\+|)(\d+)', text)
        if not match:
            return {key: None}
        symbol, value =  match.group(1), match.group(2)
        return {key: symbol + value}
    else:
        return {key: parse_text(value_element)}

def get_items_custom(soup: BeautifulSoup, target_group: str, target_pagination: str, target_item: dict)->tuple[list,bool]:
    select_items = soup.select(target_group)
    items_list = []
    
    for item in select_items:
        items_data = {}
        for key, target in target_item.items():
            selector = target.get("selector")
            attribute = target.get("attribute") 

            value_element = item.select_one(selector)

            if attribute:
                items_data[key] = value_element.get(attribute)
                continue
            
            items_data.update( get_data(value_element, key) ) 

            
        items_list.append(items_data)
        
    select_pagination = soup.select(target_pagination)
    
    empty_pagination = True if not select_pagination else False
    
    return items_list, empty_pagination



def save_data_json(name_file: str, data: list)->None:
    with open(name_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    print('se guardo:/')
