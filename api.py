from funcoes_api import delete_check, validar_existencia, json_load, json_dump
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI( title="API de Gestão Acadêmica", description="API REST para gerenciamento de estudantes, professores, disciplinas, turmas e matrículas.", version="1.0.0")

#Arquivos JSON
arquivo_estudantes = "estudantes.json"
arquivo_professores = "professores.json"
arquivo_disciplinas = "disciplinas.json"
arquivo_turmas = "turmas.json"
arquivo_matriculas = "matriculas.json"

#Classes pydantic:
class Estudante(BaseModel):
    nome: str
    cpf: str

class Professor(BaseModel):
    nome: str
    cpf: str

class Disciplina(BaseModel):
    nome: str

class Turma(BaseModel):
    id_professor: int # A classe Turma exige um ID de professor existente
    id_disciplina: int # A classe Turma também exige um ID de discipglina existente
# ATENÇÃO: Atualmente cada turma aceita apenas 1 professor e 1 disciplina.
# Para permitir múltiplos professores no futuro, altere "id_professor: int"
# para "ids_professores: list[int]" e ajuste as validações do POST e PUT.
# Com SQL, essa relação será melhor modelada com uma tabela intermediária

class Matricula(BaseModel):
    id_estudante: int
    id_turma: int

# ----- ESTUDANTES -----

#HOME
@app.get("/")
def home() -> dict:
    return {"mensagem": "API de Gestão Acadêmica","docs": "/docs", "versao": "1.0.0"}

#Listar estudantes
@app.get("/estudantes", tags=["Estudantes"])
def listar_estudantes() -> list[dict]:
    return json_load(arquivo_estudantes)

#Listar estudante por ID
@app.get("/estudantes/{id}", tags=["Estudantes"])
def listar_estudante_id(id: int) -> dict:
    arquivo = json_load(arquivo_estudantes)

    for estudante in arquivo:
        if estudante["id"] == id:
            return estudante

    raise HTTPException(status_code=404, detail="Estudante não encontrado") #comunica corretamente que o recurso não existe

#Criar estudante
@app.post("/estudantes", tags=["Estudantes"], status_code=201)
def criar_estudante(estudante: Estudante) -> dict:
    arquivo = json_load(arquivo_estudantes)

    # Impede que o mesmo CPF seja cadastrado mais de uma vez
    for e in arquivo:
        if e["cpf"] == estudante.cpf:
            raise HTTPException(status_code=400, detail="CPF já cadastrado")

    estudante = estudante.model_dump() # Converte o objeto Pydantic para dicionário

    # Como nesta versão não há uso de banco de dados, o código a seguir gera um ID único manualmente:
    estudante["id"] = max([item["id"] for item in arquivo], default=0) + 1
    # Significado simplificado, para melhor compreensão: max(LISTA_DE_IDS, default=0) + 1
    # [item["id"] for item in arquivo] -> cria uma lista com todos os IDs usando list comprehension (forma compacta de criar listas usando for em uma única linha)
    # max(..., default=0) -> pega o maior ID da lista, ou 0 se a lista estiver vazia ("default" é argumento da função max)
    # + 1 -> gera o próximo ID disponível, evitando duplicação
    # Com DB relacional este problema seria resolvido automaticamente com algo como AUTO_INCREMENT (MySQL), que gera o ID automaticamente

    arquivo.append(estudante)
    json_dump(arquivo, arquivo_estudantes)
    return estudante

#Atualizar estudante
@app.put("/estudantes/{id}", tags=["Estudantes"])
def atualizar_estudante(id: int, estudante: Estudante) -> dict:
    arquivo = json_load(arquivo_estudantes)

    # Impede duplicidade de CPF, ignorando o próprio registro
    for e in arquivo:
        if e["id"] != id and e["cpf"] == estudante.cpf:
            raise HTTPException(status_code=400, detail="CPF já cadastrado")

    novos_dados = estudante.model_dump() #Converte pra dicionário

    for index, estudante_salvo in enumerate(arquivo): #“Para cada estudante no arquivo, me dê também a posição dele na lista”
        if estudante_salvo["id"] == id:
            novos_dados["id"] = id
            arquivo[index] = novos_dados
            json_dump(arquivo, arquivo_estudantes)
            return novos_dados

    raise HTTPException(status_code=404, detail="Estudante não encontrado")

#Deletar estudante
@app.delete("/estudantes/{id}", tags=["Estudantes"], status_code=204)
def deletar_estudante(id: int):
    arquivo = json_load(arquivo_estudantes)
    # Função que impede a exclusão se o estudante possui vínculo com alguma matrícula:
    delete_check(arquivo_matriculas, "id_estudante", id, "Não é possível excluir este estudante, pois ele está vinculado a uma matrícula")

    for index, estudante in enumerate(arquivo): #“Para cada estudante no arquivo, me dê também a posição dele na lista”
        if estudante["id"] == id:
            arquivo.pop(index)
            json_dump(arquivo, arquivo_estudantes)
            return

    raise HTTPException(status_code=404, detail="Estudante não encontrado")


# ----- PROFESSORES -----

