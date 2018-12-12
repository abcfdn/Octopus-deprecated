import numpy as np
import cv2

img = cv2.imread('./images/example.png')

color = [247, 254, 255]
for col in range(790, 1000):
    for row in range(270, 1620):
        img[col][row] = color

for col in range(1080, 1200):
    for row in range(270, 1275):
        img[col][row] = color

for col in range(1260, 1380):
    for row in range(2200, 3040):
        img[col][row] = color

for col in range(1550, 1660):
    for row in range(2200, 3100):
        img[col][row] = color

cv2.imwrite('./images/template.png', img)
