from bson import ObjectId
import datetime

def mongo_to_dict(mongo_object):
    """
    Converte um único objeto do MongoDB para um dicionário Python limpo e compatível com JSON.
    """
    if not mongo_object:
        return None
    
    data = dict(mongo_object)
    
    if '_id' in data and isinstance(data['_id'], ObjectId):
        data['id'] = str(data['_id'])
        del data['_id']

    for key, value in data.items():
        if isinstance(value, datetime.datetime):
            data[key] = value.isoformat()

    return data

def mongo_list_to_dict_list(mongo_list):
    """
    Converte uma lista de objetos do MongoDB para uma lista de dicionários limpos.
    """
    if not mongo_list:
        return []
    return [mongo_to_dict(item) for item in mongo_list]