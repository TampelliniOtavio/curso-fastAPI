from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaArtigos, UsuarioSchemaCreate, UsuarioSchemaUpdate
from core.deps import get_current_user, get_session
from core.auth import autenticar, criar_token_acesso
from core.security import gerar_hash_senha

router = APIRouter()

# GET Logado
@router.get("/logado", response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado

# POST / Signup
@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_signup(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
        is_admin=usuario.is_admin
    )

    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()
            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Já existe um usuário com este email cadastrado")

# GET Usuarios
@router.get("/", response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioModel] = result.scalars().unique().all()

        return usuarios

# GET Usuario
@router.get("/{usuario_id}", response_model=UsuarioSchemaArtigos)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()

        if not usuario:
            raise HTTPException(detail="Usuário não encontrado", status_code=status.HTTP_404_NOT_FOUND)
        
        return usuario

# PUT Usuario
@router.put("/{usuario_id}", response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if not usuario_up:
            raise HTTPException(detail="Usuário não encontrado", status_code=status.HTTP_404_NOT_FOUND)
        
        if usuario.nome:
            usuario_up.nome = usuario.nome
        
        if usuario.sobrenome:
            usuario_up.sobrenome = usuario.sobrenome
        
        if usuario.email:
            usuario_up.email = usuario.email
        
        if usuario.is_admin is not None:
            usuario_up.is_admin = usuario.is_admin
        
        if usuario.senha:
            usuario_up.senha = gerar_hash_senha(usuario.senha)

        await session.commit()
        
        return usuario_up

# DELETE Usuario
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if not usuario:
            raise HTTPException(detail="Usuário não encontrado", status_code=status.HTTP_404_NOT_FOUND)

        await session.delete(usuario)
        await session.commit()
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)

# POST Login
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(form_data.username, form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Dados de Acesso Incorretos")

    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id), "token_type": "Bearer"}, status_code=status.HTTP_200_OK)
