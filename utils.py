import numpy as np

objectpath = "./object.txt"


class vertex(object):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.array = np.array([[x], [y], [z]])
        self.trans = [0, 0, 0]
        self.projected = [0, 0]

    def getvector(self, another):
        return [self.trans[0] - another.trans[0], self.trans[1] - another.trans[1], self.trans[2] - another.trans[2]]


class surface(object):

    def __init__(self, vertexA, vertexB, vertexC):
        self.vertexA = vertexA
        self.vertexB = vertexB
        self.vertexC = vertexC


def readFile(path):
    ##Open the object file
    f = open(path)
    line = f.readline()
    line = line.strip()
    len = line.split(',')
    # number of vertice and face
    nVertice = int(len[0])
    nFace = int(len[1])

    # create array to store coordinates of the vertices and face
    # verticeCoor = [[0.0] * 3 for i in range(nVertice)]
    # faceCoor = [[0] * 3 for i in range(nFace)]
    verticeCoor = []
    faceCoor = []
    for i in range(0, nVertice):
        line = f.readline()
        line = line.strip()
        len = line.split(',')
        # verticeCoor[i][0] = float(len[1])
        # verticeCoor[i][1] = float(len[2])
        # verticeCoor[i][2] = float(len[3])

        verticeCoor.append(vertex(float(len[1]), float(len[2]), float(len[3])))

    for i in range(0, nFace):
        line = f.readline()
        line = line.strip()
        len = line.split(',')
        # faceCoor[i][0] = int(len[0])-1
        # faceCoor[i][1] = int(len[1])-1
        # faceCoor[i][2] = int(len[2])-1
        faceCoor.append(
            surface(verticeCoor[int(len[0]) - 1], verticeCoor[int(len[1]) - 1], verticeCoor[int(len[2]) - 1]))
    f.close()
    return verticeCoor, faceCoor


def sameSide(VertexA, VertexB, VertexC, p):
    # VertexA = np.array(VertexA)
    # VertexB = np.array(VertexB)
    # VertexC = np.array(VertexC)

    V1V2 = [VertexB.trans[0] - VertexA.trans[0], VertexB.trans[1] - VertexA.trans[1],
            VertexB.trans[2] - VertexA.trans[2]]
    V1V3 = [VertexC.trans[0] - VertexA.trans[0], VertexC.trans[1] - VertexA.trans[1],
            VertexC.trans[2] - VertexA.trans[2]]
    V1p = [p[0] - VertexA.trans[0], p[1] - VertexA.trans[1], p[2] - VertexA.trans[2]]

    # V1V2 = VertexB-VertexA
    #
    # V1V3 = VertexC - VertexA
    #
    # V1p = p - VertexA

    z1 = V1V2[0] * V1V3[1] - V1V3[0] * V1V2[1]
    z2 = V1V2[0] * V1p[1] - V1p[0] * V1V2[1]

    return z1 * z2 >= 0

# ifFirst = False
# while line:
#     print(line)
#     if (not ifFirst):
#         line = line.strip()
#         len = line.split(',')
#         print(len)
#         ifFirst = True
#
#     line = f.readline()
