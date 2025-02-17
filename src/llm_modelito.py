from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

import json
import re


template = ( "Su tarea consiste en extraer información y transformalo los datos en formato json,  del siguiente contenido de texto: {data_str}."
    "Por favor, siga estas instrucciones cuidadosamente: \n\n"
    "1. **Extraer información:** Extraiga sólo la información que coincida directamente con la descripción proporcionada y realizar el formato a json, con todo condiciones necesaria: {parse_description}. "
    "2. **Sin contenido adicional:** No incluya texto adicional, comentarios o explicaciones en su respuesta. "
    "3. **Respuesta vacía:** Si ninguna información coincide con la descripción, devuelva una un dict vacio."
    " 4. **Sólo datos directos:** Su respuesta debe contener el json con su condiciones y estrucutra establecida, sin ningún otro texto. reitero SOLO JSON"     
)

class LLMJsonExtractor:
    def __init__(self,  model_name: str = "llama3.2-vision"):
        self.json_structure = """
        name_product:
        price_dollar: (mantener un solo formato que sea el punto como separador de decimal, y eliminar el simbolo de dolar, que quede flotante, ten encuenta que puede ver otro con el simoblo de dolar, pero seguramente sea el descuento, asi que el mayor de los dos numero sea el correcto)
        stock:
        price_soles: (Soles PEN, misma solicitud que para el precio dollar)
        url_product:
        link_img:
        is_discount: (true o false, dependiendo si oferta o no)
        type_discount(null en el caso que no tenga, pero en el caso que si:  porcent or value dollar or value soles)
        value_discount(0 en caso que no tenga oferta o que no se encuentre el valor del descuenta, en ese caso se supone que es algun regalo extra, asi que dejalo como 0 , y el valor que ponga que sea solo el numero no pongas simbolo porfa)
        """
        model = OllamaLLM(model=model_name)
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model
        self.model = chain
    

    def __clean_json(self, text: str) -> str:
        match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
        if match:
            json_text = match.group(1).strip()
        else:
            json_text = re.sub(r"^`{3,}|`{3,}$", "", text).strip()
        
        return json_text


    
    def extract_json(self, data_str: str) -> dict:
        response  = self.model.invoke( {"data_str": data_str, "parse_description": self.json_structure} )
        result_clean = self.__clean_json(response)
        try:
            parsed_json = json.loads(result_clean)
            print(f'pruducto json: {list(parsed_json.values())[0]}')
            return parsed_json
        except json.JSONDecodeError as e:
            print("❌ Error JSON:", e)
            return {}
