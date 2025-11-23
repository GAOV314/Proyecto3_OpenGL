



vertex_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(inPosition, 1.0);

    fragPosition = modelMatrix * vec4(inPosition, 1.0);

    fragNormal = normalize( vec3(modelMatrix * vec4(inNormals, 0.0)));

    fragTexCoords = inTexCoords;
}

'''


# NUEVO SHADER 1: Directional Fold Deformation - Doblez direccional como papel arrugado
twist_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform float value;

// Función para rotar un vector alrededor de un eje
vec3 rotateAroundAxis(vec3 p, vec3 axis, float angle) {
    axis = normalize(axis);
    float s = sin(angle);
    float c = cos(angle);
    float oc = 1.0 - c;
    
    mat3 rotMatrix = mat3(
        oc * axis.x * axis.x + c,           oc * axis.x * axis.y - axis.z * s,  oc * axis.z * axis.x + axis.y * s,
        oc * axis.x * axis.y + axis.z * s,  oc * axis.y * axis.y + c,           oc * axis.y * axis.z - axis.x * s,
        oc * axis.z * axis.x - axis.y * s,  oc * axis.y * axis.z + axis.x * s,  oc * axis.z * axis.z + c
    );
    
    return rotMatrix * p;
}

void main()
{
    vec3 pos = inPosition;
    vec3 normal = inNormals;
    
    // Intensidad del doblez MUY REDUCIDA
    float foldStrength = 0.15 + value * 0.3;
    
    // ====== DOBLEZ PRINCIPAL - Eje Y (vertical) - Doblez lateral ======
    vec3 foldCenter1 = vec3(0.0, 0.0, 0.0);
    vec3 foldAxis1 = vec3(0.0, 1.0, 0.0); // Eje Y
    
    // Calcular distancia solo en el plano XZ
    float dist1 = abs(pos.x);
    
    // Ángulo de rotación MUY SUTIL
    float angle1 = dist1 * foldStrength * 0.12;
    
    // Animación muy suave
    angle1 += sin(time * 0.8) * 0.05;
    
    // Aplicar rotación alrededor del eje Y
    vec3 toCenter1 = pos - foldCenter1;
    vec3 folded1 = rotateAroundAxis(toCenter1, foldAxis1, angle1);
    pos = foldCenter1 + folded1;
    
    // Rotar también la normal
    normal = rotateAroundAxis(normal, foldAxis1, angle1);
    
    
    // ====== SEGUNDO DOBLEZ - Eje Z (profundidad) - Doblez frontal ======
    vec3 foldCenter2 = vec3(0.0, 0.0, 0.0);
    vec3 foldAxis2 = vec3(0.0, 0.0, 1.0); // Eje Z
    
    // Doblez basado en la posición Y
    float dist2 = abs(pos.y);
    float angle2 = dist2 * foldStrength * 0.08;
    angle2 += sin(time * 0.6 + 1.5) * 0.04;
    
    vec3 toCenter2 = pos - foldCenter2;
    vec3 folded2 = rotateAroundAxis(toCenter2, foldAxis2, angle2);
    pos = foldCenter2 + folded2;
    
    normal = rotateAroundAxis(normal, foldAxis2, angle2);
    
    
    fragPosition = modelMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    
    fragNormal = normalize(vec3(modelMatrix * vec4(normal, 0.0)));
    fragTexCoords = inTexCoords;
}
'''


# NUEVO SHADER 2: Wave Shader - Onda unificada de abajo hacia arriba
wave_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform float value;

