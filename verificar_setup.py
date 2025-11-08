"""
Script de Prueba - Model Viewer
================================

Este script verifica que puedes ejecutar el programa con los modelos configurados.

INSTRUCCIONES:
1. Asegúrate de tener al menos un archivo .obj en la carpeta principal
2. Ejecuta este script para probar la funcionalidad básica
3. Presiona TAB para cambiar entre modelos
4. Presiona ESC para salir
"""

import sys
import os

# Verificar archivos necesarios
print("\n" + "="*60)
print("VERIFICACIÓN DEL ENTORNO")
print("="*60)

archivos_necesarios = [
    "gl.py",
    "model.py",
    "buffer.py",
    "camera.py",
    "obj.py",
    "vertexShaders.py",
    "fragmentShaders.py",
    "skybox.py",
    "RendererOpenGL2025.py"
]

archivos_faltantes = []
for archivo in archivos_necesarios:
    if os.path.exists(archivo):
        print(f"✅ {archivo}")
    else:
        print(f"❌ {archivo} - FALTANTE")
        archivos_faltantes.append(archivo)

# Buscar archivos .obj
print("\n" + "="*60)
print("MODELOS OBJ DISPONIBLES")
print("="*60)

archivos_obj = [f for f in os.listdir('.') if f.endswith('.obj')]
if archivos_obj:
    for obj in archivos_obj:
        print(f"📦 {obj}")
else:
    print("⚠️  No se encontraron archivos .obj")

# Verificar carpeta de texturas
print("\n" + "="*60)
print("TEXTURAS DISPONIBLES")
print("="*60)

if os.path.exists("textures"):
    texturas = [f for f in os.listdir('textures') if f.lower().endswith(('.jpg', '.png', '.bmp'))]
    if texturas:
        for tex in texturas:
            print(f"🎨 textures/{tex}")
    else:
        print("⚠️  La carpeta textures está vacía")
else:
    print("⚠️  No existe la carpeta textures/")

# Verificar carpeta de skybox
print("\n" + "="*60)
print("SKYBOX")
print("="*60)

if os.path.exists("skybox"):
    skybox_files = ["right.jpg", "left.jpg", "top.jpg", "bottom.jpg", "front.jpg", "back.jpg"]
    skybox_completo = True
    for sf in skybox_files:
        path = os.path.join("skybox", sf)
        if os.path.exists(path):
            print(f"✅ {sf}")
        else:
            print(f"❌ {sf} - FALTANTE")
            skybox_completo = False
    
    if not skybox_completo:
        print("\n⚠️  Skybox incompleto - El programa puede fallar al cargar")
else:
    print("⚠️  No existe la carpeta skybox/")

# Verificar dependencias
print("\n" + "="*60)
print("DEPENDENCIAS DE PYTHON")
print("="*60)

dependencias = {
    "pygame": "pygame",
    "OpenGL": "PyOpenGL",
    "glm": "PyGLM",
    "numpy": "numpy"
}

dependencias_faltantes = []
for modulo, paquete in dependencias.items():
    try:
        __import__(modulo)
        print(f"✅ {paquete}")
    except ImportError:
        print(f"❌ {paquete} - NO INSTALADO")
        dependencias_faltantes.append(paquete)

# Resumen final
print("\n" + "="*60)
print("RESUMEN")
print("="*60)

if archivos_faltantes:
    print(f"❌ Archivos faltantes: {len(archivos_faltantes)}")
    for af in archivos_faltantes:
        print(f"   - {af}")

if dependencias_faltantes:
    print(f"❌ Dependencias faltantes: {len(dependencias_faltantes)}")
    for df in dependencias_faltantes:
        print(f"   - {df}")
    print("\nPara instalarlas:")
    print(f"   pip install {' '.join(dependencias_faltantes)}")

if not archivos_obj:
    print("⚠️  No hay archivos .obj - Necesitas al menos uno para ejecutar el programa")

if not archivos_faltantes and not dependencias_faltantes and archivos_obj:
    print("\n✅ ¡Todo listo! Puedes ejecutar el programa:")
    print("   python RendererOpenGL2025.py")
    print("\n🎮 Controles:")
    print("   TAB - Cambiar modelo")
    print("   1-4 - Fragment Shaders")
    print("   7-0 - Vertex Shaders")
    print("   F   - Toggle Wireframe")
else:
    print("\n⚠️  Hay problemas que debes resolver antes de ejecutar")

print("="*60 + "\n")

# Información adicional
print("📝 NOTAS IMPORTANTES:")
print("   • El programa carga 3 modelos (puedes usar el mismo .obj 3 veces)")
print("   • Las texturas se cargan automáticamente desde archivos .mtl")
print("   • Usa TAB para cambiar entre los modelos cargados")
print("   • Solo un modelo es visible a la vez")
print("   • Los shaders se aplican al modelo visible\n")
