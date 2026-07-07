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
usuarios (base)        productos (base)
      \\                    /
       \\                  /
          carrito (depende de ambas)
              │
              ▼
          ordenes (depende de usuarios + carrito)
\`\`\`

Orden recomendado de desarrollo, siguiendo las flechas:
1. `usuarios`
2. `productos` (puede ir en paralelo con usuarios)
3. `carrito`
4. `ordenes`

## Por qué existe core/

Código usado por más de una app (ej. la regla de permisos "solo admin") vive en `core/` para no duplicarlo en cada app — principio de alta cohesión / bajo acoplamiento.