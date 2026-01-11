from src.web.configs import config

def paginate(elements, page):
    """
    Dada una lista de elementos, se devuelve una porción de esos elementos, según el número de páginas
    """
    #Esto se carga de la configuración
    per_page = int(config["cantRegPags"])
    
    start = (page - 1) * per_page
    end = start + per_page

    pag =  elements[start:end]
    return pag

def get_total_pages(elements, page):
    """
    Calcula el total de páginas a mostra para una lista de elementos.
    """
    #Esto se carga de la configuración
    per_page = int(config["cantRegPags"])
    total_elements = len(elements)
    total_pages = (total_elements + per_page - 1) // per_page
    return total_pages

