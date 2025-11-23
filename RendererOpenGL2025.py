import pygame
import pygame.display
from pygame.locals import *
import pygame.mixer

import glm

from gl import Renderer
from buffer import Buffer
from model import Model
from vertexShaders import *
from fragmentShaders import *

width = 1200
height = 640

deltaTime = 0.0

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.pointLight = glm.vec3(1,1,1)

# Shader global por defecto (cuando useIndividualShaders = False)
currVertexShader = vertex_shader
currFragmentShader = fragment_shader

pygame.mixer.init()
pygame.mixer.music.load("music/28 - Battle! (Trainer).mp3")

rend.SetShaders(currVertexShader, currFragmentShader)

# Cargar imagen 360 como skybox
skyboxTextures = ["skybox/paisaje.jpg"]
rend.CreateSkybox(skyboxTextures)

# ============================================================
# CREAR MODELOS
# ============================================================

# Model1 - Plataforma base
model1 = Model("models/model.obj")
model1.position.x = 0
model1.position.y = -2
model1.position.z = -12
model1.scale = glm.vec3(1.0, 1.0, 1.0)

# Model2 - Izquierda
model2 = Model("models/leaf.obj")
model2.position.x = -16
model2.position.y = -3
model2.position.z = -6
model2.rotation.y = 90
model2.scale = glm.vec3(0.5, 0.5, 0.5)

# Model3 - Derecha
model3 = Model("models/red.obj")
model3.position.x = 18
model3.position.y = -3
model3.position.z = -6
model3.rotation.y = -90
model3.scale = glm.vec3(0.5, 0.5, 0.5)

# Model4 - Adelante izquierda
model4 = Model("models/wigglytuff.obj")
model4.position.x = -6
model4.position.y = -3
model4.position.z = -10
model4.rotation.y = 90
model4.scale = glm.vec3(0.5, 0.5, 0.5)

# Model5 - Adelante derecha
model5 = Model("models/articuno.obj")
model5.position.x = 4
model5.position.y = 3
model5.position.z = -10
model5.rotation.x = -20
model5.rotation.y = -90
model5.rotation.z = -15
model5.scale = glm.vec3(0.1, 0.1, 0.1)



# Model1: vertex_shader + fragment_shader (iluminación básica)
model1.customShader = rend.CompileShaderForObject(wave_shader, cosmic_shader)

# Model2: wave_shader + rainbow_shader (ondas con arcoíris)
model2.customShader = rend.CompileShaderForObject(wave_shader, rainbow_shader)

# Model3: twist_shader + cosmic_shader (doblez con galaxia)
model3.customShader = rend.CompileShaderForObject(twist_shader, cosmic_shader)

# Model4: jitter_shader + pattern_shader (vórtice con patrones)
model4.customShader = rend.CompileShaderForObject(jitter_shader, pattern_shader)

# Model5: vertex_shader + fragment_shader (estándar)
model5.customShader = rend.CompileShaderForObject(twist_shader, pattern_shader)

# Lista de modelos
models = [model1, model2, model3, model4, model5]

# Agregar todos los modelos a la escena
for model in models:
    rend.scene.append(model)

# Activar modo orbital de cámara
rend.camera.orbitalMode = True
rend.camera.SetTarget(glm.vec3(0, -2, -12))

# Ciclo de música
pygame.mixer.music.play(-1)


print("\n" + "="*60)
print("CONTROLES - MODO SHADERS INDIVIDUALES")
print("="*60)
print("\nModo de Shaders:")
print("  M - Alternar entre shaders individuales ON/OFF")
print("       OFF: Todos los modelos sin shaders")
print("       ON:  Cada modelo con su shader único asignado")
print("\nAsignaciones actuales:")
print("  Model1 (Plataforma): Standard + Basic Lighting")
print("  Model2 (Leaf):       Wave + Rainbow")
print("  Model3 (Red):        Twist + Cosmic")
print("  Model4 (Wigglytuff): Vortex + Pattern")
print("  Model5 (Articuno):   Standard + Basic Lighting")
print("\nCámara Orbital:")
print("  Mouse Click + Arrastrar - Rotar alrededor del modelo")
print("  Scroll Mouse - Zoom in/out")
print("  Flechas ← → - Rotar horizontalmente")
print("  Flechas ↑ ↓ - Rotar verticalmente")
print("  + / - - Zoom")
print("\nOtros controles:")
print("  F - Toggle Wireframe/Filled")
print("  Z/X - Ajustar value (intensidad de efectos)")
print("  W/A/S/D/Q/E - Mover luz")
print("="*60 + "\n")

# Variables para control del mouse
mousePressed = False
lastMouseX = 0
lastMouseY = 0

isRunning = True

while isRunning:
    deltaTime = clock.tick(60) / 1000
    rend.elapsedTime += deltaTime

    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        
        # Controles del mouse para cámara orbital
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Click izquierdo
                mousePressed = True
                lastMouseX, lastMouseY = event.pos
            elif event.button == 4:  # Scroll up
                rend.camera.Zoom(rend.camera.zoomSensitivity)
            elif event.button == 5:  # Scroll down
                rend.camera.Zoom(-rend.camera.zoomSensitivity)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mousePressed = False
        
        elif event.type == pygame.MOUSEMOTION:
            if mousePressed:
                mouseX, mouseY = event.pos
                deltaX = mouseX - lastMouseX
                deltaY = mouseY - lastMouseY
                
                rend.camera.RotateHorizontal(deltaX * rend.camera.mouseSensitivity)
                rend.camera.RotateVertical(-deltaY * rend.camera.mouseSensitivity)
                
                lastMouseX, lastMouseY = mouseX, mouseY

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                rend.ToggleFilledMode()
            
            # NUEVO: Alternar modo de shaders individuales
            if event.key == pygame.K_m:
                rend.ToggleIndividualShaders()
    
    # Controles de cámara orbital con teclado
    if keys[K_LEFT]:
        rend.camera.RotateHorizontal(-rend.camera.keyboardSensitivity)
    
    if keys[K_RIGHT]:
        rend.camera.RotateHorizontal(rend.camera.keyboardSensitivity)
    
    if keys[K_UP]:
        rend.camera.RotateVertical(rend.camera.keyboardSensitivity)
    
    if keys[K_DOWN]:
        rend.camera.RotateVertical(-rend.camera.keyboardSensitivity)
    
    # Zoom con + y -
    if keys[K_EQUALS] or keys[K_PLUS]:  # + key
        rend.camera.Zoom(rend.camera.zoomSensitivity * deltaTime * 10)
    
    if keys[K_MINUS]:  # - key
        rend.camera.Zoom(-rend.camera.zoomSensitivity * deltaTime * 10)

    # Controles de luz
    if keys[K_w]:
        rend.pointLight.z -= 10 * deltaTime

    if keys[K_s]:
        rend.pointLight.z += 10 * deltaTime

    if keys[K_a]:
        rend.pointLight.x -= 10 * deltaTime

    if keys[K_d]:
        rend.pointLight.x += 10 * deltaTime

    if keys[K_q]:
        rend.pointLight.y -= 10 * deltaTime

    if keys[K_e]:
        rend.pointLight.y += 10 * deltaTime

    # Controlar intensidad de efectos
    if keys[K_z]:
        if rend.value > 0.0:
            rend.value -= 1 * deltaTime

    if keys[K_x]:
        if rend.value < 1.0:
            rend.value += 1 * deltaTime

    # Renderizar
    rend.Render()
    pygame.display.flip()

pygame.quit()