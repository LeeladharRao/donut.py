import numpy as np
import os

# declaring global variables
screenSize = int(os.get_terminal_size().columns/1.2)
windowHeight = int(os.get_terminal_size().lines/1.2)
if (windowHeight < screenSize):
    screenSize = windowHeight

thetaSpacing = 0.07
phiSpacing = 0.01
illumination = np.fromiter(".,-~:;=!*#$@", dtype="<U1")

A = 1
B = 1
R1 = 1
R2 = 2
K2 = 5
K1 = screenSize * K2 * 3 / (8 * (R1 + R2))


def renderBox(A: float, B: float) -> np.ndarray:
    # defining the trignometric values
    cosA = np.cos(A)
    sinA = np.sin(A)
    cosB = np.cos(B)
    sinB = np.sin(B)

    cosPhi = np.cos(phi := np.arange(0, 2 * np.pi, phiSpacing)) 
    sinPhi = np.sin(phi)  
    cosTheta = np.cos(theta := np.arange(0, 2 * np.pi, thetaSpacing))  
    sinTheta = np.sin(theta) 
    circleX = R2 + R1 * cosTheta  
    circleY = R1 * sinTheta  

    x = (np.outer(cosB * cosPhi + sinA * sinB * sinPhi, circleX) - circleY * cosA * sinB).T 
    y = (np.outer(sinB * cosPhi - sinA * cosB * sinPhi, circleX) + circleY * cosA * cosB).T 
    z = ((K2 + cosA * np.outer(sinPhi, circleX)) + circleY * sinA).T  
    ooz = np.reciprocal(z)  

    xp = (screenSize / 2 + K1 * ooz * x).astype(int)  
    yp = (screenSize / 2 - K1 * ooz * y).astype(int) 
		
    L1 = (((np.outer(cosPhi, cosTheta) * sinB) - cosA * np.outer(sinPhi, cosTheta)) - sinA * sinTheta)  
    L2 = cosB * (cosA * sinTheta - np.outer(sinPhi, cosTheta * sinA)) 
    L = np.around(((L1 + L2) * 8)).astype(int).T 
    maskL = L >= 0 
    chars = illumination[L] 

    # defining the output screen size buffer
    output = np.full((screenSize, screenSize), " ")  
    zbuffer = np.zeros((screenSize, screenSize)) 

    for i in range(60):
        mask = maskL[i] & (ooz[i] > zbuffer[xp[i], yp[i]])  

        zbuffer[xp[i], yp[i]] = np.where(mask, ooz[i], zbuffer[xp[i], yp[i]])
        output[xp[i], yp[i]] = np.where(mask, chars[i], output[xp[i], yp[i]])

    return output


def printDonut(array: np.ndarray) -> None:
    print(*[" ".join(line) for line in array], sep="\n")


if __name__ == "__main__":
    while (1):
        A += thetaSpacing
        B += phiSpacing
        print("\x1b[H")
        printDonut(renderBox(A, B))
