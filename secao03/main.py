from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from models import Curso

app = FastAPI()

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

@app.get('/cursos')
async def get_cursos():
    return cursos

@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int):
    try:
        curso = cursos[curso_id]
        curso.update({'id': curso_id})
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cruso não encontrado')
    
@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso):
    next_id = len(cursos) + 1
    del curso.id
    cursos[next_id] = curso
    return curso

@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso):
    if curso_id not in cursos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não Existe um curso com ID {curso_id}.')

    del curso.id
    cursos[curso_id] = curso
    return curso

@app.delete('/cursos/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int):
    if curso_id not in cursos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não Existe um curso com ID {curso_id}.')

    del cursos[curso_id]
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content='')
    

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
