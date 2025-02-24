import re
import json
from scrape import save_data_json
import unicodedata

def remove_accents(text):
   
    normalized_text = unicodedata.normalize('NFD', text)
    without_accents = ''.join(
        c for c in normalized_text if not unicodedata.combining(c)
    )
    return without_accents



def categorizar_producto(nombre: str) -> str:
    nombre = nombre.lower()
    nombre = remove_accents(nombre)
    print(nombre)
    
    categorias = {
        "teclado": [
            r"\bteclado\b", r"\bkeyboard\b"
        ],
        "mouse": [
            r"\bmouse\b", r"\bratón\b",
        ],
        "pad mouse": [
            r"\bpad\b", r"\bmousepad\b", r"\balfombrilla\b"
        ],
        "monitor": [
            r"\bmonitor\b", r"\bpantalla\b"
        ],
        "gráfica": [
            r"\brtx\b", r"\bgtx\b", r"\bradeon\b", r"\brx\b", 
            r"\bgeforce\b" r"\bgrafica\b", 
            r"\bgráfica\b", r"\bgpu\b", r"\bgraphics\b",r"\bgddr[0-9]\b"
        ],
        "cpu": [
            r"\bcpu\b", r"\bprocesador\b", r"\bryzen\b", 
            r"\bcore\s*i[3579]\b", r"\bathlon\b", r"\bxeon\b", 
            r"\bpentium\b"
        ],
        "laptop": [
            r"^(?!.*\bcooler\b).*?\blaptop\b", r"(?!.*\bcooler\b).*?\bnotebook\b",
            r"\bultrabook\b", r"\bchromebook\b"
        ],
        "almacenamiento": [
            r"\bssd\b", r"\bhdd\b", r"\bdisco\b", r"\bnvme\b", 
            r"\bsata\b"
        ],
        "placa madre": [
            r"\bmotherboard\b", r"\bplaca\s*madre\b", 
            r"\bplaca\s*base\b", r"\bchipset\b", r"\bmainboard\b"
        ],
        "memoria ram": [
            r"\bram\b", r"\bddr[345]\b", 
            r"\b[0-9]+gb\s*ddr\b", r"\bso-dimm\b"
        ],
        "fuente poder": [
            r"\bfuente\b", r"\bpsu\b", r"\bpower\s*supply\b", 
            r"\bcertificada\b", r"\b80+\s*plus\b"
        ],
        "case": [
            r"\bcase\b", r"\bgabinete\b", r"\bchasis\b", 
            r"\bmidi\s*tower\b"
        ],
        "cooler": [
            r"\bcooler\b", r"\bdisipador\b",  r"\bliquido\b",
            r"\blíquido\b", r"\baio\b", r"\bwater\s*cooling\b", r"\brefrigeración\b", r"\brefrigeracion\b"
        ],
        "fans": [
            r"\bfan\b", r"\bventilador\b", r"\bventilación\b"
        ],
        "pastas termicas": [
            r"\bpasta\b", r"\btérmica\b", r"\bthermal\b", r"\btermica\b"
        ],
        "audifonos": [
            r"\bauriculares\b", r"\bheadset\b", r"\bheadphones\b", r"\bauricular\b", r"\baudifono\b", r"\bheadphone\b", r"\baudifonos\b"
        ],
        "microfonos": [
            r"\bmicrofono\b", r"\bmicrophone\b", r"\bmicrofono\b", r"\bmicro\b"
        ],
        
        "controles": [
            r"\bcontrol\b", r"\bjoystick\b", r"\bgamepad\b", 
            r"\bgamepad\b", r"\bcontrol\b", r"\bmando\b",  r"\bvolante\b"
        ],
        "memorias usb": [
             r"^(?!.*\bpuerto\b).*?\busb\b.*?\d+(GB|TB)\b",
            r"^(?!.*\bpuerto\b).*?\bpendrive\b.*?\d+(GB|TB)\b",
            r"^(?!.*\bpuerto\b).*?\bflash\b.*?\d+(GB|TB)\b"
        ],
        "sillas": [
            r"\bsilla\b", r"\bchair\b"
        ],
        "tablets": [
            r"\btablet\b", r"\btableta\b", r"\bipad\b"
        ],
        "impresoras": [
            r"\bimpresora\b", r"\bprinter\b", r"\bscanner\b", r"\bescaner\b"
        ],
        "webcams": [
            r"\bwebcam\b", r"\bcámara\s*web\b", r"\bcamara\s*web\b"
        ],
        "parlantes": [
            r"\bparlante\b", r"\bspeaker\b", r"\baltavoz\b", r"\baltavoces\b"
        ],
        "equipos de vigilancia": [
            r"\bseguridad\b", r"\balarma\b", 
            r"\bvideovigilancia\b"
        ],
        "equipos de red": [
            r"\brouter\b", r"\bmodem\b", r"\bswitch\b", 
            r"\baccess\s*point\b", r"\brepetidor\b", r"\bnas\b"
        ],
        "software": [
            r"\bsoftware\b", r"\bsistema\s*operativo\b",
        ],
        "adaptadores": [
            r"\badaptador\b", r"\bcable\b", r"\bconector\b", r"\badaptadores\b"
        ],
        "celulares": [
            r"\bcelular\b", r"\bsmartphone\b", r"\biphone\b", 
            r"\bphone\b"
        ],
        "smartwatch": [
            r"\bsmartwatch\b", r"\bwatch\b"
        ],
        "estabilizadores": [
            r"\bestabilizador\b", r"\bups\b"
        ],
        
    }

    orden_prioridad = [
    "laptop", "tablets", "celulares", "impresoras", "smartwatch","pad mouse","case", "estabilizadores",
    "cooler", "pastas termicas",
    
    "audifonos", "gráfica", "cpu", "placa madre", "memoria ram", 
    "almacenamiento", "fuente poder",
    
    "monitor", "teclado", "mouse", 
    "webcams", "controles",
    
    "microfonos",
    "equipos de vigilancia", "software",
    "equipos de red", "adaptadores", 
    "parlantes",
    
    "sillas", "fans", "memorias usb",
]

    for categoria in orden_prioridad:
        for patron in categorias[categoria]:
            if re.search(patron, nombre, flags=re.IGNORECASE):
                return categoria
    return "otros"


def load_data(name_file: str):
    with open(name_file, 'r', encoding='utf-8') as file:
        datos = json.load(file)
        return datos
    return None

def main():
    for store in ['sercoplus', 'impacto','memorykings']:
        file_name = f'data_products/{store}.json'
        productos = load_data(file_name)
        for producto in productos:
            producto['category'] = categorizar_producto(producto['name'])
        save_data_json(file_name, productos)

if __name__ == '__main__':
    main()
