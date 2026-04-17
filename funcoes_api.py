import json
from fastapi import HTTPException

# UTILIDADES (JSON) --------------------------------------------------------

def json_dump(lista, nome_arquivo): #Função para ADICIONAR (gravar) informações no arquivo json.
    with open(nome_arquivo, 'w', encoding="utf-8") as arquivo:
        json.dump(lista, arquivo, ensure_ascii=False)


def json_load(nome_arquivo): #Função para MOSTRAR (carregar) informações no arquivo json.
    try:
        with open(nome_arquivo, 'r', encoding="utf-8") as arquivo:
            lista = json.load(arquivo)
        return lista
    except FileNotFoundError:
        return []


# Funções APIs --------------------------------------------------------

# Verifica se existe algum registro vinculado ao ID informado e impede a exclusão caso exista.
def delete_check(nome_arquivo, campo_id, id, mensagem):
    arquivo = json_load(nome_arquivo)

    for item in arquivo:
        if item[campo_id] == id:
            raise HTTPException(
                status_code=400,
                detail=mensagem
            )

# Retorna o primeiro elemento da lista que corresponde ao par chave=valor, ou None se não encontrar.
def buscar_elemento(lista, chave, valor):
    for elemento in lista:
        if elemento[chave] == valor:
            return elemento
    return None

# Valida se o ID informado existe antes de realizar a operação (create/update).
def validar_existencia(nome_arquivo, campo, valor, mensagem):
    entidade = buscar_elemento(json_load(nome_arquivo), campo, valor)
    if not entidade:
        raise HTTPException(status_code=404, detail=mensagem)