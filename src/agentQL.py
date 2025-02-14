import os
from dotenv import load_dotenv
import agentql
from agentql.ext.playwright.async_api import Page
import requests
import asyncio
from playwright.async_api import async_playwright
from pprint import pprint
import json
load_dotenv()

PRODUCTS_QUERY = """ 
{
    products[]{
        name
        url_product
        price_dollar(Dollar)
        price_soles(Soles PEN)
        stock
        url_img
        is_discount(True or False)
        value_discount(0 in case you do not have)
        type_discount(null in case of not having, in case of having: porcent or value dollar or value soles)
    }
}
"""

async def get_data(page: Page):
    pricing_data = await page.query_data(PRODUCTS_QUERY)
    return pricing_data.get("products", [])

async def main(url: str, name_file: str):
    data_products = loan_data_json(name_file)
    async with async_playwright() as playwright, await playwright.firefox.launch(headless=False) as browser:
        raw_page = await browser.new_page()
        page = await agentql.wrap_async(raw_page)
        await page.goto(url, timeout=60000)
        while True:         
            result = await get_data(page)
            data_products.extend(result) 
            pagination_info = await page.get_pagination_info()
            if not pagination_info.has_next_page:
                break
            await pagination_info.navigate_to_next_page() 
        save_data_json(name_file, data_products)
        

urls_data = {
    'impacto' : {
        'url' : ["https://www.impacto.com.pe/catalogo"],
        'page' : '?page='
    },
    'memoriking' : {
        'url' : [
            "https://www.memorykings.pe/novedades"
            ],
        'page' : '?pagina='
    },
    'sercoplus':{
        'urls':[
            'https://www.sercoplus.com/262-smartwatch',
            'https://www.sercoplus.com/3-laptops',
            'https://www.sercoplus.com/731-arma-tu-pc',
            'https://www.sercoplus.com/94-teclados-y-mouse',
            'https://www.sercoplus.com/74-auriculares',
            'https://www.sercoplus.com/4-accesorios',
            'https://www.sercoplus.com/145-redes',
            'https://www.sercoplus.com/8-monitores',
            'https://www.sercoplus.com/65-impresoras',
            'https://www.sercoplus.com/228-proyectores',
            'https://www.sercoplus.com/28-software',
            'http://sercoplus.com/170-tintas',
            'http://sercoplus.com/193-memorias-usb-sd'
            ],
        'page' : '?page='
    }
}

def loan_data_json(name_file: str)->dict:
    data_products = []
    if os.path.exists(name_file):
        with open(name_file, "r", encoding="utf-8") as f:
            data_products = json.load(f)
    return data_products

def save_data_json(name_file: str, data: list)->None:
     with open(name_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    

if __name__ == '__main__':
    
    name_file = 'data_sercoplus.json'
    
   
    urls = urls_data['sercoplus']['urls']
    page = urls_data['sercoplus']['page']
    
    for url in urls:
            url_new = f'{url}'
            print('\n','+'*30,'\n',f'open url: {url_new}')
            result = asyncio.run(main(url_new, name_file))
