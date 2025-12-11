from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from core.config import settings
from models.estudiante import Estudiante
from schemas.estudiante import EstudianteCreate, TokenData

# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        Hash de la contraseña
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña contra su hash
    
    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Hash de la contraseña
        
    Returns:
        True si la contraseña coincide, False en caso contrario
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT de acceso
    
    Args:
        data: Datos a codificar en el token
        expires_delta: Tiempo de expiración del token
        
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    """
    Decodifica y valida un token JWT
    
    Args:
        token: Token JWT a decodificar
        
    Returns:
        TokenData con la información del usuario o None si el token es inválido
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        correo_institucional: str = payload.get("sub")
        if correo_institucional is None:
            return None
        return TokenData(correo_institucional=correo_institucional)
    except JWTError:
        return None


def authenticate_estudiante(db: Session, correo_institucional: str, contrasena: str) -> Optional[Estudiante]:
    """
    Autentica un estudiante verificando sus credenciales
    
    Args:
        db: Sesión de base de datos
        correo_institucional: Correo institucional del estudiante
        contrasena: Contraseña en texto plano
        
    Returns:
        Objeto Estudiante si las credenciales son válidas, None en caso contrario
    """
    estudiante = db.query(Estudiante).filter(
        Estudiante.correo_institucional == correo_institucional
    ).first()
    
    if not estudiante:
        return None
    
    if not verify_password(contrasena, estudiante.contrasena_hash):
        return None
    
    return estudiante


def create_estudiante(db: Session, estudiante_data: EstudianteCreate) -> Estudiante:
    """
    Crea un nuevo estudiante en la base de datos
    
    Args:
        db: Sesión de base de datos
        estudiante_data: Datos del estudiante a crear
        
    Returns:
        Objeto Estudiante creado
    """
    hashed_password = hash_password(estudiante_data.contrasena)
    
    db_estudiante = Estudiante(
        nombres=estudiante_data.nombres,
        apellidos=estudiante_data.apellidos,
        correo_institucional=estudiante_data.correo_institucional,
        dni=estudiante_data.dni,
        contrasena_hash=hashed_password
    )
    
    db.add(db_estudiante)
    db.commit()
    db.refresh(db_estudiante)
    
    return db_estudiante


def get_estudiante_by_correo(db: Session, correo_institucional: str) -> Optional[Estudiante]:
    """
    Obtiene un estudiante por su correo institucional
    
    Args:
        db: Sesión de base de datos
        correo_institucional: Correo institucional del estudiante
        
    Returns:
        Objeto Estudiante si existe, None en caso contrario
    """
    return db.query(Estudiante).filter(
        Estudiante.correo_institucional == correo_institucional
    ).first()


def get_estudiante_by_dni(db: Session, dni: str) -> Optional[Estudiante]:
    """
    Obtiene un estudiante por su DNI
    
    Args:
        db: Sesión de base de datos
        dni: DNI del estudiante
        
    Returns:
        Objeto Estudiante si existe, None en caso contrario
    """
    return db.query(Estudiante).filter(Estudiante.dni == dni).first()
