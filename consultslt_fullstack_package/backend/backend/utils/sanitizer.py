

import re

def clean_cnpj(cnpj):
    return re.sub(r"\D","",cnpj)

def clean_cpf(cpf):
    return re.sub(r"\D","",cpf)

def clean_cep(cep):
    return re.sub(r"\D","",cep)

def clean_phone(phone):
    return re.sub(r"\D","",phone)

