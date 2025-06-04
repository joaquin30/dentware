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
├── app/                # Módulos principales de la aplicación
│   ├── models/         # Modelos SQLAlchemy
│   ├── templates/      # Plantillas HTML (Jinja2)
│   ├── static/         # Recursos estáticos (CSS, JS, imgs, PDF)
│   └── routes/         # Rutas y vistas
├── migrations/         # Archivos de migración de la base de datos
├── config.py           # Configuración del sistema
├── run.py              # Script de arranque
└── requirements.txt    # Dependencias del proyecto
```
