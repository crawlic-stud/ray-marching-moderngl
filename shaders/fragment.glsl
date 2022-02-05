#version 330 core
#include hg_sdf.glsl
layout(location = 0) out vec4 fragColor;

const float FOV = 1.0;
const int MAX_STEPS = 256;
const float MAX_DIST = 500;
const float EPSILON = 0.001;
const int ARRAY_SIZE = 50;

uniform float sphere_radius;
uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform vec3 random_array[ARRAY_SIZE];


vec2 fOpUnionID(vec2 res1, vec2 res2) {
    return (res1.x < res2.x) ? res1 : res2;
}

vec2 fOpDifferenceID(vec2 res1, vec2 res2) {
    return (res1.x > res2.x) ? res1 : vec2(-res2.x, res2.y);
}

vec2 map(vec3 p) {

    // plane
    float planeDist = fPlane(p, vec3(0, 1, 0), 1.0);
    float planeID = 2.0;
    vec2 plane = vec2(planeDist, planeID);

    // box
    float boxDist = fBox(p, vec3(0.5, 1, 0.5));
    float boxID = 3.0;
    vec2 box = vec2(boxDist, boxID);

    // spheres
    vec2 spheres = fOpUnionID(box, plane);
    float sphereID = 1.0;

    for (int i = 0; i < ARRAY_SIZE; i++) {
        vec3 offset = vec3(i, i, i);
        float sphereDist = fSphere(p + random_array[i], sphere_radius);
        vec2 sphere = vec2(sphereDist, sphereID);
        spheres = fOpUnionID(spheres, sphere);
    }

    // result
    vec2 res;
    res = spheres;

    return res;
}

vec2 rayMarch(vec3 ro, vec3 rd) {
    vec2 hit, object;
    for (int i = 0; i < MAX_STEPS; i++) {
        vec3 p = ro + object.x * rd;
        hit = map(p);
        object.x += hit.x;
        object.y = hit.y;
        if (abs(hit.x) < EPSILON || object.x > MAX_DIST) break;
    }
    return object;
}

vec3 getNormal(vec3 p) {
    vec2 e = vec2(EPSILON, 0.0);
    vec3 n = vec3(map(p).x) - vec3(map(p - e.xyy).x, map(p - e.yxy).x, map(p - e.yyx).x);
    return normalize(n);
}

vec3 getLight(vec3 p, vec3 rd, vec3 color) {
    vec3 lightPos = vec3(30.0, 40.0, -30.0);
    vec3 L = normalize(lightPos - p);
    vec3 N = getNormal(p);
    vec3 V = -rd;
    vec3 R = reflect(-L, N);

    // light for reflective surface
    vec3 specColor = vec3(0.2);
    vec3 specular = specColor * pow(clamp(dot(R, V), 0.0, 1.0), 10.0);
    vec3 diffuse = color * clamp(dot(L, N), 0.0, 1.0);
    vec3 ambient = color * 0.05;

    // shadows
    float d = rayMarch(p + N * 0.02, normalize(lightPos)).x;
    if (d < length(lightPos - p)) return ambient;

    return diffuse + ambient + specular;
}

vec3 getMaterial(vec3 p, float id) {
    // material
    vec3 m;
    switch (int(id)) {
        case 1:
        m = vec3(0.9, 0.9, 0); break;
        case 2:
        m = vec3(0.2 + 0.4 * mod(floor(p.x) + floor(p.z), 2.0)); break;
    }
    return m;
}

mat3 getCam(vec3 ro, vec3 lookAt) {
    // forward, right and up
    vec3 camF = normalize(vec3(lookAt - ro));
    vec3 camR = normalize(cross(vec3(0, 1, 0), camF));
    vec3 camU = cross(camF, camR);
    return mat3(camR, camU, camF);
}

void mouseControl(inout vec3 ro) {
    vec2 m = u_mouse / u_resolution;
    // camera rotation with a mouse
    pR(ro.yz, m.y * PI * 0.5 - 0.5);
    pR(ro.xz, m.x * TAU);
}

void render(inout vec3 col, in vec2 uv) {
    // camera position
    vec3 ro = vec3(3.0, 3.0, -5.0);
    mouseControl(ro);

    // where camera pointed
    vec3 lookAt = vec3(0, 0, 0);
    vec3 rd = getCam(ro, lookAt) * normalize(vec3(uv, FOV));

    vec2 object = rayMarch(ro, rd);

    vec3 background = vec3(0.5, 0.5, 0.9);
    if (object.x < MAX_DIST) {
        vec3 p = ro + object.x * rd;
        vec3 material = getMaterial(p, object.y);
        col += getLight(p, rd, material);
        //col += material;
        // fog
        col = mix(col, background, 1.0 - exp(-0.0008 * object.x * object.x));
    } else {
        col += background - max(0.95 * rd.y, 0.0);
    }

}

void main() {
    vec2 uv = (2.0 * gl_FragCoord.xy - u_resolution.xy) / u_resolution.y;

    // pixel color
    vec3 col;
    render(col, uv);

    // gamma correction
    col = pow(col, vec3(0.4545));
    fragColor = vec4(col, 1.0);
}