import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, symbols, reflect ):
    r = symbols[reflect][1]
    a = calculate_ambient(ambient, r)
    i = [0, 0, 0]
    i[RED] = int(a[RED])
    i[GREEN] = int(a[GREEN])
    i[BLUE] = int(a[BLUE])
    for l in light:
        n = normal[:]
        normalize(n)
        normalize(l[LOCATION])
        normalize(view)

        d = calculate_diffuse(l, r, n)
        s = calculate_specular(l, r, view, n)

        i[RED] += int(d[RED] + s[RED])
        i[GREEN] += int(d[GREEN] + s[GREEN])
        i[BLUE] += int(d[BLUE] + s[BLUE])

    limit_color(i)

    return i

def calculate_ambient(alight, reflect):
    a = [0, 0, 0]
    a[RED] = alight[RED] * reflect['red'][AMBIENT]
    a[GREEN] = alight[GREEN] * reflect['green'][AMBIENT]
    a[BLUE] = alight[BLUE] * reflect['blue'][AMBIENT]
    return a

def calculate_diffuse(light, reflect, normal):
    d = [0, 0, 0]

    dot = dot_product( light[LOCATION], normal)

    dot = dot if dot > 0 else 0
    d[RED] = light[COLOR][RED] * reflect['red'][DIFFUSE] * dot
    d[GREEN] = light[COLOR][GREEN] * reflect['green'][DIFFUSE] * dot
    d[BLUE] = light[COLOR][BLUE] * reflect['blue'][DIFFUSE] * dot
    return d

def calculate_specular(light, reflect, view, normal):
    s = [0, 0, 0]
    n = [0, 0, 0]

    result = 2 * dot_product(light[LOCATION], normal)
    n[0] = (normal[0] * result) - light[LOCATION][0]
    n[1] = (normal[1] * result) - light[LOCATION][1]
    n[2] = (normal[2] * result) - light[LOCATION][2]

    result = dot_product(n, view)
    result = result if result > 0 else 0
    result = pow( result, SPECULAR_EXP )

    s[RED] = light[COLOR][RED] * reflect['red'][SPECULAR] * result
    s[GREEN] = light[COLOR][GREEN] * reflect['green'][SPECULAR] * result
    s[BLUE] = light[COLOR][BLUE] * reflect['blue'][SPECULAR] * result
    return s

def limit_color(color):
    color[RED] = 255 if color[RED] > 255 else color[RED]
    color[GREEN] = 255 if color[GREEN] > 255 else color[GREEN]
    color[BLUE] = 255 if color[BLUE] > 255 else color[BLUE]

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N

def calculate_vertex_normal(polygons, i):
    # print("#######################")
    # print("polygons[i]")
    # print(polygons[i])
    # print("#######################")

    adj_polygons = []

    for index in range(len(polygons)):
        if polygons[i]==polygons[index]:
            adj_polygons.append(polygons[index-(index%3)])
            adj_polygons.append(polygons[index-(index%3)+1])
            adj_polygons.append(polygons[index-(index%3)+2])

    adj_polygons = adj_polygons[3:]

    # print("ADJ_POLYGONS")
    # print(adj_polygons)
    # print("-----------------------------")

    vertex_normal = [0,0,0]
    num_adj = len(adj_polygons)/3
    for x in range(num_adj):
        temp_norm = calculate_normal(adj_polygons,x*3)
        vertex_normal[0]+=temp_norm[0]
        vertex_normal[1]+=temp_norm[2]
        vertex_normal[2]+=temp_norm[2]
    vertex_normal=[x/num_adj for x in vertex_normal[:]]

    # print("VERTEX NORMAL: ", vertex_normal)
    return vertex_normal
