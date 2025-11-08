
from numpy import array, float32
import glm
from OpenGL.GL import * 
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL.EXT.texture_filter_anisotropic import GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT, GL_TEXTURE_MAX_ANISOTROPY_EXT
import pygame
import math


skybox_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 inPosition;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


out vec3 texCoords;

void main()
{
    texCoords = inPosition;
    mat4 vm = mat4(mat3(viewMatrix));
    gl_Position = projectionMatrix * vm * vec4(inPosition, 1.0);
}

'''


# Shader para imagen 360 equirectangular
skybox_fragment_shader_360 = '''
#version 450 core

uniform sampler2D skybox360;

in vec3 texCoords;

out vec4 fragColor;

const float PI = 3.14159265359;

void main()
{
    // Convertir coordenadas del cubo a dirección normalizada
    vec3 dir = normalize(texCoords);
    
    // Convertir dirección 3D a coordenadas UV equirectangulares
    float theta = atan(dir.z, dir.x); // ángulo horizontal
    float phi = asin(dir.y);           // ángulo vertical
    
    vec2 uv;
    uv.x = (theta / (2.0 * PI)) + 0.5;
    uv.y = (phi / PI) + 0.5;  // Ya no invertimos porque se voltea al cargar
    
    fragColor = texture(skybox360, uv);
}

'''


skybox_fragment_shader = '''
#version 450 core

uniform samplerCube skybox;

in vec3 texCoords;

out vec4 fragColor;

void main()
{
    fragColor = texture(skybox, texCoords);
}

'''


class Skybox(object):
	def __init__(self, textureList):
		self.cameraRef = None
		self.is360 = len(textureList) == 1  # Si hay una sola textura, es imagen 360
		
		skyboxVertices = [-1.0,  1.0, -1.0,
						  -1.0, -1.0, -1.0,
						   1.0, -1.0, -1.0,
						   1.0, -1.0, -1.0,
						   1.0,  1.0, -1.0,
						  -1.0,  1.0, -1.0,
						  
						  -1.0, -1.0,  1.0,
						  -1.0, -1.0, -1.0,
						  -1.0,  1.0, -1.0,
						  -1.0,  1.0, -1.0,
						  -1.0,  1.0,  1.0,
						  -1.0, -1.0,  1.0,
						  
						   1.0, -1.0, -1.0,
						   1.0, -1.0,  1.0,
						   1.0,  1.0,  1.0,
						   1.0,  1.0,  1.0,
						   1.0,  1.0, -1.0,
						   1.0, -1.0, -1.0,
						  
						  -1.0, -1.0,  1.0,
						  -1.0,  1.0,  1.0,
						   1.0,  1.0,  1.0,
						   1.0,  1.0,  1.0,
						   1.0, -1.0,  1.0,
						  -1.0, -1.0,  1.0,
						  
						  -1.0,  1.0, -1.0,
						   1.0,  1.0, -1.0,
						   1.0,  1.0,  1.0,
						   1.0,  1.0,  1.0,
						  -1.0,  1.0,  1.0,
						  -1.0,  1.0, -1.0,
						  
						  -1.0, -1.0, -1.0,
						  -1.0, -1.0,  1.0,
						   1.0, -1.0, -1.0,
						   1.0, -1.0, -1.0,
						  -1.0, -1.0,  1.0,
						   1.0, -1.0,  1.0 ]
		
		self.vertexBuffer = array(skyboxVertices, dtype = float32 )
		self.VBO = glGenBuffers(1)
		
		# Seleccionar shader según tipo de textura
		if self.is360:
			self.shaders = compileProgram(compileShader(skybox_vertex_shader, GL_VERTEX_SHADER),
										  compileShader(skybox_fragment_shader_360, GL_FRAGMENT_SHADER))
		else:
			self.shaders = compileProgram(compileShader(skybox_vertex_shader, GL_VERTEX_SHADER),
										  compileShader(skybox_fragment_shader, GL_FRAGMENT_SHADER))
		
		self.texture = glGenTextures(1)
		
		if self.is360:
			# Cargar imagen 360 como textura 2D
			glBindTexture(GL_TEXTURE_2D, self.texture)
			
			# Cargar imagen y convertir a formato RGB si es necesario
			texture = pygame.image.load(textureList[0])
			texture = texture.convert()  # Asegurar formato consistente
			textureData = pygame.image.tostring(texture, "RGB", True)  # True = flip vertical
			
			width = texture.get_width()
			height = texture.get_height()
			
			# Usar formato interno de alta calidad (RGB8 en lugar de RGB genérico)
			glTexImage2D(GL_TEXTURE_2D,
						 0,
						 GL_RGB8,  # Formato interno de 8 bits por canal
						 width,
						 height,
						 0,
						 GL_RGB,
						 GL_UNSIGNED_BYTE,
						 textureData)
			
			# Generar mipmaps para mejor calidad
			glGenerateMipmap(GL_TEXTURE_2D)
			
			# Filtros de máxima calidad
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
			
			# Anisotropic filtering para máxima calidad en ángulos oblicuos
			try:
				maxAnisotropy = glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)
				glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, min(16.0, maxAnisotropy))
			except:
				pass  # Si no está disponible, continuar sin anisotropic filtering
		else:
			# Cargar cubemap de 6 caras
			glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)
			
			for i in range(len(textureList)):
				texture = pygame.image.load(textureList[i])
				textureData = pygame.image.tostring(texture, "RGB", False)
				
				glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i,
							 0,
							 GL_RGB,
							 texture.get_width(),
							 texture.get_height(),
							 0,
							 GL_RGB,
							 GL_UNSIGNED_BYTE,
							 textureData)
			
			glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
			glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
			glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
			glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
			glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
		

	def Render(self):
		if self.shaders == None:
			return
		
		glUseProgram(self.shaders)
		
		if self.cameraRef is not None:
			glUniformMatrix4fv( glGetUniformLocation(self.shaders, "viewMatrix"),
								1, GL_FALSE, glm.value_ptr( self.cameraRef.viewMatrix) )
			
			glUniformMatrix4fv( glGetUniformLocation(self.shaders, "projectionMatrix"),
								1, GL_FALSE, glm.value_ptr( self.cameraRef.projectionMatrix) )
		
		glDepthMask(GL_FALSE)
		
		# Bind textura según tipo
		if self.is360:
			glBindTexture(GL_TEXTURE_2D, self.texture)
		else:
			glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)
		
		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
		
		glBufferData(GL_ARRAY_BUFFER,
					 self.vertexBuffer.nbytes,
					 self.vertexBuffer,
					 GL_STATIC_DRAW)
		
		glEnableVertexAttribArray(0)
		
		glVertexAttribPointer(0,
							  3,
							  GL_FLOAT,
							  GL_FALSE,
							  4 * 3,
							  ctypes.c_void_p(0) )
		
		
		glDrawArrays(GL_TRIANGLES, 0, 36)
		
		glDisableVertexAttribArray(0)

		glDepthMask(GL_TRUE)
		
