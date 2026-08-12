# Worven — Backend

API REST para Worven, tienda de ropa urbana. Construida con Django + Django REST Framework.

## Requisitos previos

- Python 3.11+
- PostgreSQL instalado y corriendo localmente

## Instalación

1. Clona el repositorio y entra a la carpeta del backend:
   \`\`\`bash
   git clone https://github.com/DeiberBedoya/Worven.git
   cd worven/backend
   \`\`\`

2. Crea y activa el entorno virtual:
   \`\`\`bash
   python -m venv venv
   source venv/Scripts/activate   # Windows (Git Bash)
   # o .\venv\Scripts\Activate.ps1   # Windows (PowerShell)
   \`\`\`

3. Instala las dependencias:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. Crea la base de datos en PostgreSQL:
   \`\`\`sql
   CREATE DATABASE worven_db;
   \`\`\`

5. Copia el archivo de variables de entorno y complétalo con tus datos:
   \`\`\`bash
   cp .env.example .env
   \`\`\`

6. Corre las migraciones:
   \`\`\`bash
   python manage.py migrate
   \`\`\`

7. Levanta el servidor:
   \`\`\`bash
   python manage.py runserver
   \`\`\`

## Documentación de la API

Con el servidor corriendo, la documentación interactiva (Swagger) está disponible en:
\`\`\`
http://127.0.0.1:8000/api/docs/
\`\`\`

## Variables de entorno

Ver `.env.example` para la lista completa de variables necesarias.