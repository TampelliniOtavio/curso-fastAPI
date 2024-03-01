from typing import Optional
from pydantic import BaseModel, validator

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int
    
    @validator("titulo")
    def validar_titulo(cls, value: str):
        palavras = value.split(" ")
        if len(palavras) < 3:
            raise ValueError("O título deve ter pelo menos 3 palavras")

        if value.islower():
            raise ValueError("O título dever se capitalizado")

        return value
    
    @validator("aulas")
    def validar_aulas(cls, value: int):
        if value < 12:
            raise ValueError("Deve ter no mínimo 12 Aulas")

        return value
    
    @validator("horas")
    def validar_horas(cls, value: int):
        if value < 12:
            raise ValueError("Deve ter no mínimo 12 Horas")
        
        return value

cursos = [
    Curso(id=1, titulo="Programação para Leigos", aulas=32, horas=54),
    Curso(id=2, titulo="Algoritmos e Lógica de programação", aulas=42, horas=74),
]