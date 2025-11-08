
class Obj(object):
	def __init__(self, filename):
		# Asumiendo que el archivo es un formato .obj
		with open(filename, "r") as file:
			lines = file.read().splitlines()
			
		self.vertices = []
		self.texCoords = []
		self.normals = []
		self.faces = []
		self.faceMaterials = []  # Guardar el material para cada cara
		self.mtlFile = None
		
		current_material = None  # Material activo
		
		for line in lines:
			# Si la linea no cuenta con un prefijo y un valor,
			# seguimos a la siguiente la linea

			line = line.rstrip()

			try:
				prefix, value = line.split(" ", 1)
			except:
				continue
			
			# Dependiendo del prefijo, parseamos y guardamos
			# la informacion en el contenedor correcto
			
			if prefix == "v": # Vertices
				vert = list(map(float,value.split(" ")))
				self.vertices.append(vert)
				
			elif prefix == "vt": # Coordenadas de textura
				vts = list(map(float,value.split(" ")))
				self.texCoords.append([vts[0],vts[1]])
				
			elif prefix == "vn": # Normales
				norm = list(map(float,value.split(" ")))
				self.normals.append(norm)
				
			elif prefix == "f": # Caras
				face = []
				verts = value.split(" ")
				for vert in verts:
					vert = list(map(int, vert.split("/")))
					# Asegurar que cada vértice tenga 3 valores (posición, texcoord, normal)
					while len(vert) < 3:
						vert.append(0)
					face.append(vert)
				self.faces.append(face)
				self.faceMaterials.append(current_material)  # Guardar material para esta cara
			
			elif prefix == "usemtl":  # Cambiar material activo
				current_material = value.strip()
			
			elif prefix == "mtllib": # Archivo MTL
				import os
				# Obtener el directorio del archivo OBJ
				obj_dir = os.path.dirname(filename)
				if not obj_dir:
					obj_dir = "."  # Directorio actual si está vacío
				mtl_filename = os.path.join(obj_dir, value.strip())
				try:
					self.mtlFile = self.LoadMTL(mtl_filename)
				except Exception as e:
					pass  # Silenciar errores de carga MTL
	
	def LoadMTL(self, filename):
		"""Carga un archivo MTL y extrae las texturas"""
		with open(filename, "r") as file:
			lines = file.read().splitlines()
		
		materials = {}
		current_material = None
		
		import os
		mtl_dir = os.path.dirname(filename)
		if not mtl_dir:
			mtl_dir = "."  # Directorio actual si está vacío
		
		for line in lines:
			line = line.strip()
			if not line or line.startswith('#'):
				continue
			
			parts = line.split()
			if not parts:
				continue
			
			prefix = parts[0]
			
			if prefix == "newmtl":
				# Nuevo material
				current_material = parts[1]
				materials[current_material] = {}
			
			elif prefix == "map_Kd" and current_material:
				# Textura difusa (color base)
				texture_file = " ".join(parts[1:])
				texture_path = os.path.join(mtl_dir, texture_file)
				materials[current_material]['diffuse'] = texture_path
			
			elif prefix == "map_Ks" and current_material:
				# Textura especular
				texture_file = " ".join(parts[1:])
				texture_path = os.path.join(mtl_dir, texture_file)
				materials[current_material]['specular'] = texture_path
			
			elif prefix == "map_Bump" and current_material:
				# Mapa de bump/normal
				texture_file = " ".join(parts[1:])
				texture_path = os.path.join(mtl_dir, texture_file)
				materials[current_material]['bump'] = texture_path
		
		return materials                                                                                                                                                                                                                                                                                                                                                                                           