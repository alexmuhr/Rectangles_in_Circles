import numpy as np
import cv2
import math

diameter = int(float(input("Enter Wafer Diameter (mm): "))*10)
rectw = int(float(input("Enter Part Width (mm): "))*10)
recth = int(float(input("Enter Part Height (mm): "))*10)

# Define a function that creates a black canvas with a white circle
def blank_canvas(diameter):
    centerpoint = int(diameter/2)
    canvas = np.full((diameter, diameter), 0, np.uint8) # Creates a black background
    # Then draw a white circle over the canvas
    cv2.circle(canvas, (centerpoint,centerpoint), centerpoint, (255,255,255), -1) # Draw a filled white circle
    return canvas

# Define function to draw array with black lines
def draw_lines(canvas, nw, nh, rectw, recth, offsetw, offseth):
    for i in range(nw+1):
        canvas[:,i*rectw+offsetw] = 0
    for i in range(nh+1):
        canvas[i*recth+offseth,:] = 0
    return canvas

# Define function that counts the number of complete parts in a particular configuration
def count_completes(canvas, rectw, recth):
    # Find Contours on image of circle with array
    (_,cnts,_) = cv2.findContours(canvas.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Set completes equal to zero
    completes = 0
    for contour in cnts:
        if cv2.contourArea(contour) == (rectw-2)*(recth-2):
            completes = completes + 1
    return completes


# Determine array of rectangles that will fit over canvas
nw = math.floor(diameter/rectw)
nh = math.floor(diameter/recth)

# Determine remainder distance for width and height of array on canvas
rw = diameter%(rectw)
rh = diameter%(recth)

for i in range(int(rw/5)):
    for j in range(int(rh/5)):
        max = 0
        canvas = blank_canvas(diameter)
        canvas = draw_lines(canvas, nw, nh, rectw, recth, 5*i, 5*j)
        completes = count_completes(canvas, rectw, recth)
        if completes > max:
            max = completes
            maxoffsetw = 5*i
            maxoffseth = 5*j

print(max, maxoffsetw, maxoffseth)

canvas = blank_canvas(diameter)
canvas = draw_lines(canvas, nw, nh, rectw, recth, maxoffsetw, maxoffseth)
cv2.imshow("max_yield", canvas)
cv2.waitKey(0)
