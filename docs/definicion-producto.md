# Definición del producto — Worven

## ¿Qué vende la tienda?

Camisetas de ropa urbana, dirigidas principalmente a jóvenes adultos. El cliente escoge, paga y recibe el envío, con opciones de talla y color. El sistema es usado por dos tipos de usuario: **clientes** y **administradores** de la tienda.

## Requisitos funcionales

### Módulo de usuario
- Registro
- Iniciar / cerrar sesión
- Editar perfil
- El administrador puede ver todos los usuarios

### Módulo de carrito
- Agregar producto al carrito
- Modificar cantidad
- Eliminar / vaciar carrito

### Módulo de productos
- Catálogo de camisetas
- Filtro por categoría
- Ordenamiento por precio (menor a mayor / mayor a menor) y por fecha de lanzamiento
- Categorías

### Módulo de pagos
- Método de pago (Wompi, modo sandbox)
- Estado del pedido (envío) y estado del pago (separados)
- Código de rastreo entregado por la empresa de envío
- Cancelar pedido

### Módulo administrativo
- Inventario
- Ver pedidos
- Cambiar estado del pedido
- Ver lista de usuarios registrados
- Gestionado desde el Admin de Django (con `django-jazzmin`), no requiere frontend propio

### Módulo de contacto
- Formulario de contacto (mensaje libre)
- Suscripción a newsletter (solo correo, sin duplicados)
- Sin autenticación — cualquiera puede usarlos
- Visibles para el administrador desde el Admin de Django

## Requisitos no funcionales

| Atributo | Requisito |
|---|---|
| Rendimiento | API con respuesta < 200 ms |
| Seguridad | HTTPS / JWT / bcrypt |
| Disponibilidad | 99.9% de tiempo activo |
| Usabilidad | Diseño responsive |

## Diagrama de casos de uso

Ya definido — actores Cliente y Administrador, con acciones como registrarse, ver catálogo, gestionar carrito, realizar pedido, gestionar productos, cambiar estado de pedidos, entre otras.

---

## Historias de usuario

### HU-01 — Registro de cuenta nueva
**Como** cliente nuevo, **quiero** registrarme con mi nombre, correo y contraseña, **para** tener una cuenta y poder guardar mis pedidos e historial de compras.

**Criterios de aceptación:**
1. El sistema no permite registrar dos cuentas con el mismo correo electrónico.
2. La contraseña debe tener un mínimo de 8 caracteres.
3. Al registrarse exitosamente, el sistema devuelve un `access` y un `refresh` token JWT.
4. Si el correo ya existe, el sistema muestra el mensaje "Este correo ya está registrado".
5. Al crear un superusuario de Django (createsuperuser), su rol se asigna automáticamente como "admin".

### HU-02 — Catálogo y filtros de ropa
**Como** cliente, **quiero** ver el catálogo de camisetas y filtrarlas por categoría, **para** encontrar rápidamente la camiseta que se adapte a mi estilo.

> Nota: la HU original mencionaba filtro por talla, color y categoría, pero el MVP recorta esto a **solo categoría** para la v1. Se agregó ordenamiento por precio y fecha como funcionalidad adicional.

**Criterios de aceptación:**
1. El catálogo muestra mínimo 12 productos por página, con foto, nombre y precio.
2. Al aplicar el filtro por categoría, solo aparecen productos de esa categoría.
3. Si no hay productos con el filtro aplicado, aparece el mensaje "No hay productos disponibles".
4. El catálogo puede ordenarse por precio (ambos sentidos) o por fecha de lanzamiento (por defecto).

### HU-03 — Gestión de carrito de compras
**Como** cliente, **quiero** agregar, modificar o eliminar camisetas en mi carrito, **para** preparar mi orden antes de realizar el pago.

**Criterios de aceptación:**
1. Al agregar un producto al carrito, el contador de items se actualiza.
2. Puedo cambiar la cantidad de un producto desde el carrito.
3. Al eliminar un producto, el total del carrito se recalcula automáticamente (calculado en vivo, no almacenado).
4. El carrito persiste aunque el cliente cierre sesión y vuelva a entrar.

### HU-04 — Proceso de pago y pedido
**Como** cliente, **quiero** realizar el pago de mi carrito y registrar mis datos de envío, **para** asegurar la compra de mis camisetas y recibir el paquete en mi casa.

> Actualizado: el pago se procesa con **Wompi en modo sandbox** (pasarela real, sin dinero real de por medio) — ya no es un checkout simulado sin ninguna integración.

**Criterios de aceptación:**
1. El sistema solicita dirección, ciudad y teléfono antes de confirmar el pedido.
2. Al confirmar el pago como **aprobado**, el stock de cada producto se descuenta automáticamente.
3. El cliente recibe un número de orden único como confirmación del pedido.
4. Si un producto se agotó entre agregar al carrito y pagar, el sistema avisa antes de continuar.

