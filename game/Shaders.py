from OpenGL.GL import *
from OpenGL.GLE import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders

shaderProgram = None


def loadShaders():
    global shaderProgram
    vertexShader = shaders.compileShader("""
    #version 330 core

    // Input vertex data, different for all executions of this shader.
    layout(location = 0) in vec3 vertexPosition_modelspace;
    layout(location = 1) in vec2 vertexUV;
    layout(location = 2) in vec3 vertexNormal_modelspace;

    // Output data ; will be interpolated for each fragment.
    out vec2 UV;
    out vec3 Position_worldspace;
    out vec3 Normal_cameraspace;
    out vec3 EyeDirection_cameraspace;
    out vec3 LightDirection_cameraspace;

    // Values that stay constant for the whole mesh.
    uniform mat4 Projection;
    uniform mat4 View;
    uniform mat4 Model;
    uniform vec3 LightPosition_worldspace;

    void main(){

        // Output position of the vertex, in clip space : MVP * position
        gl_Position =  Projection * View * Model * vec4(vertexPosition_modelspace,1);

        // Position of the vertex, in worldspace : Model * position
        Position_worldspace = (Model * vec4(vertexPosition_modelspace,1)).xyz;

        // Vector that goes from the vertex to the camera, in camera space.
        // In camera space, the camera is at the origin (0,0,0).
        vec3 vertexPosition_cameraspace = ( View * Model * vec4(vertexPosition_modelspace,1)).xyz;
        EyeDirection_cameraspace = vec3(0,0,0) - vertexPosition_cameraspace;

        // Vector that goes from the vertex to the light, in camera space. M is ommited because it's identity.
        vec3 LightPosition_cameraspace = ( View * vec4(LightPosition_worldspace,1)).xyz;
        LightDirection_cameraspace = LightPosition_cameraspace + EyeDirection_cameraspace;

        // Normal of the the vertex, in camera space
        Normal_cameraspace = ( View * Model * vec4(vertexNormal_modelspace,0)).xyz; // Only correct if ModelMatrix does not scale the model ! Use its inverse transpose if not.

        // UV of the vertex. No special space for this one.
        UV = vertexUV;
    }
    """, GL_VERTEX_SHADER)

    fragmentShader = shaders.compileShader("""
    #version 330 core

    // Interpolated values from the vertex shaders
    in vec2 UV;
    in vec3 Position_worldspace;
    in vec3 Normal_cameraspace;
    in vec3 EyeDirection_cameraspace;
    in vec3 LightDirection_cameraspace;

    // Ouput data
    out vec3 color;

    // Values that stay constant for the whole mesh.
    uniform sampler2D myTextureSampler;
    uniform vec3 LightPosition_worldspace;
    uniform vec3 LightColor;
    uniform int LightPower;

    uniform vec3  MaterialDiffuseColor;
    uniform vec3  MaterialAmbientColor;
    uniform vec3  MaterialSpecularColor;

    void main(){
        // Material properties
        vec3 MaterialDiffuseColor = MaterialDiffuseColor * texture( myTextureSampler, UV ).rgb;
        vec3 MaterialAmbientColor = MaterialAmbientColor * MaterialDiffuseColor;
        vec3 MaterialSpecularColor = MaterialSpecularColor;

        // Distance to the light
        float distance = length( LightPosition_worldspace - Position_worldspace );

        // Normal of the computed fragment, in camera space
        vec3 n = normalize( Normal_cameraspace );
        // Direction of the light (from the fragment to the light)
        vec3 l = normalize( LightDirection_cameraspace );
        // Cosine of the angle between the normal and the light direction,
        // clamped above 0
        //  - light is at the vertical of the triangle -> 1
        //  - light is perpendicular to the triangle -> 0
        //  - light is behind the triangle -> 0
        float cosTheta = clamp( dot( n,l ), 0,1 );

        // Eye vector (towards the camera)
        vec3 E = normalize(EyeDirection_cameraspace);
        // Direction in which the triangle reflects the light
        vec3 R = reflect(-l,n);
        // Cosine of the angle between the Eye vector and the Reflect vector,
        // clamped to 0
        //  - Looking into the reflection -> 1
        //  - Looking elsewhere -> < 1
        float cosAlpha = clamp( dot( E,R ), 0,1 );

        color =
            // Ambient : simulates indirect lighting
            MaterialAmbientColor +
            // Diffuse : "color" of the object
            MaterialDiffuseColor * LightColor * LightPower * cosTheta / (distance*distance) +
            // Specular : reflective highlight, like a mirror
            MaterialSpecularColor * LightColor * LightPower * pow(cosAlpha,5) / (distance*distance);

    }
    """, GL_FRAGMENT_SHADER)
    shaderProgram = shaders.compileProgram(vertexShader, fragmentShader)
