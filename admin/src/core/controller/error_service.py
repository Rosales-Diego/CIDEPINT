from src.core.config.database import db
from src.core.models.Institutional_Services.services import Service
import re


# funciones en comun
def solo_letras_y_comas(texto):
    if re.match("^[a-zA-Z,]*$", texto):
        return True
    else:
        return False

def contiene_numeros_ni_caracteres_especiales(input_string):
    # Utilizamos una expresión regular para buscar números o caracteres especiales en el string
    pattern = r'[0-9!@#$%^&*()_+={}\[\]:;"\'<>,.?/\|\\]'
    
    # Usamos re.search para encontrar una coincidencia en el string
    if re.search(pattern, input_string):
        return True  # Se encontró al menos un número o caracter especial
    else:
        return False 

#funciones nombre
def name_exists(service_name,institution_id):
    """
        Valida si existe un servicio con el mismo nombre 
    """
    service = Service.query.filter_by(name=service_name, 
                                      institutions_id=institution_id).first()
    if service is  None:
        return (False)
    else:
        return (True)


def validator_name(name,error_list,institution_id):
    
    """
        Realiza la validacion completa del name del servicio.
        Retorna una varable booleana que indica si cumple
        con lo solicitado y un lista de error si es que
        no cumpla con alguna consigna 
    """
    meets = True
    
    if (contiene_numeros_ni_caracteres_especiales(name)):
        error_list.append("El nombre tiene que ser una cadena valida")
        meets = False
    else:
        if(not name_exists(name,institution_id)):
            error_list.append("El nombre del servicio ya existe")    
            meets = False   
    return ((meets,error_list))

#funciones palabras calves
def obtener_palabras_claves(search_keywords):
        palabras_lista = search_keywords.split(',')
        nombres_limpios = [nombre.strip() for nombre in palabras_lista]
    
        return nombres_limpios

def exists_word(keywords_list,new_search_keywords):
    encontro = False
    
    for new_key in new_search_keywords:
        for key_list in keywords_list:
            if(new_key == key_list): 
                encontro = True
    return (encontro)

def validator_keywords(search_keywords,error_list,institution_id):

    #traigo los servicio de la institucion
    services = Service.query.filter_by(institutions_id=institution_id).all()
        
    #traigo todas la palabras claves de los servicios 
    keywords_list = []
    for service in  services:
        keywords = service.search_keywords
        if keywords:
            keywords_list.extend(keywords.split(','))  # Suponiendo que las palabras clave están separadas por comas    
        
    if(solo_letras_y_comas(search_keywords)):
       #validar si no existe un key igual
       uno=1
    else:
        error_list.append("La palabras claves tiene que estar separadas por ,")
        
    return ("esperar")   
    
#validar datos
def validator (name,search_keywords,authorized_centers,institution_id):
    error_list = []
    result = True
    
    if (contiene_numeros_ni_caracteres_especiales(name)):
        error_list.append("El nombre tiene que ser una cadena valida")
    else:
        if(name_exists(name,institution_id)):
            error_list.append("Ya existe un servicio con el mismo nombre y tipo ")
            result = False
            
    #controlar la descripcion
    
    if(not solo_letras_y_comas(search_keywords)):
        result = False
        error_list.append("La palabras claves tiene que estar separadas por ,")
        
    if(not solo_letras_y_comas(authorized_centers)):
        result = False
        error_list.append("Los centros autorizados tiene que estar separadas por ,")
        
              
    return((result,error_list))

def validator_update(name,description,search_keywords,authorized_centers,institution_id):
    
    error_list = []
    result = True
    if (not name):
        error_list.append("Se tiene que cargar un nombre ")
    else:
        if(name_exists(name,institution_id)):
            error_list.append("Ya existe un servicio con el mismo nombre")
            result = False
            
    if(description):
        error_list.append("La descripcion no tiene que estar vacia")
        result = False
        
    if(search_keywords):
        if(not solo_letras_y_comas(search_keywords)):
            result = False
            error_list.append("La palabras claves tiene que estar separadas por ,")
        
    if(authorized_centers):
        if(not solo_letras_y_comas(authorized_centers)):
            result = False
            error_list.append("Los centros autorizados tiene que estar separadas por ,")    
            
    return ((result,error_list))