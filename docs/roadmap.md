# 🗺️ Roadmap — API REST E-commerce Worven

## Fase 1 — Definición del producto ✅ Completada
- Dominio del negocio, requisitos funcionales y no funcionales
- Diagrama de casos de uso
- Historias de usuario HU-01 a HU-07
- MVP definido (ver `definicion-producto.md`)

## Fase 2 — Diseño técnico ✅ Completada
- Diagrama entidad-relación → ver `erd.md`
- Diseño de endpoints de la API → ver `api-endpoints.md`
- Arquitectura del proyecto → ver `arquitectura.md`
- Stack tecnológico confirmado (incluye Wompi en modo sandbox, ver tabla abajo)

## Fase 3 — Setup del entorno (1 día) 🔲 No iniciada
- [ ] Inicializar proyecto Django dentro de `backend/`
- [ ] Entorno virtual (`venv/`)
- [ ] Instalación de dependencias (`requirements.txt`)
- [ ] Estructura de apps (según `arquitectura.md`)
- [ ] Variables de entorno con `.env` (incluye claves de Wompi sandbox)
- [ ] Actualizar `backend/README.md` con instrucciones reales

## Fase 4 — Desarrollo por módulos (3-4 semanas) 🔲 No iniciada
Cada módulo se desarrolla en su propia rama `feature/*`, partiendo de `develop`:
1. Módulo 1: Autenticación y usuarios
2. Módulo 2: Productos y categorías
3. Módulo 3: Carrito de compras
4. Módulo 4: Órdenes y pagos (incluye integración Wompi sandbox + webhook)
5. Módulo 5: Panel de administración

## Fase 5 — Pruebas (3-5 días) 🔲 No iniciada
- [ ] Pruebas unitarias con pytest
- [ ] Pruebas de endpoints con Postman (incluye simular el webhook de Wompi)
- [ ] Corrección de bugs

## Fase 6 — Documentación (2 días) 🔲 No iniciada
- [ ] Documentación automática con Swagger (drf-spectacular)
- [ ] README del backend actualizado
- [ ] Documentar decisiones técnicas

## Fase 7 — Despliegue (2 días) 🔲 No iniciada
- [ ] Deploy en Railway
- [ ] Base de datos PostgreSQL en producción
- [ ] Variables de entorno en producción (incluye claves de Wompi sandbox)

---

## 🛠️ Stack tecnológico

| Capa | Tecnología | Por qué |
|---|---|---|
| Lenguaje | Python 3.11+ | Base |
| Framework | Django 6 | Robusto y muy demandado |
| API | Django REST Framework | Estándar de la industria |
| Autenticación | djangorestframework-simplejwt | JWT es lo que usan las empresas |
| Base de datos | PostgreSQL | Nunca SQLite en portafolio |
| Conexión a BD | psycopg2-binary | Requerido para que Django hable con PostgreSQL |
| CORS | django-cors-headers | Frontend y backend viven en orígenes distintos |
| Pasarela de pagos | Wompi (modo sandbox) | Integración real de pagos sin mover dinero real |
| Documentación | drf-spectacular (Swagger) | Se ve muy profesional |
| Variables de entorno | python-decouple | Buena práctica de seguridad |
| Testing | pytest-django | Estándar |
| Servidor de producción | gunicorn | El servidor de desarrollo de Django no sirve para producción |
| Archivos estáticos en producción | whitenoise | Sirve CSS/imágenes del admin sin servicio aparte |
| Control de versiones | Git + GitHub | Obligatorio |
| Deploy | Railway | Gratis y fácil |

---

## 📋 Marco de trabajo — GitHub Projects (Kanban)

Como son dos personas, trabajan con Kanban directamente en GitHub. Cada tarea es un Issue, cada Issue tiene una rama, y se fusiona con un Pull Request que el compañero revisa.

```
main          ← solo código estable y probado (protegida: PR + 1 aprobación obligatoria)
  └── develop ← rama de integración (protegida: requiere PR)
        └── feature/autenticacion
        └── feature/productos
        └── feature/carrito
        └── feature/ordenes-pagos
        └── feature/panel-admin
```