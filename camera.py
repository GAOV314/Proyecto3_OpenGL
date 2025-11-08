import glm
import math

class Camera(object):
	def __init__(self, width, height):

		self.screenWidth = width
		self.screenHeight = height
		
		self.position = glm.vec3(0,0,0)

		# Angulos de Euler
		self.rotation = glm.vec3(0,0,0)

		self.viewMatrix = glm.mat4(1)

		self.CreateProjectionMatrix(60, 0.1, 1000)
		
		# Sistema orbital
		self.orbitalMode = False
		self.target = glm.vec3(0, -2, -12)  # Centro donde mira la cámara
		self.distance = 15.0
		self.angleH = 0.0  # Ángulo horizontal (rotación alrededor del eje Y)
		self.angleV = 20.0  # Ángulo vertical (elevación)
		
		# Límites
		self.minDistance = 2.0
		self.maxDistance = 100.0
		self.minAngleV = -85.0
		self.maxAngleV = 85.0
		self.minAngleH = -180.0  # Límite izquierdo
		self.maxAngleH = 180.0   # Límite derecho
		
		# Sensibilidad
		self.mouseSensitivity = 0.3
		self.keyboardSensitivity = 2.0
		self.zoomSensitivity = 1.0


	def GetViewMatrix(self):
		if self.orbitalMode:
			# Modo orbital: calcular posición desde ángulos esféricos
			return self.GetOrbitalViewMatrix()
		else:
			# Modo libre original
			identity = glm.mat4(1)

			translateMat = glm.translate(identity, self.position)

			pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
			yawMat =   glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
			rollMat =  glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))

			rotationMat = pitchMat * yawMat * rollMat

			camMat = translateMat * rotationMat

			self.viewMatrix = glm.inverse(camMat)

			return self.viewMatrix


	def GetOrbitalViewMatrix(self):
		"""Calcula la view matrix en modo orbital"""
		# Limitar valores
		self.angleH = max(self.minAngleH, min(self.maxAngleH, self.angleH))
		self.angleV = max(self.minAngleV, min(self.maxAngleV, self.angleV))
		self.distance = max(self.minDistance, min(self.maxDistance, self.distance))
		
		# Convertir ángulos a radianes
		angleHRad = math.radians(self.angleH)
		angleVRad = math.radians(self.angleV)
		
		# Calcular posición de la cámara usando coordenadas esféricas
		x = self.target.x + self.distance * math.cos(angleVRad) * math.sin(angleHRad)
		y = self.target.y + self.distance * math.sin(angleVRad)
		z = self.target.z + self.distance * math.cos(angleVRad) * math.cos(angleHRad)
		
		cameraPos = glm.vec3(x, y, z)
		
		# Usar lookAt para generar la view matrix
		self.viewMatrix = glm.lookAt(cameraPos, self.target, glm.vec3(0, 1, 0))
		
		return self.viewMatrix


	def SetTarget(self, target):
		"""Establecer el punto central alrededor del cual orbita la cámara"""
		self.target = target


	def RotateHorizontal(self, angle):
		"""Rotar horizontalmente (izquierda/derecha)"""
		self.angleH += angle


	def RotateVertical(self, angle):
		"""Rotar verticalmente (arriba/abajo)"""
		self.angleV += angle


	def Zoom(self, amount):
		"""Acercar o alejar la cámara"""
		self.distance -= amount


	def CreateProjectionMatrix(self, fov, nearPlane, farPlane):
		self.projectionMatrix = glm.perspective( glm.radians(fov), self.screenWidth / self.screenHeight, nearPlane, farPlane)