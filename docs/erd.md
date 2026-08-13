# Diagrama entidad-relación — Worven

![Diagrama ERD de Worven](img/erd-worven.png)
![Diagrama ERD de Worven](img/erd-relacion-worven.png)

# Tablas — Worven
![Diagrama ERD de Worven](img/tablas-worven.png)

Ajustado al MVP: catálogo filtra solo por categoría, con soporte de variantes por talla/color (stock independiente por combinación), y con la integración de pagos vía Wompi (modo sandbox).

## Entidades

### usuarios
| Campo |       Tipo |      Nota |
|---    |---         |---        |
| id_usuario |  PK   | |
| nombre |      texto | |
| apellido |    texto | |
| correo |      texto |     único |
| password |    texto |     hasheado |
| rol |         texto |     cliente / admin |
| direccion |   texto | |
| telefono |    texto | |

### productos
| Campo |       Tipo |      Nota |
|---|---|---|
| id_producto | PK | |
| nombre |      texto | |
| descripcion | texto | |
| precio |      decimal | |
| categoria |   texto |     hombre / mujer / niños |
| imagen_principal|   ImagenField (local) |   Cloudinary en produccion, ver decision abajo |
| activo |      booleano |  para desactivar sin eliminar |
| fecha cracion | fecha | usada pera ordenar por defecto |

### variantes_producto
| Campo | Tipo | Nota |
|---    |---    |---    |
| id_variante | PK | |
| id_producto | FK | |
| talla | texto | |
| color | texto | |
| stock | entero | el stock vive aquí, no en producto |
| sku | texto | único, identifica la combinación exacta |

### carritos
| Campo |       Tipo |      Nota |
|---|---|---|   
| id_carrito |  PK | |
| id_usuario |  FK |        relación 1 a 1 con usuarios |

### item_carritos
| Campo |        Tipo |      Nota |
|---|---|---|
| id_item_carrito | PK | |
| id_carrito |      FK | |
| id_variante |     FK | |
| cantidad |        entero | |

### ordenes
| Campo |            Tipo |     Nota |
|---|---|---|
| id_orden |         PK | |
| id_usuario |       FK | |
| direccion_envio |  texto | |
| ciudad_envio |     texto | |
| telefono_envio |   texto | |
| estado |           texto |   Pendiente / Enviado / Entregado / Cancelado — solo del envío |
| estado_pago |      texto |    Pendiente / Aprobado / Rechazado |
| metodo_pago |      texto |    ej: tarjeta, PSE |
| referencia_pago |  texto |    id de transacción que devuelve Wompi |
| codigo_rastreo |   texto |    lo asigna la empresa de envío |
| total | decimal | |
| fecha | fecha | |

### item_ordenes
| Campo |           Tipo |      Nota |
|---|---|---|
| id_item_orden |   PK | |
| id_orden |        FK | |
| nombre_producto | texto |     congelado al momento de la compra |
| sku  |            texto |     congelado |
| talla |           texto |     congelado |
| color |           texto |     congelado |
| precio_unitario | decimal |   congelado |
| cantidad |        entero | |

## Relaciones

| Relación | Cardinalidad | FK |
|---|---|---|
| usuarios — carritos | 1 a 1 | carritos.id_usuario |
| usuarios — ordenes | 1 a muchos | ordenes.id_usuario |
| productos — variantes_producto | 1 a muchos | variantes_producto.id_producto |
| carritos — item_carritos | 1 a muchos | item_carritos.id_carrito |
| variantes_producto — item_carritos | 1 a muchos | item_carritos.id_variante |
| ordenes — item_ordenes | 1 a muchos | item_ordenes.id_orden |

### mensajes_contacto
- id, nombre, correo, mensaje, fecha_creacion

### suscriptores
- id, correo (único), fecha_creacion

## Decisiones de diseño registradas
- El envío no puede pasar a "Enviado" si `estado_pago` no es "Aprobado" — evita despachar pedidos no pagados.
- `create_superuser` asigna automáticamente `rol='admin'`, para que un solo comando dé acceso tanto al panel de Django Admin como a los endpoints de administrador de la API.
- `mensajes_contacto` y `suscriptores` no tienen relación con `usuarios` — cualquiera puede enviarlos sin estar autenticado ni tener cuenta.

- **Sí existe tabla de variantes** (`variantes_producto`): un producto agrupa la info general (nombre, foto, precio, categoría), y cada combinación talla+color es una variante con su propio stock y SKU — evita duplicar productos idénticos por cada talla/color.
- **Imágenes:** `ImageField` local durante desarrollo (`MEDIA_ROOT`/`MEDIA_URL`); se evaluará migrar a Cloudinary en producción, sin cambiar la lógica de negocio, solo el backend de almacenamiento.
- **item_ordenes no tiene FK a productos** — los datos se copian ("congelan") al momento de la compra, para que cambios futuros en el producto (precio, desactivación) no afecten órdenes ya realizadas.
- **estado y estado_pago están separados** — el envío y el pago tienen ciclos de vida independientes desde que se integró Wompi.