# OmniBoost Studio — Video Booster Ultra (Universal)

> **Suite de optimización, restauración y masterización cinemática de video.**  
> Desarrollado con el diseño visual oficial de **Tu Tiendita IA** (Sitio web oficial: [tutiendita-ia.store](https://tutiendita-ia.store)).

---

## 🎨 Identidad Visual y Diseño de Marca: "Tu Tiendita IA"

Esta aplicación cuenta con una interfaz gráfica premium de nivel profesional, diseñada bajo los lineamientos estéticos oficiales de **Tu Tiendita IA** ([tutiendita-ia.store](https://tutiendita-ia.store)), plataforma y tienda líder en herramientas, modelos y soluciones de vanguardia en Inteligencia Artificial y producción digital.

El estilo visual **"Noche Tinta Studio"** prescinde de interfaces genéricas o recargadas para ofrecer una experiencia editorial limpia, minimalista y descansada a la vista:
- **Azul Birome (`#1E3C96` / `#2A4FC0`)**: Botones de acción principal y elementos activos.
- **Azul Tinta Profundo (`#16205A` / `#0A1024`)**: Fondo base, encabezado institucional y profundidad estructural.
- **Rosa Malvón (`#E0435C`)**: Acentos destacados, insignias y botones de cancelación controlada.
- **Amarillo Yema (`#FFD23F`)**: Barras de progreso activas, bordes de finalización exitosa y chips destacados.
- **Plata y Papel (`#8B97B0` / `#F6F7FA`)**: Tipografía de alta legibilidad (*Segoe UI Variable*), métricas de rendimiento y contrastes suaves con bordes redondeados (12 px a 16 px).

---

## 📖 Descripción General

**OmniBoost Studio** es una estación de trabajo de escritorio orientada a creadores de contenido, animadores 3D, editores audiovisuales y productores que trabajan con video generado por Inteligencia Artificial.

La aplicación resuelve de raíz las degradaciones más comunes del material audiovisual digital:
1. **Pérdida de nitidez y texturas** causada por compresión pesada de redes sociales o cámaras de gama media.
2. **Banding de color (artefactos en bandas/escalones)** frecuentes en cielos, fondos oscuros y videos sintetizados por modelos generativos (Kling, Sora, Runway, Midjourney).
3. **Ruido electrónico y grano sucio** en tomas con poca luz.
4. **Falta de impacto dinámico** en gamas tonales y contraste.

Todo el procesamiento se realiza de manera **100% local y offline**: ningún cuadro de video sale de tu computadora, no necesitás suscripciones mensuales, no dependés de conexión a internet y no hay costos por minuto de render.

---

## ⚡ Características Principales y Tecnologías

### 1. Filtros Cinemáticos Profesionales
- **Contrast Adaptive Sharpening (FidelityFX CAS)**: Realza microtexturas, poros de la piel, detalles de ropa y bordes finos de manera adaptativa, sin generar los molestos halos blancos ni grano digital que causan los filtros de nitidez tradicionales.
- **Claridad & Micro-contraste (Unsharp Masking multicapa)**: Añade profundidad perceptual y volumen tridimensional entre los objetos en primer plano y el fondo.
- **Denoise Espacio-Temporal Inteligente**: Algoritmo `hqdn3d` adaptativo que limpia el ruido en zonas homogéneas preservando los detalles estáticos y en movimiento.
- **De-banding de Alta Precisión (`gradfun`)**: Elimina el efecto de bandas en degradados sutiles, cielos y sombras sin destruir la nitidez de la toma.
- **Realce Tonal y Perceptual HDR**: Expansión dinámica del color y contraste con preservación estricta de tonos de piel humana.

### 2. 7 Perfiles Preconfigurados (Presets)
1. **🌟 Universal / Equilibrado (Cámaras, Smartphones, Web)**: El perfil estándar todoterreno. Equilibrio perfecto entre nitidez, limpieza y fidelidad para cualquier clip común.
2. **🎬 Cine & Películas Reales (Piel natural, preserva grano 35mm)**: Ajuste analógico conservador que protege el grano orgánico del celuloide y mantiene los tonos de piel sumamente naturales.
3. **🎨 Animación 3D & CGI (Pixar, Disney, Gaming, Unreal Engine)**: Optimizado para renderizados 3D, cinemáticas y estilo Pixar. Resalta la iluminación volumétrica y suaviza las texturas complejas.
4. **⛩️ Anime & Animación 2D (Líneas definidas, colores limpios)**: Maximiza la definición de las líneas entintadas sin ensuciar los planos de color uniforme.
5. **🤖 Videos de IA (Kling, Runway, Sora — Anti-Banding & Denoise)**: Diseñado especialmente para limpiar los artefactos típicos de modelos generativos de video (shimmering, grano errático y bandas tonales).
6. **📼 Restauración & Grano Fuerte (Limpia compresión severa)**: Filtro intensivo para grabaciones antiguas, videos de baja tasa de bits o material con compresión severa.
7. **🎛️ Personalizado**: Desbloquea los deslizadores inferiores para regular manualmente la Nitidez (CAS), Claridad, Reducción de Ruido, De-banding y Realce de Color.

### 3. Resoluciones Inteligentes y Soporte Vertical (9:16)
OmniBoost Studio detecta automáticamente la orientación del archivo original:
- **Mantener resolución original**: No altera las dimensiones, solo aplica los filtros de calidad.
- **Auto-Adaptativo 1080p**: Si el video es horizontal lo procesa a `1920x1080`; si es vertical lo procesa a `1080x1920` sin recortar ni estirar.
- **Auto-Adaptativo 4K UHD**: Si es horizontal escala a `3840x2160`; si es vertical escala a `2160x3840`.
- **Auto-Adaptativo 2K QHD**: `2560x1440` (horizontal) o `1440x2560` (vertical).
- **1080x1920 (9:16 Vertical)**: Ideal para exportar contenido directo para TikTok, Instagram Reels y YouTube Shorts.
- **2160x3840 (9:16 Vertical 4K Ultra HD)**: Máxima calidad para pantallas verticales de última generación.
- **3840x2160 (16:9 4K Ultra HD)** y **2560x1440 (2K QHD)**: Formatos horizontales de pantalla ancha.
- **4K Cinema DCI (`4096x2160`)**: Relación de aspecto panorámica para salas de cine digital.

### 4. Aceleración por Hardware (GPU / CPU)
- **NVIDIA GeForce RTX (NVENC p7 + Spatial/Temporal AQ)**: Utiliza los núcleos dedicados de tu placa NVIDIA RTX con el preset `p7` (máxima calidad disponible en el silicio de codificación) y cuantización adaptativa espacial/temporal.
- **NVIDIA GeForce RTX — HEVC / H.265 (Ultra Calidad 4K)**: Para proyectos que exigen la máxima compresión y pureza en 4K.
- **AMD Radeon — AMF Hardware (RX 6000 / 7000 / 8000 Series)**: Aceleración por hardware dedicada para tarjetas gráficas AMD.
- **CPU / Software Universal (`libx264`)**: Modo seguro por procesador para equipos sin placa de video dedicada.

---

## 🚀 Guía de Uso Paso a Paso

### Opción A: Mejorar un Video Individual
1. **Abrí el programa**: Hacé doble clic en el acceso directo de OmniBoost Studio o en `OmniBoost Studio.exe`.
2. **Seleccioná el archivo**: En la pestaña **"Archivo Único"**, hacé clic en **"Examinar..."** y elegí tu archivo de video. La aplicación leerá al instante su resolución, tasa de cuadros (fps) y duración.
3. **Elegí el Perfil**: En el menú desplegable *Tipo de Video / Perfil*, elegí el preset que mejor se adapte a tu material (por ejemplo, *Universal*, *Animación 3D* o *Videos de IA*).
4. **Configurá la resolución**: Dejá *Mantener resolución original* o seleccioná la resolución deseada.
5. **Elegí tu acelerador**: Si tenés placa NVIDIA, seleccioná *NVIDIA GeForce RTX*; si tenés AMD, seleccioná *AMD Radeon*; si no, dejá *CPU / Software Universal*.
6. **Iniciá el proceso**: Hacé clic en el botón principal **"Mejorar Video"**.
7. **Monitoreá el avance**: La barra Yema te indicará el progreso porcentual y la consola inferior mostrará cada paso técnico. Al finalizar, vas a poder abrir directamente el archivo terminado o la carpeta de destino con un solo clic.

### Opción B: Procesamiento por Lote (Carpeta Completa)
1. Entrá a la pestaña **"Carpeta Completa / Lote"**.
2. Elegí la carpeta donde tenés guardados tus videos.
3. Indicá si querés procesar también subcarpetas marcando la casilla *Incluir subcarpetas (recursivo)*.
4. Seleccioná el perfil y la resolución.
5. Hacé clic en **"Procesar Carpeta"**. La app recorrerá cada video uno a uno sin interrumpir el proceso si algún archivo estuviese dañado.

---

## 📁 Formatos Soportados

- **Formatos de Entrada**: `.mp4`, `.mov`, `.mkv`, `.avi`, `.webm`, `.flv`, `.ts`, `.m4v`, `.mpg`, `.mpeg`.
- **Formato de Salida**: Contenedor `.mp4` universal codificado en H.264 / H.265 con audio estéreo AAC a 320 kbps sin pérdida audible.
- **Nombres de archivo**: Por defecto añade el sufijo `_boosted.mp4` para no sobreescribir tu video original, permitiéndote además renombrarlo si lo deseás.

---

## 📦 Opciones de Instalación y Despliegue

OmniBoost Studio se entrega en dos variantes independientes:
1. **Versión con Instalador (`OmniBoost Studio Instalador 1.0.exe`)**:
   - Asistente guiado de instalación estándar de Windows.
   - Crea accesos directos en el Escritorio y en el Menú Inicio.
   - El ejecutable es nativo (`.exe`), no abre ventanas negras de comando (cmd) y cuenta con su desinstalador estándar en el Panel de Control.
2. **Versión Portable (`OmniBoost Studio Portable.zip`)**:
   - No requiere privilegios de administrador ni instalación en el registro de Windows.
   - Simplemente descomprimí la carpeta en cualquier disco local, pendrive o disco externo y ejecutá `OmniBoost Studio.exe`.
   - Incluye FFmpeg y todas las dependencias autocontenidas dentro de la carpeta `_internal`.

---

## 💻 Requisitos del Sistema

- **Sistema Operativo**: Windows 10 u 11 (64 bits).
- **Procesador**: Intel Core i3 / AMD Ryzen 3 o superior (4 núcleos recomendados).
- **Memoria RAM**: 4 GB mínimo (8 GB recomendados).
- **Placa Gráfica (Opcional pero muy recomendada)**: NVIDIA GeForce GTX 1050 / RTX 2060 / 3060 / 4060 o superior, o AMD Radeon RX 5000 / 6000 / 7000 series.
- **Espacio en Disco**: 400 MB libres para la aplicación más el espacio requerido para los videos exportados.

---

*Desarrollado para la suite creativa de **Tu Tiendita IA** · [https://tutiendita-ia.store](https://tutiendita-ia.store)*
