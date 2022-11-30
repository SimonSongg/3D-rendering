from math import *

import numpy as np
import pygame

from utils import readFile, vertex, surface, sameSide

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

DARKBLUE = (0, 0, 95)  # #00005F
LIGHTBLUE = (0, 0, 255)  # #0000FF

WIDTH, HEIGHT = 400, 300
pygame.display.set_caption("3D Rendering for Neocis")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Variable initialize
scale = 50

circle_pos = [WIDTH / 2, HEIGHT / 2]  # x, y

angle = 0

points = []  # this will store all the vertices

mouseX = 0
mouseY = 0
angleX = 0
angleY = 0

normal = []

# Object file read in
objectpath = "./object.txt"
points, faceCoor = readFile(objectpath)

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])

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

    # Calculate the transformation of points
    i = 0
    for point in points:
        rotated2d = np.dot(rotation_x, point.array)
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_z, rotated2d)
        # Store the current position
        points[i].array = np.array([[float(rotated2d[0][0])], [float(rotated2d[1][0])], [float(rotated2d[2][0])]])
        # Project to canvas and make it center
        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(-projected2d[1][0] * scale) + circle_pos[1]

        point.trans = [float(rotated2d[0][0] * scale + circle_pos[0]), float(-rotated2d[1][0] * scale + circle_pos[1]),
                       float(rotated2d[2][0] * scale)]

        pygame.draw.circle(screen, RED, (x, y), 5)
        i += 1

    # Create a zBuffer for correct rendering order
    zBuffer = np.full((WIDTH * HEIGHT), float("-inf"))

    # True Redering starts from here!
    for face in faceCoor:
        # Determine the range of rasterization
        minX = max(0, ceil(min(face.vertexA.trans[0], min(face.vertexB.trans[0], face.vertexC.trans[0]))))
        minY = max(0, ceil(
            min(face.vertexA.trans[1], min(face.vertexB.trans[1], face.vertexC.trans[1]))))

        maxX = min(WIDTH - 1, floor(max(face.vertexA.trans[0], max(face.vertexB.trans[0], face.vertexC.trans[0]))))
        maxY = min(HEIGHT - 1, floor(max(face.vertexA.trans[1], max(face.vertexB.trans[1], face.vertexC.trans[1]))))

        # Calculate the normal vector for current surface
        vec1 = face.vertexB.getvector(face.vertexA)
        vec2 = face.vertexC.getvector(face.vertexA)
        norm = np.cross(vec1, vec2)
        # Normalize it
        normallenth = sqrt(norm[0] * norm[0] + norm[1] * norm[1] + norm[2] * norm[2])
        norm = norm / normallenth
        # Use Z value is OK
        angleCos = abs(norm[2])

        # Process each pixel in the bounding box
        for y in range(minY, maxY):
            for x in range(minX, maxX):
                sample = [x, y, 0]

                # Check if the point [x, y] in the surface
                V1 = sameSide(face.vertexA, face.vertexB, face.vertexC, sample)
                V2 = sameSide(face.vertexB, face.vertexC, face.vertexA, sample)
                V3 = sameSide(face.vertexC, face.vertexA, face.vertexB, sample)

                if V1 and V2 and V3:  # Checked! On surface! Started check occlusion

                    depth = face.vertexA.trans[2] + face.vertexB.trans[2] + face.vertexC.trans[2]
                    zIndex = y * WIDTH + x

                    if zBuffer[zIndex] < depth:
                        # If this point is more close to the canvas, draw this
                        # The color is determined by the angle of viewing
                        screen.set_at((x, y), (0, 0, 95 + 160 * angleCos))
                        zBuffer[zIndex] = depth

    pygame.display.update()
