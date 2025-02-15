from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

import json
import re


template = ( "Su tarea consiste en extraer información y transformalo los datos en formato json,  del siguiente contenido de texto: {data_str}."
    "Por favor, siga estas instrucciones cuidadosamente: \n\n"
    "1. **Extraer información:** Extraiga sólo la información que coincida directamente con la descripción proporcionada y realizar el formato a json, con todo condiciones necesaria: {parse_description}. "
    "2. **Sin contenido adicional:** No incluya texto adicional, comentarios o explicaciones en su respuesta. "
    "3. **Respuesta vacía:** Si ninguna información coincide con la descripción, devuelva una lista vacia []."
    " 4. **Sólo datos directos:** Su respuesta debe contener el json con su condiciones y estrucutra establecida, sin ningún otro texto. reitero SOLO JSON"    
)

class LLMJsonExtractor:
    def __init__(self,  model_name: str = "llama3.2-vision"):
        self.json_structure = """
        name_product:
        price_dollar: (mantener un solo formato que sea el punto como separador de decimal, y eliminar el simbolo de dolar, que quede flotante)
        stock:
        price_soles: (Soles PEN, misma solicitud que para el precio dollar)
        url_product:
        link_img:
        is_discount: (True o False)
        type_discount(null en el caso que no tenga, pero en el caso que si:  porcent or value dollar or value soles)
        value_discount(0 en caso que no tenga o que no se establesca el valor de descuento)
        """
        model = OllamaLLM(model=model_name)
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model
        self.model = chain
    
    def __clean_json(self, text: str) -> str:
        matches = re.findall(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        
        clear_text =  matches[0].strip() if matches else text.strip()
        
        if clear_text.startswith("```"):
            clear_text = clear_text[len("```"):].strip()
            
        if clear_text.endswith("```"):
            clear_text = clear_text[:-3].strip()
            
        return clear_text
    
    def extract_json(self, data_str: str) -> dict:
        response  = self.model.invoke( {"data_str": data_str, "parse_description": self.json_structure} )
        print(response)
        result_clean = self.__clean_json(response )
        print(result_clean)
        return json.loads(result_clean)


if __name__ == "__main__":
    data_str = """Mochila Teros ( Te-ids18570 ) Negro C/ Negro | P/ 15.6"
MINICÓDIGO:
018426
STOCK:
1
$16.50 -
                    S/62.04
link_product: https://www.impacto.com.pe/producto/mochila-teros-te-ids18570-negro-c-negro-p-15-6
link_img: https://www.impacto.com.pe/storage/products/sm/171027873651896.jpg
    """
    
    model = LLMJsonExtractor()
    result = model.extract_json(data_str)
    print(f'resultado: {result}, tipo: {type(result)}')