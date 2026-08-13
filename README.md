# 👕 Worven

Tienda online de ropa urbana enfocada en jóvenes adultos. El cliente navega el catálogo, agrega productos al carrito (eligiendo talla y color), realiza el pago con Wompi y hace seguimiento del estado de su pedido. El sistema contempla dos tipos de usuario: clientes y administradores.

## 🛠️ Stack tecnológico

**Frontend**
- HTML5 / CSS3

**Backend**
- Python 3.11+ · Django 6 · Django REST Framework
- Autenticación JWT (access + refresh) con `djangorestframework-simplejwt`
- PostgreSQL
- Pasarela de pagos: Wompi (modo sandbox)
- Documentación de la API con Swagger (`drf-spectacular`)
- Panel de administración: Django Admin + `django-jazzmin`
- Imágenes: `ImageField` local en desarrollo, con Cloudinary planeado para producción
- Deploy: Railway

## ✨ Funcionalidades

### Ya implementadas (frontend)
- Página de inicio
- Catálogo de camisetas
- Colecciones
- Sobre Worven
- Contáctanos
- Políticas

### En desarrollo (backend)
- Registro / inicio de sesión con JWT
- Catálogo con productos y variantes (talla, color, stock por combinación), filtro por categoría y ordenamiento
- Carrito de compras
- Proceso de pago y órdenes (Wompi sandbox)
- Panel administrativo — gestión de inventario, pedidos y usuarios (Django Admin)
- Formulario de contacto y suscripción a newsletter

## 📊 Estado del proyecto

Ver el roadmap completo y el detalle de cada fase en [`docs/roadmap.md`](./docs/roadmap.md). Actualmente en **Fase 3 — Setup del entorno**.

## 👩‍💻 Desarrollado por
- [Dahiana Gaviria](https://github.com/DahianaGL)
- [Deiber Bedoya](https://github.com/DeiberBedoya)

## 🚀 Cómo ejecutar el proyecto localmente

### Frontend
```bash
# 1. Clonar el repositorio
git clone https://github.com/DeiberBedoya/Worven.git

# 2. Entrar a la carpeta del frontend
cd Worven/frontend

# 3. Abrir index.html en el navegador
```

### Backend
Instrucciones detalladas de instalación en [`backend/README.md`](./backend/README.md).

## 📁 Estructura del proyecto
\`\`\`
worven/
├── frontend/      # Sitio web (HTML + CSS)
└── backend/       # API REST (Django + DRF) — próximamente
└── docs/ # Definición de producto, ERD, endpoints, arquitectura y roadmap

## 📄 Documentación técnica

- [`docs/definicion-producto.md`](./docs/definicion-producto.md) — historias de usuario y MVP
- [`docs/erd.md`](./docs/erd.md) — diagrama entidad-relación
- [`docs/api-endpoints.md`](./docs/api-endpoints.md) — diseño de la API
- [`docs/arquitectura.md`](./docs/arquitectura.md) — estructura del proyecto y decisiones técnicas
- [`docs/roadmap.md`](./docs/roadmap.md) — plan de trabajo por fases
\`\`\`