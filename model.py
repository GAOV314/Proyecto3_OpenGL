from OpenGL.GL import *
from obj import Obj
from buffer import Buffer

import glm

import pygame

class Model(object):
	def __init__(self, filename):
		self.objFile = Obj(filename)

		self.position = glm.vec3(0,0,0)
		self.rotation = glm.vec3(0,0,0)
		self.scale = glm.vec3(1,1,1)

		self.textures = {}  # Diccionario: nombre_material -> texture_id
		self.materialToTexture = {}  # Mapa de material a índice de textura
		
		# Cargar texturas desde el archivo MTL si existe
		self.LoadTexturesFromMTL()
		
		self.BuildBuffers()  # Después de cargar texturas

	def GetModelMatrix(self):

		identity = glm.mat4(1)

		translateMat = glm.translate(identity, self.position)

		pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
		yawMat =   glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
		rollMat =  glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))

		rotationMat = pitchMat * yawMat * rollMat

		scaleMat = glm.scale(identity, self.scale)

		return translateMat * rotationMat * scaleMat


	def BuildBuffers(self):
		# Agrupar caras por material
		material_groups = {}
		
		for face_idx, face in enumerate(self.objFile.faces):
			material = self.objFile.faceMaterials[face_idx] if face_idx < len(self.objFile.faceMaterials) else None
			
			if material not in material_groups:
				material_groups[material] = []
			material_groups[material].append(face)
		
		# Crear buffers separados para cada material
		self.materialBuffers = []
		
		for material, faces in material_groups.items():
			positions = []
			texCoords = []
			normals = []
			vertexCount = 0
			
			for face in faces:
				facePositions = []
				faceTexCoords = []
				faceNormals = []

				for i in range(len(face)):
					# Posiciones
					facePositions.append(self.objFile.vertices[face[i][0] - 1])
					
					# Coordenadas de textura (con valor por defecto si no existen)
					if face[i][1] != 0 and face[i][1] <= len(self.objFile.texCoords):
						faceTexCoords.append(self.objFile.texCoords[face[i][1] - 1])
					else:
						faceTexCoords.append([0, 0])  # Valor por defecto
					
					# Normales (con valor por defecto si no existen)
					if face[i][2] != 0 and face[i][2] <= len(self.objFile.normals):
						faceNormals.append(self.objFile.normals[face[i][2] - 1])
					else:
						faceNormals.append([0, 1, 0])  # Normal hacia arriba por defecto

				# Primer triángulo
				for value in facePositions[0]: positions.append(value)
				for value in facePositions[1]: positions.append(value)
				for value in facePositions[2]: positions.append(value)

				for value in faceTexCoords[0]: texCoords.append(value)
				for value in faceTexCoords[1]: texCoords.append(value)
				for value in faceTexCoords[2]: texCoords.append(value)

				for value in faceNormals[0]: normals.append(value)
				for value in faceNormals[1]: normals.append(value)
				for value in faceNormals[2]: normals.append(value)

				vertexCount += 3

				# Si es un quad, agregar el segundo triángulo
				if len(face) == 4:
					for value in facePositions[0]: positions.append(value)
					for value in facePositions[2]: positions.append(value)
					for value in facePositions[3]: positions.append(value)

					for value in faceTexCoords[0]: texCoords.append(value)
					for value in faceTexCoords[2]: texCoords.append(value)
					for value in faceTexCoords[3]: texCoords.append(value)

					for value in faceNormals[0]: normals.append(value)
					for value in faceNormals[2]: normals.append(value)
					for value in faceNormals[3]: normals.append(value)

					vertexCount += 3
			
			# Crear buffers para este material
			materialBuffer = {
				'material': material,
				'posBuffer': Buffer(positions),
				'texCoordsBuffer': Buffer(texCoords),
				'normalsBuffer': Buffer(normals),
				'vertexCount': vertexCount
			}
			self.materialBuffers.append(materialBuffer)


	def AddTexture(self, filename):
		textureSurface = pygame.image.load(filename)
		
		# Detectar si la imagen tiene canal alpha (transparencia)
		if textureSurface.get_alpha() is not None or filename.lower().endswith('.png'):
			textureData = pygame.image.tostring(textureSurface, "RGBA", True)
			internalFormat = GL_RGBA
			format = GL_RGBA
		else:
			textureData = pygame.image.tostring(textureSurface, "RGB", True)
			internalFormat = GL_RGB
			format = GL_RGB

		texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, texture)

		glTexImage2D(GL_TEXTURE_2D,
					 0,
					 internalFormat,
					 textureSurface.get_width(),
					 textureSurface.get_height(),
					 0,
					 format,
					 GL_UNSIGNED_BYTE,
					 textureData)

		glGenerateMipmap(GL_TEXTURE_2D)

		return texture
	
	
	def LoadTexturesFromMTL(self):
		"""Carga automáticamente las texturas desde el archivo MTL"""
		if self.objFile.mtlFile:
			for material_name, material_data in self.objFile.mtlFile.items():
				if 'diffuse' in material_data:
					import os
					texture_path = material_data['diffuse']
					
					if os.path.exists(texture_path):
						try:
							texture_id = self.AddTexture(texture_path)
							self.textures[material_name] = texture_id
						except Exception as e:
							pass


	def Render(self):
		# Renderizar cada grupo de material con su textura
		for materialBuffer in self.materialBuffers:
			material = materialBuffer['material']
			
			# Activar la textura correspondiente al material
			if material and material in self.textures:
				glActiveTexture(GL_TEXTURE0)
				glBindTexture(GL_TEXTURE_2D, self.textures[material])
			elif len(self.textures) > 0:
				# Si no hay material específico, usar la primera textura
				first_texture = list(self.textures.values())[0]
				glActiveTexture(GL_TEXTURE0)
				glBindTexture(GL_TEXTURE_2D, first_texture)
			
			# Usar los buffers de este grupo
			materialBuffer['posBuffer'].Use(0, 3)
			materialBuffer['texCoordsBuffer'].Use(1, 2)
			materialBuffer['normalsBuffer'].Use(2, 3)

			glDrawArrays(GL_TRIANGLES, 0, materialBuffer['vertexCount'])

			glDisableVertexAttribArray(0)
			glDisableVertexAttribArray(1)
			glDisableVertexAttribArray(2)




