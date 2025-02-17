from bs4 import BeautifulSoup
import requests
from parse import parse_with_ollama
from typing import Optional
def hola():
    price_impacto = 0
    price_memorykings = 0

    page_to_scrape = requests.get('https://www.impacto.com.pe/producto/mouse-logitech-g203-lightsync-gaming-910-005790-hasta-8000-dpi-6-botones-programables-rgb-negro')
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    prices = soup.find_all("span",{'class': 'regular-price'})

    for price in prices:
        clean_price = price.get_text(strip=True)
        price_dolares = clean_price.split("-")[0].strip()  # Toma el valor después de "-"
        price_impacto = float(price_dolares[1::])


    page_to_memoriking = requests.get('https://www.memorykings.pe/producto/326731/mouse-gaming-logitech-g203-lightsync-rgb-8k-black')
    soup = BeautifulSoup(page_to_memoriking.text, "html.parser")
    prices = soup.find_all('div', {'class':'price pt-1'})
    for price in prices:
        clean_price = price.get_text(strip=True)
        price_dolares = clean_price.split("ó")[0].strip()  # Toma el valor después de "-"
        price_memorykings= float(price_dolares[2::])



    print('precio de impacto: ', price_impacto)
    print('precio de memoriking: ', price_memorykings)

    if price_impacto > price_memorykings:
        print('Opcion a comprar, memoriking')
    elif price_memorykings == price_impacto:
        print('Misma mierda')
    else:
        print('Opcion a comrpar, Impactame esta')
    
    
def extrac_content(url, name_class):
    url_page = url
    response = requests.get(url_page)
    if response.status_code != 200:
        raise('fallido')
    soup = BeautifulSoup(response.text, "html.parser")
    
    header = soup.find("header")  
    if header:
        header.extract()  

    footer = soup.find("footer") 
    if footer:
        footer.extract()
        
    content_data = soup.body
    if not content_data:
        return ''
    return str(content_data)
    
def clean_content(body: str):
    soup = BeautifulSoup(body, "html.parser")
    for script_or_style in soup(['script', 'style']):
        script_or_style.extract
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def scrape_website(url: str, setting : dict) -> Optional[str]:
    api_url = f'https://r.jina.ai/{url}'
    try:
        response = requests.get(api_url, headers=setting)
        if response.status_code != 200:
            raise Exception('error')
        return response.text
    
    except Exception as e:
        print(f'error: {e}')
        return None

data_impacto = {
    'target': '.single-product-page'
}

data_memoryking = {
    'target': 'section > .car-header > h1, #slider-detalle .lslide.active',
    'targetxd': 'section > .car-header , #slider-detalle .lslide.active , div > .car-section'
    
}


# 'section:has(> .breadcrumbs)' para obtener el padre apartir del hijo


if __name__ == '__main__':
    url ='https://www.impacto.com.pe/producto/mouse-logitech-g203-lightsync-gaming-910-005790-hasta-8000-dpi-6-botones-programables-rgb-negro'
    url_memory = 'https://www.memorykings.pe/producto/349370/memoria-ddr5-48gb-8200-cl40-g-skill-trident-z5-rgb'
    # body_data = extrac_content(url, name_class='single-product-page')
    # result = clean_content(body_data)
    # print(result)
    headers = {
       
        "x-target-selector":data_memoryking['target'],
        # "x-respond-with": "text"
    }
    result_ai = scrape_website(url_memory,setting=headers)
    # result_ai = clean_content(result_ai.text)
    print(result_ai)
    # pront = 'i want you to capture the price and product name and display it in json'
    # xd = parse_with_ollama(result,pront)
    # print(xd)
