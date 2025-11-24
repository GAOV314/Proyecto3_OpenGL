# Proyecto #3 Graficas de la Computación

## Descripción
Este proyecto es un diorama 3D creado con OpenGL en Python, utilizando Pygame para la gestión de ventanas y eventos. El diorama presenta una escena con múltiples modelos 3D posicionados de manera coherente, simulando un entorno temático con iluminación, shaders personalizados y un skybox.

## Requisitos
- **Python 3.8+**
- **Librerías necesarias**:
  - pygame
  - PyOpenGL
  - numpy
  - pyglm
  - colorama
  - click

Todas las dependencias están incluidas en el entorno virtual `venv32/`.

## Instalación y Ejecución
1. Asegúrate de tener Python instalado.
2. Activa el entorno virtual:
   ```
   venv32\Scripts\activate  # En Windows
   ```
3. Ejecuta el programa principal:
   ```
   python RendererOpenGL2025.py
   ```

## Funciones y Características
- **Modelos 3D**: Carga y renderizado de modelos OBJ con texturas automáticas desde archivos MTL.
- **Shaders personalizados**: Vertex y fragment shaders para efectos visuales avanzados (iluminación, deformaciones, patrones procedurales).
- **Skybox**: Entorno 3D infinito usando imagen 360 equirectangular.
- **Iluminación**: Luz puntual móvil con parámetros ajustables.
- **Cámara orbital**: Movimiento de cámara con mouse y teclado para orbitar alrededor de los modelos.
- **Interactividad**: Cambio entre modelos, alternancia de modos (wireframe/fill), ajuste de efectos en tiempo real.

## Controles del Programa
### Cambio de Modelos
- **TAB**: Cambia al siguiente modelo en la escena.

### Cámara Orbital
- **Mouse Click + Arrastrar**: Rota la cámara horizontal y verticalmente alrededor del modelo.
- **Scroll Mouse**: Zoom in/out.
- **Flechas ← →**: Rotación horizontal.
- **Flechas ↑ ↓**: Rotación vertical.
- **+ / -**: Zoom.

### Shaders
- **1**: Fragment Shader - Basic Lighting
- **2**: Fragment Shader - Rainbow/Gradient
- **3**: Fragment Shader - Cosmic Shader (Galaxia)
- **4**: Fragment Shader - Procedural Pattern
- **7**: Vertex Shader - Standard
- **8**: Vertex Shader - Directional Fold
- **9**: Vertex Shader - Wave
- **0**: Vertex Shader - Vortex

### Otros Controles
- **F**: Toggle Wireframe/Filled
- **Z/X**: Ajustar intensidad de efectos
- **W/A/S/D/Q/E**: Mover la luz puntual

## Estructura del Proyecto
- `RendererOpenGL2025.py`: Archivo principal del programa.
- `gl.py`: Clase Renderer para gestión de OpenGL.
- `model.py`: Clase Model para carga de modelos OBJ.
- `buffer.py`: Gestión de buffers de vértices.
- `camera.py`: Implementación de la cámara orbital.
- `skybox.py`: Renderizado del skybox.
- `obj.py`: Parser de archivos OBJ.
- `vertexShaders.py` / `fragmentShaders.py`: Shaders GLSL.
- `models/`: Carpeta con modelos 3D (.obj, .mtl).
- `textures/`: Carpeta con texturas.
- `skybox/`: Carpeta con imágenes para el entorno.
- `venv32/`: Entorno virtual con dependencias.</content>
<parameter name="filePath">d:\Universidad\Semestre 6\Graficas_Computador\Proyecto3_OpenGL\README.md