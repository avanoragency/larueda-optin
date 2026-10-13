# Landings de opt-in y reseña — La Rueda (7 sedes)

Cada carpeta de `sedes/` es **una página completa e independiente** (un solo archivo `index.html`, sin dependencias externas salvo las tipografías de Google). Se publica como la raíz de su propio subdominio.

## Qué publicar y dónde

| Carpeta | Sede | Subdominio sugerido |
|---|---|---|
| `calle-170` | Jumbo 170 | `calle170.larueda.co` |
| `lagartos` | Primax Lagartos | `lagartos.larueda.co` |
| `calle-80` | Jumbo 80 | `calle80.larueda.co` |
| `suba` | Avenida Suba | `suba.larueda.co` |
| `hayuelos` | Jumbo Hayuelos | `hayuelos.larueda.co` |
| `quito` | Av. Quito | `quito.larueda.co` |
| `puente-aranda` | Puente Aranda | `puentearanda.larueda.co` |

Pasos por cada sede:
1. Crear el subdominio (registro DNS apuntando al hosting).
2. Subir `index.html` de esa carpeta como página de inicio del subdominio.
3. Verificar que abre con HTTPS desde un celular.

(Los nombres de subdominio son una sugerencia: cortos, en minúsculas, sin tildes. Una vez impresos en un QR no conviene cambiarlos.)

## Antes de imprimir los QR

1. **Conectar el guardado del registro.** Cada página tiene un bloque `CONFIG` al inicio del `<script>` con `registroUrl: ''`. Mientras esté vacío, el formulario muestra "No pudimos guardar tu registro". Hay que poner ahí la URL del webhook que guarda el consentimiento (nombre, teléfono, sede, texto de la autorización, fecha). Esa información es la prueba de opt-in ante Meta.
2. **Política de datos.** Reemplazar el enlace `https://larueda.co/politica-de-privacidad` (marcado en amarillo en pantalla) por la URL real de la política de tratamiento de datos.
3. **Revisar el texto legal** de la autorización (responsable, finalidad, derechos).
4. **Sedes sin reseña:** `lagartos` y `suba` solo tienen opt-in porque aún no tienen Perfil de Empresa en Google. Cuando lo tengan, se agrega su Place ID y se regenera la página (ver más abajo).

## QR

El QR de cada sede debe apuntar a **la URL de su subdominio**, por ejemplo `https://quito.larueda.co/`. Puede añadirse `?utm_source=qr&utm_medium=sede` para medir los escaneos.

## Cómo se generan las páginas (si hay que cambiar algo)

El código fuente está en https://github.com/avanoragency/larueda-optin:
- `template.html`: la plantilla única (textos, colores, sedes y Place IDs).
- `build.py`: genera las páginas de `sedes/` (`python build.py`).

Para cambiar un texto o añadir un Place ID: editar `template.html`, correr `python build.py` y volver a subir las páginas.
