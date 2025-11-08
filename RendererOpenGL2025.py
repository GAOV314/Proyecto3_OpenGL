import pygame
import pygame.display
from pygame.locals import *

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

currVertexShader = vertex_shader
currFragmentShader = fragment_shader

rend.SetShaders(currVertexShader, currFragmentShader)

# Cargar imagen 360 como skybox
skyboxTextures = ["skybox/hdri_sky_766.jpg"]

rend.CreateSkybox(skyboxTextures)

# Cargar los tres modelos OBJ desde la carpeta models/
# Modelo 1
model1 = Model("models/model.obj")
# Las texturas se cargan automáticamente desde el archivo .mtl si existe
# Si quieres usar texturas manuales, descomenta las siguientes líneas:
# if len(model1.textures) == 0:
# 	model1.AddTexture("textures/texture1.jpg")

model1.position.x = 0
model1.position.y = -2
model1.position.z = -12
model1.scale = glm.vec3(0.05, 0.05, 0.05)

# Modelo 2 - Cambia "model2.obj" por el archivo OBJ que quieras usar
model2 = Model("models/Boo_fix.obj")  # Cambia esto por tu segundo archivo .obj
# if len(model2.textures) == 0:
# 	model2.AddTexture("textures/texture2.jpg")

model2.position.x = 0
model2.position.y = -2
model2.position.z = -12
model2.scale = glm.vec3(0.05, 0.05, 0.05)

# Modelo 3 - Cambia "model3.obj" por el archivo OBJ que quieras usar
model3 = Model("models/gremlingus.obj")  # Cambia esto por tu tercer archivo .obj
# if len(model3.textures) == 0:
# 	model3.AddTexture("textures/texture3.jpg")

model3.position.x = 0
model3.position.y = -2
model3.position.z = -12
model3.scale = glm.vec3(2.0, 2.0, 2.0)  # Escala grande como solicitaste

# Lista de modelos y control del modelo actual
models = [model1, model2, model3]
currentModelIndex = 0

# Agregar solo el modelo actual a la escena
rend.scene.append(models[currentModelIndex])

# Activar modo orbital de cámara
rend.camera.orbitalMode = True
rend.camera.SetTarget(glm.vec3(0, -2, -12))

print("\n" + "="*60)
print("CONTROLES DE SHADERS")
print("="*60)
print("\nFragment Shaders:")
print("  1 - Basic Lighting")
print("  2 - Rainbow/Gradient (NUEVO)")
print("  3 - Cosmic Shader (NUEVO) - Galaxia con nebulosas y estrellas")
print("  4 - Procedural Pattern (NUEVO)")
print("\nVertex Shaders:")
print("  7 - Standard")
print("  8 - Directional Fold (NUEVO) - Doblez como papel arrugado")
print("  9 - Wave (NUEVO)")
print("  0 - Vortex (NUEVO) - Efecto de remolino/torbellino")
print("\nCambio de Modelos:")
print("  TAB - Cambiar al siguiente modelo")
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
print(f"Modelo actual: {currentModelIndex + 1}/3\n")

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
			
			# Cambiar de modelo con Tab
			if event.key == pygame.K_TAB:
				# Remover el modelo actual de la escena
				rend.scene.remove(models[currentModelIndex])
				
				# Cambiar al siguiente modelo
				currentModelIndex = (currentModelIndex + 1) % len(models)
				
				# Agregar el nuevo modelo a la escena
				rend.scene.append(models[currentModelIndex])
				
				print(f"\n>>> Cambiando a Modelo {currentModelIndex + 1}/3\n")

			# Fragment Shaders
			if event.key == pygame.K_1:
				currFragmentShader = fragment_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Fragment: Basic Lighting")

			if event.key == pygame.K_2:
				currFragmentShader = rainbow_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Fragment: Rainbow/Gradient (NUEVO)")

			if event.key == pygame.K_3:
				currFragmentShader = cosmic_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Fragment: Cosmic Shader (NUEVO) - Galaxia con nebulosas y estrellas")

			if event.key == pygame.K_4:
				currFragmentShader = pattern_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Fragment: Procedural Pattern (NUEVO)")
			
			# Vertex Shaders
			if event.key == pygame.K_7:
				currVertexShader = vertex_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Vertex: Standard")


			if event.key == pygame.K_8:
				currVertexShader = twist_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Vertex: Directional Fold (NUEVO) - Doblez como papel arrugado")
			
			if event.key == pygame.K_9:
				currVertexShader = wave_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Vertex: Wave (NUEVO)")
			
			if event.key == pygame.K_0:
				currVertexShader = jitter_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Vertex: Vortex (NUEVO) - Efecto de remolino/torbellino")
	
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


	if keys[K_z]:
		if rend.value > 0.0:
			rend.value -= 1 * deltaTime

	if keys[K_x]:
		if rend.value < 1.0:
			rend.value += 1 * deltaTime



	# faceModel.rotation.y += 45 * deltaTime


	rend.Render()
	pygame.display.flip()

pygame.quit()