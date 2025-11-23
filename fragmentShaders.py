# GLSL

fragment_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max( 0 , dot(fragNormal, lightDir)) + ambientLight;

    fragColor = texture(tex0, fragTexCoords) * intensity;
}

'''


# NUEVO SHADER 1: Rainbow/Gradient Shader - Arcoíris dinámico animado
rainbow_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform float time;
uniform sampler2D tex0;

// Función para convertir HSV a RGB
vec3 hsv2rgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void main()
{
    // Crear un gradiente basado en posición y tiempo
    float hue = fract(fragPosition.x * 0.1 + fragPosition.y * 0.1 + fragPosition.z * 0.1 + time * 0.3);
    
    // Añadir ondas para hacer el arcoíris más dinámico
    hue += sin(fragPosition.y * 3.0 + time * 2.0) * 0.1;
    hue += cos(fragPosition.x * 2.0 - time * 1.5) * 0.1;
    
    // Variar saturación y brillo con el tiempo para efecto pulsante
    float saturation = 0.8 + sin(time * 3.0) * 0.2;
    float value = 0.9 + cos(time * 2.5) * 0.1;
    
    vec3 rainbowColor = hsv2rgb(vec3(hue, saturation, value));
    
    // Mezclar con la textura original
    vec3 texColor = texture(tex0, fragTexCoords).rgb;
    vec3 finalColor = mix(texColor, rainbowColor, 0.7);
    
    fragColor = vec4(finalColor, 1.0);
}
'''


# NUEVO SHADER 2: Cosmic Shader - Galaxia con nebulosas y estrellas
cosmic_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform float time;
uniform sampler2D tex0;

// Función de ruido hash
float hash(vec3 p) {
    p = fract(p * vec3(443.897, 441.423, 437.195));
    p += dot(p, p.yzx + 19.19);
    return fract((p.x + p.y) * p.z);
}

// Ruido 3D suave
float noise3D(vec3 p) {
    vec3 i = floor(p);
    vec3 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    
    return mix(
        mix(mix(hash(i + vec3(0,0,0)), hash(i + vec3(1,0,0)), f.x),
            mix(hash(i + vec3(0,1,0)), hash(i + vec3(1,1,0)), f.x), f.y),
        mix(mix(hash(i + vec3(0,0,1)), hash(i + vec3(1,0,1)), f.x),
            mix(hash(i + vec3(0,1,1)), hash(i + vec3(1,1,1)), f.x), f.y),
        f.z
    );
}

// Fractal Brownian Motion (FBM) - para nebulosas
float fbm(vec3 p) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    
    for(int i = 0; i < 5; i++) {
        value += amplitude * noise3D(p * frequency);
        frequency *= 2.0;
        amplitude *= 0.5;
    }
    return value;
}

// Función para crear estrellas parpadeantes
float stars(vec3 p, float threshold) {
    float n = hash(floor(p));
    float twinkle = sin(time * 3.0 + n * 6.28) * 0.5 + 0.5;
    return (n > threshold) ? twinkle : 0.0;
}

