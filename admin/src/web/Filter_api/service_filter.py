from src.core.models.Institutional_Services.services import Service
from sqlalchemy import or_

def filter(filtros):
    
    if (filtros['name'] == '' and filtros['keyword'] == '' and 
        filtros['type_of_service'] == '' and filtros['institution_id'] == 0):
        services = Service.query.all()
        return services
    
    query = Service.query    
    if filtros['name'] != '':
        query = name_filter(filtros['name'],query)
    if filtros['keyword'] != '' :
        query = keyword_filter(filtros['keyword'],query)
    if filtros['type_of_service'] != '':
        query = type_of_service_filter(filtros['type_of_service'],query)
    if filtros['institution_id'] != 0:
        query = institution_id_filter(filtros['institution_id'],query)
    
    return query.all()


def name_filter(name, query):
    services = query.filter(Service.name.ilike('%{}%'.format(name)))
    return services

def keyword_filter(keyword , query):
    services = query.filter(Service.search_keywords.ilike('%{}%'.format(keyword)))
    return services

def type_of_service_filter(type_of_service, query):
    types_list = type_of_service.split(',')
    type_conditions = [Service.type_of_service == getattr(Service.TypeService, t) for t in types_list]
    services = query.filter(or_(*type_conditions))
    
    return services

def institution_id_filter(id, query):
    services = query.filter(Service.institutions_id == id)
    return services