#Listar professores
@app.get("/professores", tags=["Professores"])
def listar_professores() -> list[dict]:
    return json_load(arquivo_professores)

#Listar professor por ID
@app.get("/professores/{id}", tags=["Professores"])
def listar_professor_id(id: int) -> dict:
    arquivo = json_load(arquivo_professores)

    for professor in arquivo:
        if professor["id"] == id:
            return professor

    raise HTTPException(status_code=404, detail="Professor não encontrado")

#Criar professor
@app.post("/professores", tags=["Professores"], status_code=201)
def criar_professor(professor: Professor) -> dict:
    arquivo = json_load(arquivo_professores)

    for p in arquivo:
        if p["cpf"] == professor.cpf:
            raise HTTPException(status_code=400, detail="CPF já cadastrado")

    professor = professor.model_dump()

    professor["id"] = max([item["id"] for item in arquivo], default=0) + 1

    arquivo.append(professor)
    json_dump(arquivo, arquivo_professores)
    return professor

#Atualizar professor
@app.put("/professores/{id}", tags=["Professores"])
def atualizar_professor(id: int, professor: Professor) -> dict:
    arquivo = json_load(arquivo_professores)

    for p in arquivo:
        if p["id"] != id and p["cpf"] == professor.cpf:
            raise HTTPException(status_code=400, detail="CPF já cadastrado")

    novos_dados = professor.model_dump()

    for index, professor_salvo in enumerate(arquivo):
        if professor_salvo["id"] == id:
            novos_dados["id"] = id
            arquivo[index] = novos_dados
            json_dump(arquivo, arquivo_professores)
            return novos_dados

    raise HTTPException(status_code=404, detail="Professor não encontrado")

#Deletar professor
@app.delete("/professores/{id}", tags=["Professores"], status_code=204)
def deletar_professor(id: int):
    arquivo = json_load(arquivo_professores)
    delete_check(arquivo_turmas, "id_professor", id, "Não é possível excluir este professor, pois ele está vinculado a uma turma")

    for index, professor in enumerate(arquivo):
        if professor["id"] == id:
            arquivo.pop(index)
            json_dump(arquivo, arquivo_professores)
            return

    raise HTTPException(status_code=404, detail="Professor não encontrado")


# ----- DISCIPLINAS -----

#Listar disciplinas
@app.get("/disciplinas", tags=["Disciplinas"])
def listar_disciplinas() -> list[dict]:
    return json_load(arquivo_disciplinas)

#Listar disciplina por ID
@app.get("/disciplinas/{id}", tags=["Disciplinas"])
def listar_disciplina_id(id: int) -> dict:
    arquivo = json_load(arquivo_disciplinas)

    for disciplina in arquivo:
        if disciplina["id"] == id:
            return disciplina

    raise HTTPException(status_code=404, detail="Disciplina não encontrada")

#Criar disciplina
@app.post("/disciplinas", tags=["Disciplinas"], status_code=201)
def criar_disciplina(disciplina: Disciplina) -> dict:
    arquivo = json_load(arquivo_disciplinas)
    disciplina = disciplina.model_dump()

    disciplina["id"] = max([item["id"] for item in arquivo], default=0) + 1

    arquivo.append(disciplina)
    json_dump(arquivo, arquivo_disciplinas)
    return disciplina

#Atualizar disciplina
@app.put("/disciplinas/{id}", tags=["Disciplinas"])
def atualizar_disciplina(id: int, disciplina: Disciplina) -> dict:
    arquivo = json_load(arquivo_disciplinas)
    novos_dados = disciplina.model_dump()

    for index, disciplina_salvo in enumerate(arquivo):
        if disciplina_salvo["id"] == id:
            novos_dados["id"] = id
            arquivo[index] = novos_dados
            json_dump(arquivo, arquivo_disciplinas)
            return novos_dados

    raise HTTPException(status_code=404, detail="Disciplina não encontrada")

#Deletar disciplina
@app.delete("/disciplinas/{id}", tags=["Disciplinas"], status_code=204)
def deletar_disciplina(id: int):
    arquivo = json_load(arquivo_disciplinas)
    delete_check(arquivo_turmas, "id_disciplina", id, "Não é possível excluir esta disciplina, pois ela está vinculada a uma turma")

    for index, disciplina in enumerate(arquivo):
        if disciplina["id"] == id:
            arquivo.pop(index)
            json_dump(arquivo, arquivo_disciplinas)
            return

    raise HTTPException(status_code=404, detail="Disciplina não encontrada")


# ----- TURMAS -----

#Listar turmas
@app.get("/turmas", tags=["Turmas"])
def listar_turmas() -> list[dict]:
    return json_load(arquivo_turmas)

#Listar turma por ID
@app.get("/turmas/{id}", tags=["Turmas"])
def listar_turma_id(id: int) -> dict:
    arquivo = json_load(arquivo_turmas)

    for turma in arquivo:
        if turma["id"] == id:
            return turma

    raise HTTPException(status_code=404, detail="Turma não encontrada")

