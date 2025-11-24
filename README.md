# Proyecto #3 - Visualizador 3D con Shaders Personalizados

## 📋 Descripción del Proyecto

Este proyecto es un renderizador 3D interactivo desarrollado con PyOpenGL que permite visualizar múltiples modelos 3D con shaders personalizados y efectos visuales avanzados. El programa incluye un sistema de cámara orbital, skybox panorámico 360°, y la capacidad de aplicar shaders individuales a cada modelo en la escena.

### ✨ Características Principales

- **Sistema de Cámara Orbital**: Control intuitivo de cámara que orbita alrededor de los modelos
- **Skybox Panorámico 360°**: Fondo inmersivo con imagen equirectangular
- **Shaders Personalizados**: Cada modelo puede tener su propio shader visual único
- **Efectos Visuales Avanzados**:
  - Rainbow Shader: Efecto arcoíris animado con colores HSV
  - Cosmic Shader: Simulación de galaxias con nebulosas y estrellas
  - Pattern Shader: Patrones geométricos procedurales (Voronoi, hexagonales)
  - Wave Shader: Ondas sinusoidales verticales
  - Twist Shader: Deformación de doblez direccional
  - Vortex Shader: Efecto de remolino/vórtice
- **Iluminación Dinámica**: Control de luz puntual en tiempo real
- **Música de Fondo**: Reproducción de música ambiente
- **Modo Wireframe**: Alternar entre vista sólida y malla de alambre

---

## 🛠️ Requisitos

### Dependencias de Python

```bash
pip install PyOpenGL
pip install PyOpenGL-accelerate
pip install PyGLM
pip install pygame
pip install numpy
```

### Requisitos del Sistema

- Python 3.7 o superior
- OpenGL 3.3 o superior
- Tarjeta gráfica compatible con shaders GLSL 330

### Estructura de Archivos Requerida

```
proyecto/
│
├── RendererOpenGL2025.py    # Archivo principal
├── gl.py                     # Motor de renderizado
├── camera.py                 # Sistema de cámara
├── model.py                  # Cargador de modelos 3D
├── obj.py                    # Parser de archivos .obj
├── buffer.py                 # Gestión de buffers OpenGL
├── skybox.py                 # Sistema de skybox
├── vertexShaders.py          # Shaders de vértices
├── fragmentShaders.py        # Shaders de fragmentos
│
├── models/                   # Carpeta de modelos 3D (.obj)
│   ├── model.obj
│   ├── leaf.obj
│   ├── red.obj
│   ├── wigglytuff.obj
│   └── articuno.obj
│
├── skybox/                   # Carpeta de texturas de skybox
│   └── paisaje.jpg
│
├── textures/                 # Carpeta de texturas (opcional)
│
└── music/                    # Carpeta de música
    └── 28 - Battle! (Trainer).mp3
```

---

## 🚀 Cómo Ejecutar

1. **Clonar o descargar el proyecto** en tu máquina local

2. **Instalar las dependencias**:
   ```bash
   pip install PyOpenGL PyOpenGL-accelerate PyGLM pygame numpy
   ```

3. **Verificar la estructura de archivos**: Asegúrate de que todas las carpetas (models, skybox, music) estén en el directorio correcto

4. **Ejecutar el programa**:
   ```bash
   python RendererOpenGL2025.py
   ```

---

## 🎮 Controles

### 🎨 Modo de Shaders
| Tecla | Función |
|-------|---------|
| **M** | Alternar entre shaders individuales ON/OFF<br>• OFF: Todos los modelos sin shaders<br>• ON: Cada modelo con su shader único asignado |

### 📷 Cámara Orbital
| Control | Función |
|---------|---------|
| **Click Izquierdo + Arrastrar** | Rotar cámara alrededor del modelo |
| **Scroll Mouse** | Zoom in/out |
| **← →** (Flechas) | Rotar horizontalmente |
| **↑ ↓** (Flechas) | Rotar verticalmente |
| **+ / =** | Acercar zoom |
| **-** | Alejar zoom |

### 💡 Control de Iluminación
| Tecla | Función |
|-------|---------|
| **W** | Mover luz hacia adelante (-Z) |
| **S** | Mover luz hacia atrás (+Z) |
| **A** | Mover luz a la izquierda (-X) |
| **D** | Mover luz a la derecha (+X) |
| **Q** | Mover luz hacia abajo (-Y) |
| **E** | Mover luz hacia arriba (+Y) |

### 🎛️ Efectos y Visualización
| Tecla | Función |
|-------|---------|
| **F** | Alternar entre modo Wireframe y modo Relleno |
| **Z** | Disminuir intensidad de efectos (value) |
| **X** | Aumentar intensidad de efectos (value) |

---

## 🎨 Shaders Asignados

Cada modelo en la escena tiene una combinación única de shaders:

| Modelo | Vertex Shader | Fragment Shader | Efecto Visual |
|--------|---------------|-----------------|---------------|
| **Model1** (Plataforma) | Wave | Cosmic | Ondas con galaxia |
| **Model2** (Leaf) | Wave | Rainbow | Ondas con arcoíris |
| **Model3** (Red) | Twist | Cosmic | Doblez con galaxia |
| **Model4** (Wigglytuff) | Jitter/Vortex | Pattern | Vórtice con patrones |
| **Model5** (Articuno) | Twist | Pattern | Doblez con patrones |

---

## 📝 Notas Técnicas

- El programa utiliza OpenGL 3.3 Core Profile
- Los shaders están escritos en GLSL versión 330
- La cámara orbital tiene límites configurables de ángulo y distancia
- El skybox utiliza proyección equirectangular para imágenes 360°
- Los modelos deben estar en formato Wavefront OBJ (.obj)
- Se soportan archivos MTL para carga automática de texturas

---

## 🐛 Solución de Problemas

### El programa no inicia
- Verifica que todas las dependencias estén instaladas correctamente
- Asegúrate de tener OpenGL 3.3 o superior

### Los modelos no se visualizan
- Confirma que los archivos .obj estén en la carpeta `models/`
- Verifica que las rutas en el código coincidan con tus archivos

### Los shaders no funcionan
- Presiona la tecla **M** para activar el modo de shaders individuales
- Verifica que tu tarjeta gráfica soporte GLSL 330

### No hay música
- Verifica que el archivo de música esté en la carpeta `music/`
- Ajusta el volumen del sistema

---

## 👨‍💻 Créditos

Proyecto desarrollado como parte del Proyecto #3 de Gráficas por Computadora utilizando PyOpenGL y GLSL.

---

## 📄 Licencia

Este proyecto es de uso educativo.
