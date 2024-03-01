from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi import Path, Query, Header, Depends
from models import Curso
from typing import Any, Optional
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
    version='0.0.1'
)

cursos = {
    1: {
        'titulo': 'Programação para leigos',
        'aulas': 112,
        'horas': 58,
    },
    2: {
        'titulo': 'Algoritmos de Programação',
        'aulas': 87,
        'horas': 67,
    },
}

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

@app.get('/cursos')
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos

@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int = Path(title='ID do Curso', description='Deve Ser entre 1 e 2', gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        curso.update({'id': curso_id})
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cruso não encontrado')
    
@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    next_id = len(cursos) + 1
    del curso.id
    cursos[next_id] = curso
    return curso

@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    if curso_id not in cursos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não Existe um curso com ID {curso_id}.')

    del curso.id
    cursos[curso_id] = curso
    return curso

@app.delete('/cursos/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id not in cursos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não Existe um curso com ID {curso_id}.')

    del cursos[curso_id]
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content='')
    

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
