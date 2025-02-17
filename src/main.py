from llm_modelito import LLMJsonExtractor
from scrape import get_page, get_items, save_data_json
import json


def load_data()-> dict:
    with open('json/info_store.json', 'r', encoding='utf-8') as file:
        datos = json.load(file)
        return datos
    return {}


def scrape_plus_ia():
    
    store = load_data()
    if not store:
        return
    
    store = store['impacto']
    
    urls =  store['urls']
    page = store['page']    
    target_group_items = store['target_group']
    target_pagination = store['target_pagination']
    
    
    model = LLMJsonExtractor()
    name_file = 'impacto.json'
    list_result = []
    
    for url in urls:
        num_page = 1
        empty_pagination = False
        while not empty_pagination:
            new_url = f'{url}{page}{num_page}'
            page_result = get_page(new_url)
            data_result, empty_pagination = get_items(page_result, target_group_items, target_pagination)
            
            print(f'link de la pagina: {new_url}')
            
            for data in data_result:
                print('data: ',data)
                result = model.extract_json(data)
                list_result.append(result)
                
            num_page = num_page + 1
        
        save_data_json(name_file,list_result)
    
    print('se termino :)))')




if __name__ == '__main__':
    scrape_plus_ia()