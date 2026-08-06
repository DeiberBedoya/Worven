# Diseño de endpoints — API Worven

## Usuarios / Auth

| Método | Ruta                 | Descripción | Quién puede usarlo | Request body                 | Respuesta   |
|---   |---                     |---          |---                 |---                           |---          |
| POST | `/api/auth/registro/`  | Crear cuenta | Cualquiera        | `{nombre, correo, password}` | `{id_usuario, access, refresh}` |
| POST | `/api/auth/login/`     | Iniciar sesión | Cualquiera      | `{correo, password}`         | `{access, refresh}`              |
| POST | `/api/auth/refresh/`   | Renovar el access token sin volver a pedir usuario/contraseña | Cualquiera con un refresh token válido | `{refresh}` | `{access}` |
| POST | `/api/auth/logout/`    | Cerrar sesión | Usuario autenticado | —                           | —                     |
| GET  | `/api/usuarios/me/`    | Ver mi perfil | Usuario autenticado | —                         | `{id_usuario, nombre, apellido, correo, direccion, telefono}` |
| PATCH | `/api/usuarios/me/`   | Editar mi perfil | Usuario autenticado | `{nombre?, direccion?, telefono?}` | `{id_usuario, nombre, ...}` |
| GET | `/api/usuarios/`        | Listar todos los usuarios | Solo admin | —                      | `[{id_usuario, nombre, apellido, correo, rol, direccion, telefono}, ...]` |

## Productos

| Método | Ruta | Descripción | Quién puede usarlo | Request body | Respuesta |
|---|---|---|---|---|---|
| GET | `/api/productos/?categoria=hombre&ordering=precio` | Listar catálogo, cada producto incluye sus variantes | Cualquiera | — | `[{id_producto, nombre, descripcion, precio, categoria, imagen_principal, activo, variantes: [{id_variante, talla, color, stock, sku}, ...]}, ...]` |
| GET | `/api/productos/{id}/` | Ver detalle de un producto con sus variantes | Cualquiera | — | `{id_producto, nombre, descripcion, precio, categoria, imagen_principal, activo, variantes: [...]}` |
| POST | `/api/productos/` | Crear producto (sin variantes todavía) | Solo admin | `{nombre, descripcion, precio, categoria, imagen_principal}` | `{id_producto, nombre, ...}` |
| PATCH | `/api/productos/{id}/` | Editar producto existente | Solo admin | `{nombre?, precio?, ...}` | `{id_producto, nombre, ...}` |
| PATCH | `/api/productos/{id}/desactivar/` | Desactivar sin eliminar | Solo admin | — | `{id_producto, activo: false}` |
| POST | `/api/productos/{id}/variantes/` | Agregar una variante (talla/color/stock) a un producto | Solo admin | `{talla, color, stock, sku}` | `{id_variante, talla, color, stock, sku}` |
| PATCH | `/api/productos/variantes/{id}/` | Editar una variante existente (ej. actualizar stock) | Solo admin | `{talla?, color?, stock?}` | `{id_variante, talla, color, stock, sku}` |

**Parámetro `ordering`:** acepta `precio` (menor a mayor), `-precio` (mayor a menor) o `-fecha_creacion` (más reciente primero, valor por defecto si no se especifica). El filtro sigue siendo únicamente por categoría — no se combina con talla ni color en esta versión.

## Carritos

| Método | Ruta | Descripción | Quién puede usarlo | Request body | Respuesta |
|---|---|---|---|---|---|
| GET | `/api/carritos/me/` | Ver mi carrito | Usuario autenticado | — | `{id_carrito, items: [{id_item_carrito, id_producto, nombre, precio, cantidad, subtotal}, ...], total}` |
| POST | `/api/carritos/items/` | Agregar un producto al carrito | Usuario autenticado | `{id_producto, cantidad}` | `{id_item_carrito, id_variante, cantidad, subtotal}` |
| PATCH | `/api/carritos/items/{id}/` | Modificar cantidad de un item | Usuario autenticado | `{cantidad}` | `{id_item_carrito, cantidad, subtotal}` |
| DELETE | `/api/carritos/items/{id}/` | Eliminar un producto del carrito | Usuario autenticado | — | — |
| DELETE | `/api/carritos/items/` | Vaciar el carrito completo | Usuario autenticado | — | — |

## Órdenes

| Método | Ruta | Descripción | Quién puede usarlo | Request body | Respuesta |
|---|---|---|---|---|---|
| POST | `/api/ordenes/` | Crear orden (aún sin pagar) | Usuario autenticado | `{direccion_envio, ciudad_envio, telefono_envio}` | `{id_orden, estado: "Pendiente", estado_pago: "Pendiente", total, items: [...]}` |
| POST | `/api/ordenes/{id}/pagar/` | Iniciar el pago con Wompi (sandbox) | Usuario autenticado (dueño) | `{metodo_pago}` | `{referencia_pago, url_checkout}` |
| POST | `/api/webhooks/wompi/` | Wompi confirma el resultado del pago | Nadie directamente — validado por firma, no por JWT | Payload que envía Wompi | `200 OK` — actualiza `estado_pago`, descuenta stock si fue aprobado |
| GET | `/api/ordenes/` | Listar órdenes (cliente ve las suyas, admin todas) | Usuario autenticado | — | `[{id_orden, estado, estado_pago, total, fecha}, ...]` |
| GET | `/api/ordenes/{id}/` | Ver detalle de una orden específica | Usuario autenticado (dueño) o admin | — | `{id_orden, direccion_envio, ciudad_envio, telefono_envio, estado, estado_pago, codigo_rastreo, total, fecha, items: [...]}` |
| PATCH | `/api/ordenes/{id}/estado/` | Cambiar el estado del envío — no permite pasar a "Enviado" si `estado_pago` no es "Aprobado", ni retroceder estados | Solo admin | `{estado, codigo_rastreo?}` | `{id_orden, estado, codigo_rastreo}` |
| PATCH | `/api/ordenes/{id}/cancelar/` | Cancelar orden (solo si no fue despachada) | Usuario autenticado (dueño) | — | `{id_orden, estado: "Cancelado"}` |

## Contacto y Newsletter

| Método | Ruta | Descripción | Quién puede usarlo | Request body | Respuesta |
|---|---|---|---|---|---|
| POST | `/api/contacto/` | Enviar mensaje desde el formulario de contacto | Cualquiera | `{nombre, correo, mensaje}` | `{id, confirmacion}` |
| POST | `/api/newsletter/` | Suscribirse al newsletter | Cualquiera | `{correo}` | `{confirmacion}` — error si el correo ya está suscrito |

## Fuera del MVP

- **Reportes de ventas (HU-07)** — se pospone a una versión futura, según lo definido en el MVP.
- **Filtro combinado por talla y color** — el catálogo filtra solo por categoría; combinar múltiples filtros a la vez queda fuera de esta versión.