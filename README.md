# 🎓 API de Gestão Acadêmica

Projeto desenvolvido como exercício de **fundamentos de APIs REST com Python**, sem uso de banco de dados. Implementei manualmente conceitos que normalmente são abstraídos por ORMs e bancos relacionais — como geração de IDs, integridade referencial e validações de duplicidade — demonstrando o funcionamento dessas camadas na prática.

A API gerencia estudantes, professores, disciplinas, turmas e matrículas, com persistência em arquivos JSON.

---

## 📋 Funcionalidades

- **Estudantes** — cadastrar, listar, atualizar e remover estudantes
- **Professores** — cadastrar, listar, atualizar e remover professores
- **Disciplinas** — cadastrar, listar, atualizar e remover disciplinas
- **Turmas** — criar turmas vinculando professores e disciplinas existentes
- **Matrículas** — matricular estudantes em turmas existentes
- Integridade referencial e validações de negócio implementadas manualmente (detalhes abaixo)

---

## 🛠️ Tecnologias

- [Python 3.10+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)

---

## 🚀 Como executar

**1. Clone o repositório**
```bash
git clone https://github.com/jvmorva/api-gestao-academica.git
cd api-gestao-academica
```

**2. Crie e ative um ambiente virtual**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install fastapi uvicorn
```

**4. Inicie o servidor**
```bash
uvicorn api:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

---

## 📖 Documentação interativa

Após iniciar o servidor, acesse a documentação automática gerada pelo FastAPI:

| Interface | URL |
|-----------|-----|
| Swagger UI | `http://127.0.0.1:8000/docs` |
| ReDoc | `http://127.0.0.1:8000/redoc` |

---

## 🔢 Padrões de resposta

| Status HTTP | Significado |
|--------|------------|
| 200 | Sucesso |
| 201 | Recurso criado |
| 400 | Erro de validação |
| 404 | Recurso não encontrado |

---

<details>
<summary><h2>📡 Endpoints</h2></summary>

### Estudantes `/estudantes`
| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/estudantes` | Lista todos os estudantes |
| `GET` | `/estudantes/{id}` | Busca um estudante pelo ID |
| `POST` | `/estudantes` | Cadastra um novo estudante |
| `PUT` | `/estudantes/{id}` | Atualiza os dados de um estudante |
| `DELETE` | `/estudantes/{id}` | Remove um estudante |

### Professores `/professores`
| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/professores` | Lista todos os professores |
| `GET` | `/professores/{id}` | Busca um professor pelo ID |
| `POST` | `/professores` | Cadastra um novo professor |
| `PUT` | `/professores/{id}` | Atualiza os dados de um professor |
| `DELETE` | `/professores/{id}` | Remove um professor |

### Disciplinas `/disciplinas`
| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/disciplinas` | Lista todas as disciplinas |
| `GET` | `/disciplinas/{id}` | Busca uma disciplina pelo ID |
| `POST` | `/disciplinas` | Cadastra uma nova disciplina |
| `PUT` | `/disciplinas/{id}` | Atualiza os dados de uma disciplina |
| `DELETE` | `/disciplinas/{id}` | Remove uma disciplina |

### Turmas `/turmas`
| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/turmas` | Lista todas as turmas |
| `GET` | `/turmas/{id}` | Busca uma turma pelo ID |
| `POST` | `/turmas` | Cadastra uma nova turma |
| `PUT` | `/turmas/{id}` | Atualiza os dados de uma turma |
| `DELETE` | `/turmas/{id}` | Remove uma turma |

### Matrículas `/matriculas`
| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/matriculas` | Lista todas as matrículas |
| `GET` | `/matriculas/{id}` | Busca uma matrícula pelo ID |
| `POST` | `/matriculas` | Cadastra uma nova matrícula |
| `PUT` | `/matriculas/{id}` | Atualiza os dados de uma matrícula |
| `DELETE` | `/matriculas/{id}` | Remove uma matrícula |
</details>

---

## 📦 Estrutura do projeto

```
api-gestao-academica/
├── api.py              # Rotas e lógica principal da API
├── funcoes_api.py      # Funções utilitárias (I/O JSON, validações)
├── estudantes.json     # Gerado automaticamente na primeira execução
├── professores.json
├── disciplinas.json
├── turmas.json
├── matriculas.json
└── .gitignore
```

---

## 🔗 Relacionamentos

```
Professor ──┐
            ├──> Turma ───> Matrícula <─── Estudante
Disciplina ─┘
```

- Uma **turma** requer um professor e uma disciplina já cadastrados
- Uma **matrícula** requer um estudante e uma turma já cadastrados
- Não é possível excluir um registro que esteja vinculado a outro (integridade referencial)

---

## 🔒 Integridade referencial e validações de negócio

Como o projeto não utiliza banco de dados, essas garantias foram implementadas manualmente — reproduzindo o comportamento que um banco relacional ofereceria nativamente.

**Integridade referencial:**
- Não é possível excluir um professor vinculado a uma turma
- Não é possível excluir uma disciplina vinculada a uma turma
- Não é possível excluir um estudante vinculado a uma matrícula
- Não é possível excluir uma turma vinculada a uma matrícula
- Não é possível criar uma turma referenciando um professor ou disciplina inexistente
- Não é possível criar uma matrícula referenciando um estudante ou turma inexistente

**Validações de negócio:**
- CPF duplicado é rejeitado no cadastro e atualização de estudantes e professores
- Um estudante não pode ser matriculado na mesma turma mais de uma vez

---

## ⚠️ Observações / limitações

- Os dados são persistidos localmente em arquivos `.json`, sem banco de dados
- Não há controle de concorrência para escrita nos arquivos `.json`
- Não há autenticação ou controle de acesso aos endpoints
- Os IDs são gerados automaticamente de forma incremental
- Esta versão aceita apenas **um professor e uma disciplina por turma**. Para suportar múltiplos vínculos no futuro, os campos `id_professor` e `id_disciplina` deverão ser refatorados para listas e, idealmente, o projeto migrado para um banco de dados relacional com tabelas intermediárias para essas relações
