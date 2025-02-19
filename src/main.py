from llm_modelito import LLMJsonExtractor
from scrape import get_page, get_items, save_data_json, get_items_custom
import json


urls =  ''
page = ''    
target_group =''
target_pagination = ''
target_item = {}


def initialize_store(name_store: str)->bool:
    global urls, page, target_group, target_pagination, target_item
    
    store = load_data()
    if not store:
        return False
    
    store = store[name_store]
   
    urls =  store['urls']
    page = store['page']    
    target_group = store['target_group']
    target_pagination = store['target_pagination']
    target_item =  store['target_item'] 
    
    return True


def load_data()-> dict:
    with open('json/info_store.json', 'r', encoding='utf-8') as file:
        datos = json.load(file)
        return datos
    return {}


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
    
    

def scrape_plus_manual():
    if not initialize_store('impacto'):
        return
    name_file = 'impacto_custon_expresion_regular.json'
    list_result = []
    
    for url in urls:
        num_page = 1
        empty_pagination = False
        while not empty_pagination:
            new_url = url if num_page == 1 else f'{url}{page}{num_page}'
            
            page_result = get_page(new_url)
            
            print(f'link de la pagina: {new_url}')
            
            if not page_result:
                print(f'❌ Error: No se proceso correcamtne la pagina{new_url}')
                break
            
            data_result, empty_pagination = get_items_custom(page_result, target_group, target_pagination, target_item)
            
            list_result.extend(data_result)
            
            num_page = num_page + 1
            
        
        save_data_json(name_file,list_result)
    
    print('se termino :)))')
    

if __name__ == '__main__':
    # scrape_plus_ia()
    scrape_plus_manual()