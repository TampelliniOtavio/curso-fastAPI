import enum
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi import Path, Query, Header, Depends
from models import Curso, cursos
from typing import Any, Optional, Dict, List
from time import sleep

def fake_db():
    try:
        print('Abrindo conexão com banco de dados...')
        sleep(1)
    finally:
        print('Fechando conexão com bando de dados...')
        sleep(1)

app = FastAPI(
    title="API de Cursos da Geek University",
    version='0.0.1',
    description="Uma API para estudo do FastAPI"
)

@app.get('/calculadora')
async def get_calculadora(
        a: int = Query(default=0, gt=5),
        b: int = Query(default=0, gt=10),
        c: Optional[int] = 0,
        x_geek: str = Header(default=None)
    ):
    soma = a + b + c

    print(f'X_GEEK: {x_geek}')
    return {'resultado': soma}

@app.get('/cursos',
         description="Retorna todos os Cursos ou uma Lista Vazia",
         summary="Retorna todos os cursos",
         response_model=List[Curso],
         response_description='Cursos encontrados com sucesso')
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos

@app.get('/cursos/{curso_id}',
         description="Retorna o Curso Consultado ou Erro",
         summary="Retorna um curso",
         response_model=Curso,
         response_description="Curso Encontrado com sucesso")
async def get_curso(curso_id: int = Path(title='ID do Curso', description='Deve Ser entre 1 e 2', gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        for index, curso in enumerate(cursos):
            if curso.id == curso_id:
                return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cruso não encontrado')
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cruso não encontrado')
    
@app.post('/cursos',
          status_code=status.HTTP_201_CREATED,
          description="Cadastra ou Sobrescreve um Curso",
          summary="Cadastra um curso",
          response_model=Curso,
          response_description="Curso Cadastrado")
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    for i, item in enumerate(cursos):
        if item.id == curso.id:
            cursos[i] = curso
            return curso
    cursos.append(curso)
    return curso

@app.put('/cursos/{curso_id}',
         description="Atualiza um Curso, retorna erro caso não encontra",
         summary="Atualiza Um Curso",
         response_model=Curso,
         response_description="Curso Atualizado")
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    for i, item in enumerate(cursos):
        if item.id == curso_id:
            cursos[i] = curso
            return curso
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não Existe um curso com ID {curso_id}.')

@app.delete('/cursos/{curso_id}',
            status_code=status.HTTP_204_NO_CONTENT,
            description="Deleta um curso, retorna erro caso não encontra",
            summary="Deleta um curso")
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    for i, item in enumerate(cursos):
        if item.id == curso_id:
            cursos.remove(item)
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content='')
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não Existe um curso com ID {curso_id}.')
    

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