#Criar turma
@app.post("/turmas", tags=["Turmas"], status_code=201)
def criar_turma(turma: Turma) -> dict:
    arquivo = json_load(arquivo_turmas)

    # Valida se o ID informado existe antes de realizar a operação.
    validar_existencia(arquivo_professores, "id", turma.id_professor, "Professor não encontrado")
    validar_existencia(arquivo_disciplinas, "id", turma.id_disciplina, "Disciplina não encontrada")

    turma = turma.model_dump()

    turma["id"] = max([item["id"] for item in arquivo], default=0) + 1

    arquivo.append(turma)
    json_dump(arquivo, arquivo_turmas)
    return turma

#Atualizar turma
@app.put("/turmas/{id}", tags=["Turmas"])
def atualizar_turma(id: int, turma: Turma) -> dict:
    arquivo = json_load(arquivo_turmas)

    validar_existencia(arquivo_professores, "id", turma.id_professor, "Professor não encontrado")
    validar_existencia(arquivo_disciplinas, "id", turma.id_disciplina, "Disciplina não encontrada")

    novos_dados = turma.model_dump()

    for index, turma_salvo in enumerate(arquivo):
        if turma_salvo["id"] == id:
            novos_dados["id"] = id
            arquivo[index] = novos_dados
            json_dump(arquivo, arquivo_turmas)
            return novos_dados

    raise HTTPException(status_code=404, detail="Turma não encontrada")

#Deletar turma
@app.delete("/turmas/{id}", tags=["Turmas"], status_code=204)
def deletar_turma(id: int):
    arquivo = json_load(arquivo_turmas)
    delete_check(arquivo_matriculas, "id_turma", id, "Não é possível excluir esta turma, pois ela está vinculada a uma matrícula")

    for index, turma in enumerate(arquivo):
        if turma["id"] == id:
            arquivo.pop(index)
            json_dump(arquivo, arquivo_turmas)
            return

    raise HTTPException(status_code=404, detail="Turma não encontrada")


# ----- MATRÍCULAS -----

#Listar matrículas
@app.get("/matriculas", tags=["Matrículas"])
def listar_matriculas() -> list[dict]:
    return json_load(arquivo_matriculas)

#Listar matrícula por ID
@app.get("/matriculas/{id}", tags=["Matrículas"])
def listar_matricula_id(id: int) -> dict:
    arquivo = json_load(arquivo_matriculas)

    for matricula in arquivo:
        if matricula["id"] == id:
            return matricula

    raise HTTPException(status_code=404, detail="Matrícula não encontrada")

#Criar matrícula
@app.post("/matriculas", tags=["Matrículas"], status_code=201)
def criar_matricula(matricula: Matricula) -> dict:
    arquivo = json_load(arquivo_matriculas)

    validar_existencia(arquivo_estudantes, "id", matricula.id_estudante, "Estudante não encontrado")
    validar_existencia(arquivo_turmas, "id", matricula.id_turma, "Turma não encontrada")

    # Impede matrícula duplicada: um estudante não pode ser matriculado na mesma turma mais de uma vez.
    # Essa regra mantém a consistência dos dados e simula uma constraint UNIQUE (id_estudante, id_turma)
    # que normalmente seria aplicado em um banco de dados relacional.
    for m in arquivo:
        if m["id_estudante"] == matricula.id_estudante and m["id_turma"] == matricula.id_turma:
            raise HTTPException(status_code=400, detail="Estudante já matriculado nesta turma")

    matricula = matricula.model_dump()

    matricula["id"] = max([item["id"] for item in arquivo], default=0) + 1

    arquivo.append(matricula)
    json_dump(arquivo, arquivo_matriculas)
    return matricula

#Atualizar matrícula
@app.put("/matriculas/{id}", tags=["Matrículas"])
def atualizar_matricula(id: int, matricula: Matricula) -> dict:
    arquivo = json_load(arquivo_matriculas)

    validar_existencia(arquivo_estudantes, "id", matricula.id_estudante, "Estudante não encontrado")
    validar_existencia(arquivo_turmas, "id", matricula.id_turma, "Turma não encontrada")

    # Impede duplicidade de matrícula ao atualizar, ignorando o próprio registro
    # Se as 3 condições forem verdadeiras, a atualização geraria uma matrícula já existente.
    for m in arquivo:
        if m["id"] != id and m["id_estudante"] == matricula.id_estudante and m["id_turma"] == matricula.id_turma:
            raise HTTPException(status_code=400, detail="Estudante já matriculado nesta turma")

    novos_dados = matricula.model_dump()

    for index, matricula_salvo in enumerate(arquivo):
        if matricula_salvo["id"] == id:
            novos_dados["id"] = id
            arquivo[index] = novos_dados
            json_dump(arquivo, arquivo_matriculas)
            return novos_dados

    raise HTTPException(status_code=404, detail="Matrícula não encontrada")

#Deletar matrícula
@app.delete("/matriculas/{id}", tags=["Matrículas"], status_code=204)
def deletar_matricula(id: int):
    arquivo = json_load(arquivo_matriculas)

    for index, matricula in enumerate(arquivo):
        if matricula["id"] == id:
            arquivo.pop(index)
            json_dump(arquivo, arquivo_matriculas)
            return

    raise HTTPException(status_code=404, detail="Matrícula não encontrada")