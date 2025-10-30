# Intervalos de carrera

Aplicación web híbrida orientada a planificar, ejecutar y registrar entrenamientos de carrera por intervalos, optimizada para funcionar tanto en escritorio como en móviles y con soporte offline mediante PWA.

## Características principales

- **Cronómetro de intervalos** con transición automática entre fases, resumen de etapa actual, barra de progreso y controles rápidos para pausar, reanudar, saltar una fase o avanzar 10 segundos.
- **Monitor cardíaco Web Bluetooth** integrado que conecta con bandas compatibles, traza el histórico en un lienzo `canvas` y colorea el estado según el rango objetivo de la etapa activa.
- **Editor visual de workouts** en un panel modal: añade, reordena, duplica y elimina etapas o subfases (split) con validaciones inmediatas y resumen de duración total.
- **Gestor de sesiones** con múltiples entrenamientos nombrados, con duplicado y borrado seguro, más selector emergente accesible desde el título de la tarjeta principal.
- **Persistencia en localStorage** tanto de la configuración aplicada como de borradores, para recuperar sesiones al reabrir la app.
- **Internacionalización automática**: detecta el idioma del navegador (es/en) y cambia textos estáticos y mensajes dinámicos sin recargar ni duplicar lógica.
- **Importación y exportación JSON** de workouts para respaldarlos o compartirlos, con validación y feedback contextual.
- **PWA lista para instalación** con `manifest.webmanifest`, service worker de caché estática/dinámica y botón `Instalar app` controlado vía `beforeinstallprompt`.

## Estructura e implementación

- `index.html`: archivo único con estructura HTML, estilos embebidos y la mayor parte de la lógica en JavaScript vanilla. Contiene:
  - Declaración de temas CSS y layout responsivo.
  - Lógica de internacionalización (`t()`), generación de workouts por defecto y helpers de UI.
  - Cronómetro, validaciones de etapas, reproducción de audio y gestión de rangos cardíacos.
  - Renderizado dinámico de formularios e interacción con el monitor HR.
  - Registro del service worker, manejadores de instalación PWA y detección de `beforeinstallprompt`.
- `hrm.html`: versión reducida del panel de frecuencia cardíaca, útil para pruebas aisladas (no se modifica en las tareas recientes).
- `manifest.webmanifest`: define nombre, `short_name`, tema, descripción e iconos `192x192` y `512x512` necesarios para las tiendas y banners móviles. Empieza en `.` para mantener las rutas relativas.
- `service-worker.js`: caches
  - Rutas críticas (`./`, `./index.html`, `./manifest.webmanifest`, `./hrm.html`).
  - Responde con caché primero y reintenta `fetch` con actualización silenciosa; ante fallo devuelve `index.html`.
  - Implementa limpieza de versiones viejas en `activate`.
- `icons/icon-192.png` y `icons/icon-512.png`: recursos ligeros generados programáticamente que respetan la identidad cromática del dashboard.

## Flujo de instalación PWA

1. Al cargar `index.html`, se registra el `service-worker.js` (si el navegador lo soporta).
2. En navegadores que cumplen los criterios (HTTPS y engagement), el evento `beforeinstallprompt` se intercepta, se guarda la referencia y se muestra el botón “Instalar app”.
3. El usuario pulsa el botón y se ejecuta `prompt()`. Tras la elección, el botón vuelve a ocultarse. El evento `appinstalled` asegura que no se ofrezca nuevamente si la app ya está instalada.

## Desarrollo y pruebas

- No se utiliza framework; basta un servidor estático (p.ej. `npx serve marta/`) para probar en escritorio o móvil.
- Para depurar el monitor HR, Chrome requiere contexto seguro (HTTPS o `localhost`).
- Las pruebas de PWA en Android pueden hacerse con Chrome DevTools → Application → Manifest, forzando el `beforeinstallprompt` desde `Lighthouse` o `Application > Service Workers`.

## Próximos pasos sugeridos

- Añadir control explícito para deshacer cambios en workouts antes de guardar.
- Guardar un registro histórico de ritmo cardíaco por sesión usando IndexedDB para análisis posterior.
- Integrar notificaciones o vibración para cambios de etapa cuando la pantalla está bloqueada.
