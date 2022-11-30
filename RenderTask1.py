import pygame
import numpy as np
from math import *
from utils import readFile, vertex, surface

WHITE = (255, 255, 255)

BLUE = (0, 0, 255)

WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("3D rendering for Neocis")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Variable initialize
scale = 100

circle_pos = [WIDTH / 2, HEIGHT / 2]  # x, y

angle = 0

points = [] # this will store all the vertices

mouseX = 0
mouseY = 0
angleX = 0
angleY = 0

# Object file read in
objectpath = "./object.txt"
points, faceCoor = readFile(objectpath)

projected_points = [
    [n, n] for n in range(len(points))
]

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])


def connect_points(i, j):
    pygame.draw.line(
        screen, BLUE, i, j)

# Ready to start rendering
isMouseFirstPress = True
clock = pygame.time.Clock()
while True:

    clock.tick(60)
    # If mouse press detected, read the mouse position (skip the first data to avoid large change)
    if pygame.mouse.get_pressed()[0]:
        mouseXtemp, mouseYtemp = pygame.mouse.get_rel()
        if isMouseFirstPress:
            isMouseFirstPress = False
        else:
            mouseX = mouseXtemp
            mouseY = mouseYtemp
    else:
        isMouseFirstPress = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scale = scale + 5
            elif event.button == 5:
                if scale > 5:
                    scale = scale - 5

    # Calculate the angle will be rotated
    angleX = mouseY * 0.005
    angleY = mouseX * 0.005

    # Start update
    # Define rotation matrix

    rotation_z = np.matrix([
        [cos(0), -sin(0), 0],
        [sin(0), cos(0), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angleY), 0, sin(angleY)],
        [0, 1, 0],
        [-sin(angleY), 0, cos(angleY)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angleX), -sin(angleX)],
        [0, sin(angleX), cos(angleX)],
    ])

    screen.fill(WHITE)
    # drawining stuff
    # Calculate the transformation of points and draw projected points on canvas
    i = 0
    print(len(points))
    for point in points:
        rotated2d = np.dot(rotation_x, rotation_y)
        rotated2d = np.dot(rotated2d, rotation_z)
        rotated2d = np.dot(rotated2d, point.array)
        # Store the current position
        points[i].array = np.array([[float(rotated2d[0][0])], [float(rotated2d[1][0])], [float(rotated2d[2][0])]])
        # Project to canvas and make it center
        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(-projected2d[1][0] * scale) + circle_pos[1]

        points[i].projected = [x, y]
        pygame.draw.circle(screen, BLUE, (x, y), 5)
        i += 1
    # Connected corresponding vertices on canvas
    for face in faceCoor:
        connect_points(face.vertexA.projected, face.vertexB.projected)
        connect_points(face.vertexA.projected, face.vertexC.projected)
        connect_points(face.vertexC.projected, face.vertexB.projected)

    pygame.display.update()
