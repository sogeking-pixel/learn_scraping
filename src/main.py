from llm_modelito import LLMJsonExtractor
from asyncx import scrape_url_async
from scrape import get_page, get_items, save_data_json, get_items_custom
import json
import argparse
import time
import asyncio
import aiohttp

urls =  ''
page = ''    
target_group =''
target_pagination = ''
target_item = {}


def initialize_store(name_store: str)->bool:
    global urls, page, target_group, target_pagination, target_item
    
    store = load_data('json/info_store.json')
    if not store:
        return False
    
    store = store[name_store]
   
    urls =  load_data( store['urls_file'])
    if not urls:
        return False
    page = store['page']    
    target_group = store['target_group']
    target_pagination = store['target_pagination']
    target_item =  store['target_item'] 
    
    return True


def load_data(name_file: str):
    with open(name_file, 'r', encoding='utf-8') as file:
        datos = json.load(file)
        return datos
    return None


def scrape_plus_ia():
    
    if not initialize_store(name_store = 'impacto'):
        return
    
    model = LLMJsonExtractor()
    name_file = 'impacto.json'
    list_result = []
    
    for url in urls:
        num_page = 1
        empty_pagination = False
        while not empty_pagination:
            new_url = f'{url}{page}{num_page}'
            page_result = get_page(new_url)
            data_result, empty_pagination = get_items(page_result, target_group, target_pagination)
            
            print(f'link de la pagina: {new_url}')
            
            for data in data_result:
                print('data: ',data)
                result = model.extract_json(data)
                list_result.append(result)
                
            num_page = num_page + 1
        
        save_data_json(name_file,list_result)
    
    print('se termino :)))')
    
    

def scrape_plus_manual(store_name: str):
    if not initialize_store(store_name):
        return
    name_file = f'data_products/{store_name}.json'
    list_result = []
    
    for url in urls:
        num_page = 1
        
        while True:
            new_url = url if num_page == 1 else f'{url}{page}{num_page}'
            
            page_result = get_page(new_url)
            
            if not page_result:
                print(f'❌ Error: No se proceso correcamtne la pagina {new_url}')
                break
            
            data_result, _ = get_items_custom(page_result, target_group, target_pagination, target_item)
            if not data_result:
                print(f'❌ Termino la paginacion em {new_url}')
                break
            
            print(f'link de la pagina: {new_url}')
            list_result.extend(data_result)
            num_page = num_page + 1
            
        save_data_json(name_file,list_result)
    
    print('se termino :)))')
    

async def scrape_plus_manual_async(store_name: str):
    if not initialize_store(store_name):
        return
    name_file = f'data_products/{store_name}.json'
    print(urls)
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(scrape_url_async(url,page, session, target_group, target_pagination, target_item))
        
        results_list = await asyncio.gather(*tasks)
        
    list_result = []
    for r in results_list:
        list_result.extend(r)
    
    save_data_json(name_file, list_result)
    print('Se terminó el scraping :)')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Scrape store data")
    parser.add_argument('-t', '--store', type=str, help="Name of the store to process")
    args = parser.parse_args()
    start_time = time.time()
    
    store_names = ['sercoplus', 'impacto', 'memorykings']
    if args.store:
        print(f'se esta procesando la tienda: {args.store}')
        del store_names
        store_names = [args.store]
       
      
    for store in store_names:
        print(f'se esta procesando la tienda: {store}')
        scrape_plus_manual(store)
        # asyncio.run(scrape_plus_manual_async(store))
        
        
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tiempo de ejecución: {execution_time:.2f} segundos")