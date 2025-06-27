# 🦷 Dentware

Sistema de gestión clínica odontológica desarrollado por el equipo **BrickByBrick**, como parte del curso de Sistemas de Información de la Universidad Católica San Pablo.

## 👥 Autores
Proyecto desarrollado por:
- Roberto Cayro Cuadros
- Fabián Concha Sifuentes
- Mauricio Estefanero Chávez
- Camila Luque Juárez
- Joaquín Pino Zavala

## 📋 Descripción

Dentware es una aplicación de escritorio que permite gestionar la información clínica de pacientes en una consulta odontológica. Su diseño está orientado a brindar una solución práctica, segura e intuitiva para la administración de historiales clínicos, odontogramas, tratamientos, exámenes auxiliares, presupuestos, pagos y más.

## 🚀 Características Principales

- Registro y gestión de pacientes
- Gestión de historia clínica y antecedentes médicos
- Alerta de contraindicaciones médicas importantes
- Registro y visualización de exámenes auxiliares (PDF, imágenes)
- Odontograma digital interactivo
- Creación y seguimiento de tratamientos
- Emisión de presupuestos
- Registro de pagos y saldo pendiente
- Búsqueda de pacientes por DNI o nombre
- Soporte multiplataforma (Windows y Linux)

## 🧠 Tecnologías Utilizadas

- **Lenguaje:** Python 3
- **Framework:** Flask 3.1.1
- **Base de Datos:** PostgreSQL
- **ORM:** SQLAlchemy
- **Frontend:** HTML, CSS, Bootstrap
- **Otros:** Jinja2, Werkzeug

## 📁 Estructura del proyecto
```bash
dentware/
├── app/                          # Módulos principales de la aplicación
│   ├── __init__.py                # Inicializa la aplicación Flask y los blueprints
│   ├── extensions.py              # Extensiones de Flask (ej. SQLAlchemy, Migrate)
│   ├── gen_fake_data.py          # Script para generar datos falsos de prueba
│   ├── importar_procedimientos.py # Carga masiva de procedimientos desde JSON
│   ├── models.py                 # Definición de modelos con SQLAlchemy
│   ├── procedimientos.json       # Datos base con procedimientos odontológicos
│   ├── utils.py                  # Funciones auxiliares reutilizables
│   ├── historia/                 # Módulo de historia clínica (routes, forms)
│   ├── odontograma/              # Módulo del odontograma (routes, forms)
│   ├── sistema/                  # Módulo administrativo (routes, forms)
│   ├── static/                   # Archivos estáticos (CSS, imágenes, JS)
│   └── templates/                # Plantillas HTML (Jinja2)
├── db/                           # Scripts o archivos relacionados a la base de datos
├── venv/                         # Entorno virtual de Python (no incluir en control de versiones)
├── .env                          # Variables de entorno para configuración
├── .gitignore                    # Archivos y carpetas ignoradas por git
├── app.db                        # Base de datos SQLite (solo para desarrollo)
├── config.py                     # Configuración global del sistema
├── README.md                     # Documentación del proyecto
└── requirements.txt              # Lista de dependencias del entorno Python

```