### HU-05 — Gestión de inventario (CRUD)
**Como** administrador, **quiero** crear un producto y agregarle variantes (talla, color y stock), y poder editarlos, **para** mantener el catálogo de la tienda siempre actualizado.

> Actualizado: el producto (nombre, descripción, precio, categoría, foto) y sus variantes (talla, color, stock) ahora son entidades separadas — un mismo producto puede tener varias combinaciones de talla/color, cada una con su propio stock.

**Criterios de aceptación:**
1. El administrador puede crear un producto nuevo con nombre, precio, categoría y foto, y agregarle una o más variantes (talla, color, stock).
2. El sistema no permite guardar un producto con precio en cero, ni una variante con stock negativo.
3. Al editar un producto o una variante, los cambios se reflejan inmediatamente en el catálogo.
4. Al desactivar un producto, deja de aparecer en el catálogo sin eliminarse de la base de datos (sus variantes permanecen asociadas).

### HU-06 — Control y cambios de estado de pedidos
**Como** administrador, **quiero** ver todos los pedidos realizados y cambiar el estado de su envío, **para** gestionar la logística de manera eficiente.

> Actualizado: el estado del **envío** (Pendiente/Enviado/Entregado) ahora es independiente del estado del **pago** (Pendiente/Aprobado/Rechazado), gestionado por Wompi.

**Criterios de aceptación:**
1. El panel muestra todos los pedidos con número de orden, cliente, total y estado actual.
2. El administrador puede filtrar pedidos por estado de envío: Pendiente, Enviado, Entregado.
3. Al cambiar el estado, el cambio queda registrado con fecha y hora.
4. El sistema no permite retroceder el estado (ej: de "Enviado" a "Pendiente").
5. Al marcar como "Enviado", el administrador ingresa el código de rastreo entregado por la empresa de envío.
6. No se puede marcar un pedido como "Enviado" si `estado_pago` no es "Aprobado".

### HU-07 — Reporte de ventas básico
**Como** administrador, **quiero** ver el reporte de las ventas realizadas, **para** analizar los ingresos del negocio.

> **Fuera del MVP** — se pospone a una versión futura (ver sección de exclusiones).

---

## Definición del MVP

### ✅ Lo que SÍ entra en la primera versión

**Módulo usuarios**
- Registro básico (nombre, correo, contraseña)
- Inicio de sesión seguro con JWT (`access` + `refresh`)
- Cerrar sesión
- Editar nombre y dirección del perfil

**Módulo productos**
- API que devuelve productos reales desde la base de datos
- Filtrar por categoría (Hombre / Mujer / Niños)
- Ordenar por precio o fecha de lanzamiento
- Ver detalle del producto
- CRUD completo de productos para el administrador

**Módulo carrito**
- Agregar productos al carrito con talla y cantidad
- Modificar cantidad de un item
- Eliminar productos del carrito o vaciarlo

**Módulo pagos/órdenes**
- Registrar datos de envío (dirección, ciudad, teléfono)
- Crear orden
- Procesar el pago con **Wompi en modo sandbox** (pasarela real, sin dinero real de por medio)
- Descontar stock automáticamente una vez el pago sea confirmado como aprobado
- Cancelar pedido si no fue despachado
- El cliente puede ver el **estado actual** del pedido (Pendiente/Enviado/Entregado) — no verá un historial detallado ni podrá rastrear el envío dentro del sistema; en su lugar, recibe un **código de rastreo** entregado por la empresa de envío, quien se encarga del seguimiento

**Módulo administrativo**
- Ver todos los pedidos
- Cambiar el estado del envío: Pendiente / Enviado / Entregado (bloqueado si el pago no está aprobado)
- Gestión de inventario (crear, editar, desactivar)
- Ver lista de usuarios registrados
- Implementado con Admin de Django + `django-jazzmin`, sin frontend propio

**Módulo de contacto**
- Formulario de contacto (nombre, correo, mensaje)
- Suscripción a newsletter (correo único, sin duplicados)
- Visible para el administrador desde el Admin de Django

### ❌ Lo que NO entra en esta versión

**Pagos**
- Pagos por PSE integrado fuera de Wompi
- Opciones de financiación en cuotas
- Procesamiento de pagos con dinero real (solo modo sandbox/pruebas)

**Productos**
- Filtros avanzados de catálogo
- Búsqueda por múltiples colores, tallas y precios a la vez
- Filtro combinado por talla y/o color — el catálogo filtra solo por categoría

**Reportes de venta**
- Reporte de ventas básico completo (HU-07)
- Gráficos de ventas por mes
- Ranking de productos más vendidos
- Gráficos complejos o carritos abandonados