void main()
{
    // Coordenadas espaciales animadas
    vec3 pos = fragPosition.xyz * 2.0;
    vec3 animatedPos = pos + vec3(time * 0.1, time * 0.05, time * 0.08);
    
    // Crear nebulosas con FBM
    float nebula1 = fbm(animatedPos * 0.8);
    float nebula2 = fbm(animatedPos * 1.2 + vec3(100.0, 50.0, 75.0));
    float nebula3 = fbm(animatedPos * 0.5 - vec3(50.0, 25.0, 100.0));
    
    // Colores de nebulosa (púrpura, azul, rosa)
    vec3 color1 = vec3(0.4, 0.1, 0.6); // Púrpura profundo
    vec3 color2 = vec3(0.1, 0.3, 0.8); // Azul espacial
    vec3 color3 = vec3(0.8, 0.2, 0.5); // Rosa nebulosa
    vec3 color4 = vec3(0.2, 0.5, 0.9); // Azul brillante
    
    // Mezclar colores de nebulosa basado en el ruido
    vec3 nebulaColor = mix(color1, color2, nebula1);
    nebulaColor = mix(nebulaColor, color3, nebula2 * 0.7);
    nebulaColor = mix(nebulaColor, color4, nebula3 * 0.5);
    
    // Añadir variación temporal a los colores
    nebulaColor += vec3(
        sin(time * 0.5 + nebula1 * 3.14) * 0.1,
        cos(time * 0.3 + nebula2 * 3.14) * 0.1,
        sin(time * 0.7 + nebula3 * 3.14) * 0.1
    );
    
    // Aumentar intensidad en zonas densas de nebulosa
    float density = (nebula1 + nebula2 + nebula3) / 3.0;
    nebulaColor *= 1.0 + density * 0.5;
    
    // Crear campo de estrellas con múltiples capas
    vec3 starPos1 = pos * 15.0;
    vec3 starPos2 = pos * 25.0 + vec3(100.0);
    vec3 starPos3 = pos * 40.0 + vec3(200.0);
    
    float starField = stars(starPos1, 0.995) * 0.8;
    starField += stars(starPos2, 0.997) * 0.6;
    starField += stars(starPos3, 0.998) * 1.0;
    
    // Color de estrellas (blanco brillante con tinte azulado)
    vec3 starColor = vec3(1.0, 0.95, 0.9) * starField;
    
    // Añadir algunas estrellas de colores
    float coloredStars = stars(pos * 20.0, 0.998);
    if(coloredStars > 0.5) {
        float starHue = hash(floor(pos * 20.0));
        if(starHue < 0.33)
            starColor += vec3(0.8, 0.4, 0.4) * coloredStars; // Estrellas rojizas
        else if(starHue < 0.66)
            starColor += vec3(0.4, 0.6, 1.0) * coloredStars; // Estrellas azules
        else
            starColor += vec3(1.0, 0.9, 0.5) * coloredStars; // Estrellas amarillas
    }
    
    // Combinar nebulosas y estrellas
    vec3 cosmicColor = nebulaColor + starColor;
    
    // Añadir regiones más brillantes (núcleos de nebulosa)
    float brightCore = pow(density, 3.0);
    cosmicColor += vec3(0.6, 0.3, 0.8) * brightCore * 0.5;
    
    // Efecto de profundidad basado en la posición
    float depth = sin(pos.x * 0.5 + time * 0.2) * cos(pos.z * 0.5 - time * 0.15);
    cosmicColor *= 0.8 + depth * 0.2;
    
    // Mezclar sutilmente con la textura original
    vec3 texColor = texture(tex0, fragTexCoords).rgb;
    vec3 finalColor = mix(cosmicColor, texColor * cosmicColor, 0.2);
    
    fragColor = vec4(finalColor, 1.0);
}
'''


# NUEVO SHADER 3: Procedural Pattern Shader - Patrones geométricos complejos
pattern_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform float time;
uniform sampler2D tex0;

// Función de ruido simplificado
float noise(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

// Patrón de Voronoi simplificado
float voronoi(vec2 p) {
    vec2 n = floor(p);
    vec2 f = fract(p);
    
    float minDist = 1.0;
    for(int j = -1; j <= 1; j++) {
        for(int i = -1; i <= 1; i++) {
            vec2 neighbor = vec2(float(i), float(j));
            vec2 point = noise(n + neighbor) * vec2(
                sin(time + noise(n + neighbor) * 6.28),
                cos(time + noise(n + neighbor) * 6.28)
            );
            vec2 diff = neighbor + point - f;
            float dist = length(diff);
            minDist = min(minDist, dist);
        }
    }
    return minDist;
}

// Patrón de cuadrícula hexagonal
float hexPattern(vec2 p) {
    p *= 8.0;
    vec2 s = vec2(1.0, 1.732);
    vec2 a = mod(p, s) - s * 0.5;
    vec2 b = mod(p - s * 0.5, s) - s * 0.5;
    return min(dot(a, a), dot(b, b));
}

void main()
{
    // Coordenadas para los patrones
    vec2 uv = fragPosition.xz * 2.0 + time * 0.1;
    
    // Combinar múltiples patrones
    float pattern1 = voronoi(uv * 3.0);
    float pattern2 = hexPattern(fragPosition.xy * 10.0 + time * 0.2);
    float pattern3 = sin(fragPosition.x * 10.0 + time) * cos(fragPosition.y * 10.0 - time);
    
    // Crear ondas circulares
    float dist = length(fragPosition.xz);
    float circles = sin(dist * 15.0 - time * 3.0) * 0.5 + 0.5;
    
    // Combinar patrones con pesos animados
    float combined = pattern1 * 0.3 + 
                     pattern2 * 0.3 + 
                     (pattern3 * 0.5 + 0.5) * 0.2 + 
                     circles * 0.2;
    
    // Colorear basado en los patrones
    vec3 color1 = vec3(0.2, 0.5, 1.0); // Azul
    vec3 color2 = vec3(1.0, 0.3, 0.5); // Rosa
    vec3 color3 = vec3(0.3, 1.0, 0.5); // Verde
    
    vec3 patternColor = mix(color1, color2, combined);
    patternColor = mix(patternColor, color3, sin(time + combined * 3.14) * 0.5 + 0.5);
    
    // Mezclar con textura base
    vec3 texColor = texture(tex0, fragTexCoords).rgb;
    vec3 finalColor = mix(texColor * 0.3, patternColor, 0.8);
    
    // Añadir brillo en las líneas del patrón
    float edge = smoothstep(0.45, 0.5, combined);
    finalColor += vec3(1.0) * edge * 0.5;
    
    fragColor = vec4(finalColor, 1.0);
}
'''









