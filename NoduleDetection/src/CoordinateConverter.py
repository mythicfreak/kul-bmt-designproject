from numpy import linalg as la
import numpy as np

class CoordinateConverter:
    def __init__(self, matrix): 
        self.Matrix = matrix;
        self.Inverse = la.inv(matrix)
    
    def getPixelZ(self, worldZ):
        #dz = self.Slices[0].SliceThickness;
        #return (worldZ - self.getMinZ() + dz/2) / dz
        return self.getPixelVector([0, 0, worldZ, 1])[2]

    def getWorldZ(self, pixelZ):
        #dz = self.Slices[0].SliceThickness;
        #return pixelZ * dz + self.getMinZ() - dz/2
        return self.getWorldVector([0, 0, pixelZ, 1])[2]

    def getPixelVector(self, worldVector):
        if len(worldVector) == 3:
            worldVector = np.append(worldVector, 1)
        assert len(worldVector) == 4
        return np.dot(self.Inverse, worldVector).A1
    
    def getWorldVector(self, pixelVector):
        if len(pixelVector) == 3:
            pixelVector = np.append(pixelVector, 1)
        assert len(pixelVector) == 4
        return np.dot(self.Matrix, pixelVector).A1