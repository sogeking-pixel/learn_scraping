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

def parse_number(input_str)->float | None:
    pattern_float_english = r'^((\d{1,3}(,\d{3})*)|\d+)(\.\d{2})?$'
    pattern_float_europe = r'^((\d{1,3}(\.\d{3})*)|\d+)(,\d{2})?$'
    
    input_str = input_str.strip()
    
    if re.search(pattern_float_english, input_str):
        clean_str = input_str.replace(',', '')
        return round(float(clean_str), 2)
        
    if re.search(pattern_float_europe, input_str):
        clean_str = input_str.replace('.', '').replace(',', '.')
        return round(float(clean_str), 2)
        
    return None

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
        result["value_discount"] = parse_number(discount_value) if discount_value else None
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
        result = parse_text(value_element, r'\$')
        result_float = parse_number(result)
        return {key: result_float}
    elif key == "price_soles":
        result = parse_text(value_element, r'S/')
        result_float = parse_number(result)
        return {key: result_float}
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
        return {key: value_element.get_text(strip=True, separator='\n') if value_element else None}

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
                prefix = target.get("prefix") if target.get("prefix") else ""
                url = prefix + value_element.get(attribute)
                items_data[key] = url
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
