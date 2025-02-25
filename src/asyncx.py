import aiohttp
from bs4 import BeautifulSoup
from scrape import get_items_custom
import time
import asyncio
import aiohttp
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    # Más User-Agents
]

async def async_get_page(url: str, session: aiohttp.ClientSession) -> BeautifulSoup:
    try:
        headers = {
            "User-Agent": random.choice(user_agents),  # Lista de User-Agents
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

        async with session.get(
            url,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=30),
            ssl=False,
            allow_redirects=True
        ) as response:
            if response.status != 200:
                print(f'Status code {response.status} en {url}')
                return None

            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            return soup

    except Exception as e:
        print(f'Error al obtener {url}: {str(e)}')
        return None

async def scrape_url_async(url: str, page: str, session: aiohttp.ClientSession, target_group: str, target_pagination: str, target_item: dict) -> list:
    num_page = 1
    empty_pagination = False
    results = []
    
    while True:
      
        new_url = url if num_page == 1 else f'{url}{page}{num_page}'
        print(f'Procesando la página: {new_url}')
        
        soup = await async_get_page(new_url, session)
        if not soup:
            print(f'❌ Error: No se procesó correctamente la página {new_url}')
            break
        
        data_result, _ = get_items_custom(soup, target_group, target_pagination, target_item)
        if not data_result:
            print(f'❌ Terminó la paginación en {new_url}')
            break
        results.extend(data_result)
        num_page += 1
        
    return results




# Entrada principal
if __name__ == "__main__":
    start_time = time.time()
    
    store_name = 'impacto'  # Ajusta el nombre de la tienda según corresponda
    # asyncio.run(scrape_plus_manual_async(store_name))
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tiempo de ejecución: {execution_time:.2f} segundos")