void main()
{
    vec3 pos = inPosition;
    
    // Amplitud controlada por value
    float amplitude = 1.5 + value * 2.0;
    
    // Onda principal que viaja de abajo hacia arriba
    // Usa la posición Y del vértice para determinar la fase de la onda
    float wave = sin(pos.y * 3.0 - time * 4.0) * amplitude;
    
    // Aplicar el desplazamiento en X y Z de forma uniforme
    // Esto hace que todo el objeto oscile junto
    pos.x += wave * 0.3;
    pos.z += wave * 0.3;
    
    // También agregar un movimiento suave en Y para énfasis
    pos.y += cos(pos.y * 2.0 - time * 4.0) * amplitude * 0.2;
    
    fragPosition = modelMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    
    // Calcular normal modificada basada en la derivada de la onda
    float derivative = cos(pos.y * 3.0 - time * 4.0) * 3.0 * amplitude;
    
    vec3 tangentY = vec3(derivative * 0.3, 1.0, derivative * 0.3);
    vec3 modifiedNormal = normalize(cross(vec3(1.0, 0.0, 0.0), tangentY));
    
    fragNormal = normalize(vec3(modelMatrix * vec4(modifiedNormal, 0.0)));
    fragTexCoords = inTexCoords;
}
'''


# NUEVO SHADER 3: Vortex Shader - Efecto de vórtice/remolino
jitter_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform float value;

// Función para rotar alrededor del eje Y
vec3 rotateY(vec3 p, float angle) {
    float c = cos(angle);
    float s = sin(angle);
    return vec3(
        p.x * c - p.z * s,
        p.y,
        p.x * s + p.z * c
    );
}

void main()
{
    vec3 pos = inPosition;
    
    // Centro del vórtice
    vec3 vortexCenter = vec3(0.0, 0.0, 0.0);
    
    // Calcular distancia desde el centro del vórtice
    vec3 toCenter = pos - vortexCenter;
    float distFromCenter = length(toCenter.xz); // Distancia en el plano XZ
    
    // Intensidad del vórtice REDUCIDA (ajustable con Z/X)
    float vortexStrength = 0.5 + value * 1.5;
    
    // Ángulo de rotación basado en:
    // 1. Distancia (más lejos = más rotación)
    // 2. Altura Y (diferentes niveles rotan diferente)
    // 3. Tiempo (animación continua)
    float angle = distFromCenter * vortexStrength * 0.2;  // Reducido de 0.5 a 0.2
    angle += pos.y * vortexStrength * 0.15;  // Reducido de 0.3 a 0.15
    angle += time * 1.0;  // Reducido de 2.0 a 1.0
    
    // Aplicar rotación alrededor del eje Y
    pos = rotateY(pos, angle);
    
    // Efecto de succión hacia el centro REDUCIDO
    float pullStrength = 0.05 + value * 0.1;  // Reducido de 0.2/0.3 a 0.05/0.1
    vec3 pullDirection = normalize(vortexCenter - pos);
    pullDirection.y = 0.0; // Solo tirar en el plano XZ
    
    // La fuerza de succión disminuye con la distancia
    float pullFactor = pullStrength / (1.0 + distFromCenter * 2.0);
    pos += pullDirection * pullFactor * sin(time * 1.5) * 0.3;  // Reducido de 0.5 a 0.3
    
    // Efecto de espiral vertical REDUCIDO
    float spiral = sin(angle * 2.0 - time * 3.0) * 0.08 * value;  // Reducido de 0.2 a 0.08
    pos.y += spiral;
    
    // Efecto de pulsación radial REDUCIDO
    float pulse = sin(time * 2.5 + distFromCenter * 3.0) * 0.04 * value;  // Reducido de 0.1 a 0.04
    pos += normalize(toCenter) * pulse;
    
    fragPosition = modelMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    
    // Rotar las normales también
    vec3 rotatedNormal = rotateY(inNormals, angle);
    
    // Añadir perturbación REDUCIDA a las normales
    vec3 tangentialDir = vec3(-toCenter.z, 0.0, toCenter.x); // Perpendicular al radio
    rotatedNormal = normalize(rotatedNormal + tangentialDir * 0.15 * value);  // Reducido de 0.3 a 0.15
    
    fragNormal = normalize(vec3(modelMatrix * vec4(rotatedNormal, 0.0)));
    fragTexCoords = inTexCoords;
}
'''





water_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;


void main()
{
    float displacement = sin(time + inPosition.x + inPosition.z) * value;
    fragPosition = modelMatrix * vec4(inPosition + vec3(0,displacement, 0)  , 1.0);

    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    fragNormal = normalize( vec3(modelMatrix * vec4(inNormals, 0.0)));

    fragTexCoords = inTexCoords;
}

'''





