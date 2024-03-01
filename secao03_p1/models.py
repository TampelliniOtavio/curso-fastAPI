from typing import Optional
from pydantic import BaseModel

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

cursos = [
    Curso(id=1, titulo="Programação para Leigos", aulas=32, horas=54),
    Curso(id=2, titulo="Algoritmos e Lógica de programação", aulas=42, horas=74),
]