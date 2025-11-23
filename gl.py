import glm # pip install PyGLM
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from camera import Camera
from skybox import Skybox

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _,_, self.width, self.height = screen.get_rect()
        
        glClearColor(0.2, 0.2, 0.2, 1.0)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glViewport(0,0, self.width, self.height)
        
        # Configuración adicional para evitar parpadeo
        glFrontFace(GL_CCW)
        glPolygonOffset(1.0, 1.0)

        self.camera = Camera(self.width, self.height)

        self.scene = []
        
        self.filledMode = True
        self.ToggleFilledMode()

        # NUEVO: Modo para activar/desactivar shaders individuales
        self.useIndividualShaders = False

        self.activeShader = None
        self.skybox = None

        self.pointLight = glm.vec3(0,0,0)
        self.ambientLight = 0.5

        self.value = 0.0
        self.elapsedTime = 0.0

    def CreateSkybox(self, textureList):
        self.skybox = Skybox(textureList)
        self.skybox.cameraRef = self.camera

    def ToggleFilledMode(self):
        self.filledMode = not self.filledMode

        if self.filledMode:
            glEnable(GL_CULL_FACE)
            glCullFace(GL_BACK)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glDisable(GL_CULL_FACE)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # NUEVO: Alternar modo de shaders individuales
    def ToggleIndividualShaders(self):
        self.useIndividualShaders = not self.useIndividualShaders
        if self.useIndividualShaders:
            print("✓ Modo SHADERS INDIVIDUALES activado")
        else:
            print("✗ Modo shaders individuales desactivado")

    def SetShaders(self, vertexShader, fragmentShader):
        if vertexShader is not None and fragmentShader is not None:
            self.activeShader = compileProgram( compileShader(vertexShader, GL_VERTEX_SHADER),
                                                compileShader(fragmentShader, GL_FRAGMENT_SHADER) )
        else:
            self.activeShader = None

    # NUEVO: Compilar shader para un objeto específico
    def CompileShaderForObject(self, vertexShader, fragmentShader):
        """Compila y retorna un programa de shader"""
        if vertexShader is not None and fragmentShader is not None:
            return compileProgram( compileShader(vertexShader, GL_VERTEX_SHADER),
                                  compileShader(fragmentShader, GL_FRAGMENT_SHADER) )
        return None

    # MODIFICADO: Enviar uniforms a cualquier shader
    def SendUniforms(self, shaderProgram, obj=None):
        """Envía los uniforms comunes a un shader dado"""
        glUniformMatrix4fv( glGetUniformLocation(shaderProgram, "viewMatrix"),
                            1, GL_FALSE, glm.value_ptr(self.camera.GetViewMatrix()) )

        glUniformMatrix4fv( glGetUniformLocation(shaderProgram, "projectionMatrix"),
                            1, GL_FALSE, glm.value_ptr(self.camera.projectionMatrix) )

        glUniform3fv( glGetUniformLocation(shaderProgram, "pointLight"), 1, glm.value_ptr(self.pointLight) )
        glUniform1f( glGetUniformLocation(shaderProgram, "ambientLight"), self.ambientLight )

        glUniform1f( glGetUniformLocation(shaderProgram, "value"), self.value )
        glUniform1f( glGetUniformLocation(shaderProgram, "time"), self.elapsedTime )

        glUniform1i( glGetUniformLocation(shaderProgram, "tex0"), 0)
        glUniform1i( glGetUniformLocation(shaderProgram, "tex1"), 1)

        # Si hay un objeto, enviar su matriz de modelo
        if obj is not None:
            glUniformMatrix4fv( glGetUniformLocation(shaderProgram, "modelMatrix"),
                                1, GL_FALSE, glm.value_ptr( obj.GetModelMatrix() ) )

    def Render(self):
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

        # Renderizar skybox primero siempre en modo relleno
        if self.skybox is not None:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glDepthFunc(GL_LEQUAL)
            self.skybox.Render()
            glDepthFunc(GL_LESS)
            # Restaurar el modo de polígono según el estado actual
            if self.filledMode:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # MODIFICADO: Renderizar objetos
        for obj in self.scene:
            # Determinar qué shader usar
            if self.useIndividualShaders and hasattr(obj, 'customShader') and obj.customShader is not None:
                # Usar shader individual del objeto
                currentShader = obj.customShader
            else:
                # Usar shader global (o ninguno)
                currentShader = self.activeShader

            # Activar el shader correspondiente
            if currentShader is not None:
                glUseProgram(currentShader)
                self.SendUniforms(currentShader, obj)

            # Renderizar el objeto
            obj.Render()