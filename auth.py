from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta
import logging

from core.config import settings
from core.database import get_db, engine, Base
from schemas.estudiante import EstudianteCreate, EstudianteResponse, LoginRequest, Token
from services.auth_service import (
    create_estudiante,
    authenticate_estudiante,
    create_access_token,
    get_estudiante_by_correo,
    get_estudiante_by_dni
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API de autenticación para el sistema PAPPI Calculator",
    version="1.0.0"
)

# Manejador de errores de validación
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Error de validación: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": str(exc.body) if hasattr(exc, 'body') else None
        }
    )

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Endpoint raíz de la API"""
    return {
        "message": "Bienvenido a PAPPI Calculator Auth API",
        "version": "1.0.0",
        "endpoints": {
            "registro": "/registro",
            "login": "/login",
            "health": "/health"
        }
    }


@app.get("/health")
def health_check():
    """Endpoint de health check"""
    return {"status": "healthy", "service": "auth"}


@app.post(
    "/registro",
    response_model=EstudianteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo estudiante",
    description="Crea una cuenta nueva para un estudiante con sus datos personales"
)
async def registrar_estudiante(
    estudiante: EstudianteCreate,
    db: Session = Depends(get_db)
):
    """
    Registra un nuevo estudiante en el sistema
    
    Args:
        estudiante: Datos del estudiante a registrar
        db: Sesión de base de datos
        
    Returns:
        Datos del estudiante registrado
        
    Raises:
        HTTPException: Si el correo o DNI ya están registrados
    """
    logger.info(f"Intentando registrar estudiante: {estudiante.correo_institucional}")
    logger.info(f"Datos recibidos: nombres={estudiante.nombres}, apellidos={estudiante.apellidos}, dni={estudiante.dni}")
    
    # Verificar si el correo ya existe
    existing_correo = get_estudiante_by_correo(db, estudiante.correo_institucional)
    if existing_correo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo institucional ya está registrado"
        )
    
    # Verificar si el DNI ya existe
    existing_dni = get_estudiante_by_dni(db, estudiante.dni)
    if existing_dni:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El DNI ya está registrado"
        )
    
    # Crear el estudiante
    try:
        db_estudiante = create_estudiante(db, estudiante)
        logger.info(f"Estudiante registrado exitosamente: {estudiante.correo_institucional}")
        return db_estudiante
    except Exception as e:
        logger.error(f"Error al registrar estudiante: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar el estudiante: {str(e)}"
        )


@app.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Autentica a un estudiante y retorna un token JWT"
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Autentica a un estudiante y genera un token JWT
    
    Args:
        login_data: Credenciales del estudiante (correo y contraseña)
        db: Sesión de base de datos
        
    Returns:
        Token JWT de acceso
        
    Raises:
        HTTPException: Si las credenciales son inválidas
    """
    # Autenticar al estudiante
    estudiante = authenticate_estudiante(
        db,
        login_data.correo_institucional,
        login_data.contrasena
    )
    
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo institucional o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear el token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": estudiante.correo_institucional},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
