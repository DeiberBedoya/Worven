# Arquitectura del proyecto — Worven

## Estructura del monorepo

\`\`\`
worven/
├── frontend/            # sitio estático (HTML + CSS) — completo
├── docs/                 # este directorio
├── backend/               # Django + DRF
└── README.md
\`\`\`

## Estructura de backend/

\`\`\`
backend/
├── config/               # settings, urls raíz, wsgi/asgi
├── core/                  # código compartido: permisos, paginación
├── usuarios/               # app base — auth y perfil
├── productos/               # app base — catálogo
├── carrito/                  # depende de usuarios + productos
├── ordenes/                    # depende de usuarios + carrito (incluye integración Wompi)
├── contacto/                   # app independiente — mensajes y newsletter, sin dependencias
├── venv/
├── .env
├── manage.py
└── requirements.txt
\`\`\`

Cada app de negocio sigue la misma estructura interna:
\`\`\`
nombre_app/
├── models.py         # tablas del ERD que le corresponden
├── serializers.py    # conversión modelo ↔ JSON
├── views.py          # lógica de los endpoints
├── urls.py           # rutas de esta app
├── admin.py          # registro en el panel admin de Django
├── apps.py
├── tests.py
└── migrations/
\`\`\`

## Grafo de dependencias entre apps

\`\`\`
usuarios (base)        productos (base)        contacto (independiente)
      \\                    /
       \\                  /
          carrito (depende de ambas)
              │
              ▼
          ordenes (depende de usuarios + carrito)
\`\`\`

`contacto` no depende de ninguna otra app ni ninguna otra app depende de ella — puede desarrollarse en cualquier momento, en paralelo con cualquier oleada.

Orden recomendado de desarrollo, siguiendo las flechas:
1. `usuarios`
2. `productos` (puede ir en paralelo con usuarios)
3. `carrito`
4. `ordenes`
5. `contacto` (sin restricción de orden, se acomoda donde haya disponibilidad)

## Por qué existe core/

Código usado por más de una app (ej. la regla de permisos "solo admin") vive en `core/` para no duplicarlo en cada app — principio de alta cohesión / bajo acoplamiento.

## Panel de administración

El módulo administrativo no tiene una app propia ni frontend dedicado — se implementa registrando los modelos de `usuarios`, `productos` y `ordenes` en el Admin nativo de Django, personalizado visualmente con `django-jazzmin`. Vive en la ruta `/admin/`, separado del sitio público y de la API REST.

## Variables de entorno (`.env`)

Agrupadas por propósito — todas documentadas sin valores reales en `.env.example`:
- **Base de datos:** credenciales de PostgreSQL
- **Django:** `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
- **Wompi:** `WOMPI_PUBLIC_KEY`, `WOMPI_PRIVATE_KEY`, `WOMPI_EVENTS_SECRET`