from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.database import Base


class Estudiante(Base):
    """Modelo de estudiante para el sistema de autenticación"""
    
    __tablename__ = "estudiantes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    correo_institucional = Column(String(255), unique=True, index=True, nullable=False)
    dni = Column(String(20), unique=True, index=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Estudiante(id={self.id}, nombres={self.nombres}, apellidos={self.apellidos}, correo={self.correo_institucional})>"
