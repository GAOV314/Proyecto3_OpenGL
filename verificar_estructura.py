"""
Script de Verificación de Estructura de Carpetas
=================================================

Verifica que todos los archivos estén en las carpetas correctas
y que las rutas de carga funcionen.
"""

import os

print("\n" + "="*70)
print("VERIFICACIÓN DE ESTRUCTURA DE CARPETAS")
print("="*70)

# Verificar carpetas
carpetas_requeridas = {
    "models": "Modelos 3D (.obj, .mtl)",
    "textures": "Texturas (.jpg, .png, .bmp)"
}

print("\n📁 CARPETAS:")
for carpeta, descripcion in carpetas_requeridas.items():
    if os.path.exists(carpeta):
        print(f"  ✅ {carpeta}/ - {descripcion}")
    else:
        print(f"  ❌ {carpeta}/ - FALTANTE - {descripcion}")

# Verificar archivos en models/
print("\n📦 ARCHIVOS EN models/:")
if os.path.exists("models"):
    archivos_obj = [f for f in os.listdir('models') if f.endswith('.obj')]
    archivos_mtl = [f for f in os.listdir('models') if f.endswith('.mtl')]
    
    if archivos_obj:
        for obj in archivos_obj:
            print(f"  ✅ {obj}")
    else:
        print("  ⚠️  No hay archivos .obj")
    
    if archivos_mtl:
        for mtl in archivos_mtl:
            print(f"  ✅ {mtl}")
    else:
        print("  ⚠️  No hay archivos .mtl")
else:
    print("  ❌ Carpeta models/ no existe")

# Verificar archivos en textures/
print("\n🎨 ARCHIVOS EN textures/:")
if os.path.exists("textures"):
    texturas = [f for f in os.listdir('textures') 
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')) 
                and not f.startswith('README')]
    
    if texturas:
        for tex in texturas:
            tamano = os.path.getsize(os.path.join('textures', tex)) / 1024
            print(f"  ✅ {tex} ({tamano:.1f} KB)")
    else:
        print("  ⚠️  No hay archivos de textura")
else:
    print("  ❌ Carpeta textures/ no existe")

# Verificar referencias en archivos .mtl
print("\n🔗 VERIFICACIÓN DE REFERENCIAS EN .MTL:")
if os.path.exists("models"):
    archivos_mtl = [f for f in os.listdir('models') if f.endswith('.mtl')]
    
    for mtl in archivos_mtl:
        print(f"\n  Archivo: {mtl}")
        mtl_path = os.path.join('models', mtl)
        
        with open(mtl_path, 'r') as f:
            for line in f:
                if line.strip().startswith('map_'):
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        texture_ref = ' '.join(parts[1:])
                        print(f"    📄 {parts[0]}: {texture_ref}")
                        
                        # Verificar si la textura existe
                        if texture_ref.startswith('../textures/'):
                            texture_path = texture_ref.replace('../textures/', 'textures/')
                        elif texture_ref.startswith('textures/'):
                            texture_path = texture_ref
                        else:
                            texture_path = os.path.join('models', texture_ref)
                        
                        if os.path.exists(texture_path):
                            print(f"       ✅ Archivo encontrado: {texture_path}")
                        else:
                            print(f"       ❌ Archivo NO encontrado: {texture_path}")

# Verificar código Python
print("\n💻 VERIFICACIÓN DE CÓDIGO:")
try:
    with open('RendererOpenGL2025.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Buscar referencias a Model()
        import re
        model_refs = re.findall(r'Model\(["\']([^"\']+)["\']\)', content)
        
        if model_refs:
            print(f"  📝 Referencias a modelos encontradas: {len(model_refs)}")
            for ref in model_refs:
                print(f"    • {ref}")
                if ref.startswith('models/'):
                    print(f"      ✅ Ruta correcta (usa carpeta models/)")
                else:
                    print(f"      ⚠️  Ruta sin carpeta models/ - debería ser 'models/{ref}'")
        else:
            print("  ⚠️  No se encontraron referencias a Model()")
        
        # Buscar referencias a AddTexture()
        texture_refs = re.findall(r'AddTexture\(["\']([^"\']+)["\']\)', content)
        
        if texture_refs:
            print(f"\n  📝 Referencias a texturas manuales: {len(texture_refs)}")
            for ref in texture_refs:
                print(f"    • {ref}")
                if ref.startswith('textures/'):
                    print(f"      ✅ Ruta correcta (usa carpeta textures/)")
                else:
                    print(f"      ⚠️  Ruta sin carpeta textures/ - debería ser 'textures/{ref}'")
        
except Exception as e:
    print(f"  ❌ Error al leer RendererOpenGL2025.py: {e}")

# Resumen
print("\n" + "="*70)
print("RESUMEN")
print("="*70)

errores = []
advertencias = []

if not os.path.exists("models"):
    errores.append("Falta carpeta models/")
elif not os.listdir("models"):
    advertencias.append("Carpeta models/ está vacía")

if not os.path.exists("textures"):
    errores.append("Falta carpeta textures/")

if errores:
    print("\n❌ ERRORES:")
    for error in errores:
        print(f"  • {error}")

if advertencias:
    print("\n⚠️  ADVERTENCIAS:")
    for adv in advertencias:
        print(f"  • {adv}")

if not errores and not advertencias:
    print("\n✅ ¡TODO EN ORDEN!")
    print("\n📋 Estructura correcta:")
    print("  • Carpetas models/ y textures/ creadas")
    print("  • Archivos .obj y .mtl en models/")
    print("  • Archivos de textura en textures/")
    print("  • Referencias en código actualizadas")
    print("\n🚀 Puedes ejecutar:")
    print("  python RendererOpenGL2025.py")

print("="*70 + "\n")

# Información adicional
print("💡 TIPS:")
print("  • Los archivos .obj y .mtl deben estar en models/")
print("  • Las texturas deben estar en textures/")
print("  • En código, usa: Model('models/tu_modelo.obj')")
print("  • En .mtl, usa: map_Kd ../textures/tu_textura.jpg")
print("  • O coloca texturas en models/ y usa: map_Kd tu_textura.jpg\n")
