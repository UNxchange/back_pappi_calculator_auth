# PAPPI Calculator Auth API

API de autenticación para el sistema PAPPI Calculator. Proporciona endpoints para registro e inicio de sesión de estudiantes con autenticación JWT.

## 🚀 Características

- ✅ Registro de estudiantes con validación de datos
- ✅ Login con autenticación JWT
- ✅ Hashing seguro de contraseñas con bcrypt
- ✅ Base de datos PostgreSQL
- ✅ Validación de DNI (8 dígitos)
- ✅ Validación de contraseñas seguras
- ✅ API REST con FastAPI
- ✅ Documentación automática con Swagger

## 📋 Requisitos

- Python 3.8+
- PostgreSQL 12+
- Docker y Docker Compose (opcional, para desarrollo local)

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/UNxchange/back_pappi_calculator_auth.git
cd back_pappi_calculator_auth
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar el archivo `.env` y configurar las variables:

```env
DATABASE_URL=postgresql://pappi_user:pappi_password@localhost:5432/pappi_auth_db
SECRET_KEY=tu-clave-secreta-super-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**⚠️ IMPORTANTE**: Genera una clave secreta segura para `SECRET_KEY`. Puedes usar:

```bash
openssl rand -hex 32
```

### 5. Iniciar PostgreSQL con Docker (opcional)

```bash
docker-compose up -d
```

Esto iniciará una instancia de PostgreSQL en el puerto 5432.

## ▶️ Ejecutar la aplicación

```bash
uvicorn auth:app --reload --host 0.0.0.0 --port 8000
```

O directamente:

```bash
python auth.py
```

La API estará disponible en: `http://localhost:8000`

## 📚 Documentación de la API

Una vez iniciada la aplicación, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Endpoints

### 1. Registro de Estudiante

**POST** `/registro`

Registra un nuevo estudiante en el sistema.

**Request Body:**
```json
{
  "nombres": "Juan Carlos",
  "apellidos": "Pérez García",
  "correo_institucional": "juan.perez@universidad.edu.pe",
  "dni": "12345678",
  "contrasena": "MiPassword123"
}
```

**Requisitos de contraseña:**
- Mínimo 8 caracteres
- Al menos una letra mayúscula
- Al menos una letra minúscula
- Al menos un número

**Response (201 Created):**
```json
{
  "id": 1,
  "nombres": "Juan Carlos",
  "apellidos": "Pérez García",
  "correo_institucional": "juan.perez@universidad.edu.pe",
  "dni": "12345678",
  "created_at": "2025-12-11T10:30:00",
  "updated_at": null
}
```

### 2. Login

**POST** `/login`

Autentica a un estudiante y retorna un token JWT.

**Request Body:**
```json
{
  "correo_institucional": "juan.perez@universidad.edu.pe",
  "contrasena": "MiPassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Health Check

**GET** `/health`

Verifica el estado de la API.

**Response:**
```json
{
  "status": "healthy",
  "service": "auth"
}
```

## 🗄️ Estructura del Proyecto

```
back_pappi_calculator_auth/
├── auth.py                 # Aplicación principal con endpoints
├── requirements.txt        # Dependencias de Python
├── .env.example           # Ejemplo de variables de entorno
├── .gitignore            # Archivos ignorados por Git
├── docker-compose.yml    # Configuración de PostgreSQL
├── README.md             # Este archivo
├── core/
│   ├── __init__.py
│   ├── config.py         # Configuración de la aplicación
│   └── database.py       # Conexión a base de datos
├── models/
│   ├── __init__.py
│   └── estudiante.py     # Modelo SQLAlchemy de Estudiante
├── schemas/
│   ├── __init__.py
│   └── estudiante.py     # Schemas Pydantic para validación
└── services/
    ├── __init__.py
    └── auth_service.py   # Lógica de autenticación
```

## 🔐 Seguridad

- Las contraseñas se hashean con **bcrypt** antes de almacenarse
- Los tokens JWT expiran después de 30 minutos (configurable)
- Validación estricta de datos de entrada
- No se exponen contraseñas en las respuestas de la API

## 🧪 Pruebas

### Usando cURL

**Registro:**
```bash
curl -X POST "http://localhost:8000/registro" \
  -H "Content-Type: application/json" \
  -d '{
    "nombres": "María",
    "apellidos": "López",
    "correo_institucional": "maria.lopez@universidad.edu.pe",
    "dni": "87654321",
    "contrasena": "Password123"
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "correo_institucional": "maria.lopez@universidad.edu.pe",
    "contrasena": "Password123"
  }'
```

## 🐳 Docker

Para ejecutar todo el stack con Docker:

```bash
docker-compose up -d
```

## 📝 Notas

- El DNI debe tener exactamente 8 dígitos numéricos
- El correo institucional debe ser un email válido
- Los nombres y apellidos deben tener al menos 2 caracteres
- No se permiten duplicados de correo institucional o DNI

## 👨‍💻 Desarrollo

Para contribuir al proyecto:

1. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
2. Realiza tus cambios y haz commit: `git commit -am 'Agrega nueva funcionalidad'`
3. Push a la rama: `git push origin feature/nueva-funcionalidad`
4. Crea un Pull Request

## 📄 Licencia

Este proyecto es parte del sistema PAPPI Calculator.

## 🆘 Soporte

Para reportar problemas o solicitar funcionalidades, crea un issue en el repositorio.