from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
import re


class EstudianteBase(BaseModel):
    """Schema base para estudiante"""
    nombres: str = Field(..., min_length=2, max_length=100, description="Nombres del estudiante")
    apellidos: str = Field(..., min_length=2, max_length=100, description="Apellidos del estudiante")
    correo_institucional: EmailStr = Field(..., description="Correo institucional del estudiante")
    dni: str = Field(..., min_length=8, max_length=20, description="DNI del estudiante")


class EstudianteCreate(EstudianteBase):
    """Schema para crear un estudiante"""
    contrasena: str = Field(..., min_length=6, max_length=72, description="Contraseña del estudiante")
    
    @field_validator('dni')
    @classmethod
    def validar_dni(cls, v):
        """Validar que el DNI contenga solo números"""
        if not v.isdigit():
            raise ValueError('El DNI debe contener solo números')
        if len(v) < 7 or len(v) > 20:
            raise ValueError('El DNI debe tener entre 7 y 20 dígitos')
        return v
    
    @field_validator('contrasena')
    @classmethod
    def validar_contrasena(cls, v):
        """Validar requisitos mínimos de la contraseña"""
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        return v


class EstudianteResponse(EstudianteBase):
    """Schema para respuesta de estudiante"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Schema para solicitud de login"""
    correo_institucional: EmailStr
    contrasena: str


class Token(BaseModel):
    """Schema para respuesta de token JWT"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema para datos del token"""
    correo_institucional: Optional[str] = None
