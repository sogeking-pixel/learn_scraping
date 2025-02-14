from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from typing import Optional

@dataclass
class Store:
    name: str
    url: str
    price_selector: dict
    price_split_char: str
    price_index: int
    price_offset: int

class PriceComparer:
    def __init__(self):
        self.stores = {
            'impacto': Store(
                name='Impacto',
                url='https://www.impacto.com.pe/producto/mouse-logitech-g203-lightsync-gaming-910-005790-hasta-8000-dpi-6-botones-programables-rgb-negro',
                price_selector= ['span', {'class': 'regular-price'}],
                price_split_char='-',
                price_index=0,
                price_offset=1
            ),
            'memorykings': Store(
                name='MemoryKings',
                url='https://www.memorykings.pe/producto/326731/mouse-gaming-logitech-g203-lightsync-rgb-8k-black',
                price_selector=['div',  {'class': 'price pt-1'}],
                price_split_char='ó',
                price_index=0,
                price_offset=2
            )
        }
        self.prices = {}

    def get_price(self, store: Store) -> Optional[float]:
        try:
            page = requests.get(store.url)
            soup = BeautifulSoup(page.text, "html.parser")
            price_elements = soup.find_all(store.price_selector[0], store.price_selector[1] )
            
            price = 0
            if price_elements:
                for price_element in price_elements:
                    clean_price = price_element.get_text(strip=True)
                    price_str = clean_price.split(store.price_split_char)[store.price_index].strip()
                    price = float(price_str[store.price_offset:])
                return price

            return None
        except Exception as e:
            print(f"Error getting price for {store.name}: {e}")
            return None

    def compare_prices(self):
        for store_id, store in self.stores.items():
            self.prices[store_id] = self.get_price(store)

        if None in self.prices.values():
            print("Error: Could not fetch all prices")
            return

        impacto_price = self.prices['impacto']
        memorykings_price = self.prices['memorykings']

        print(f'Precio de Impacto: {impacto_price}')
        print(f'Precio de MemoryKings: {memorykings_price}')

        if impacto_price > memorykings_price:
            print('Mejor opción: MemoryKings')
        elif memorykings_price > impacto_price:
            print('Mejor opción: Impacto')
        else:
            print('Precios iguales')

def main():
    comparer = PriceComparer()
    comparer.compare_prices()
    
if __name__ == "__main__":
    main()