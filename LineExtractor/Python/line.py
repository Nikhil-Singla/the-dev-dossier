import cv2
import os
import numpy as np
import json

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Image file name
image_file = "floor_plan.png"
output_file = "output.png"

# Image file path
image_path = os.path.join(current_dir, image_file)
output_path = os.path.join(current_dir, output_file)


# Check if the image file exists
if not os.path.isfile(image_path):
    raise FileNotFoundError(f"Image file '{image_file}' not found.")

def getWalls(image_path, threshold_area, canny_threshold1, canny_threshold2):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to segment the walls
    _, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Apply Canny edge detection to detect lines
    edges = cv2.Canny(thresholded, canny_threshold1, canny_threshold2)
    
    # Remove small components or noise from the detected lines
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(edges, connectivity=8)
    
    # Create a mask to filter out small components
    mask = np.zeros_like(labels, dtype=np.uint8)
    for label in range(1, num_labels):
        area = stats[label, cv2.CC_STAT_AREA]
        if area > threshold_area:
            mask[labels == label] = 255
    
    # Apply the mask to retain only the lines along the walls
    result = cv2.bitwise_and(edges, edges, mask=mask)
    
    # Perform morphological dilation to connect adjacent line segments
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    dilated = cv2.dilate(result, kernel, iterations=1)

    ##cv2.floodFill(dilated, mask=None, seedPoint=(int(0), int(0)), newVal=(255))

    # Display the resulting image
    cv2.imshow('Original Image', image)
    cv2.imshow('Lines along Walls', dilated)
    cv2.imwrite(output_path, dilated)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def reduction(pathToOutput):
    img = cv2.imread(pathToOutput, cv2.IMREAD_GRAYSCALE)

    # Set the desired thickness reduction factor
    thickness_reduction_factor = 9

    # Define the structuring element for erosion
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Perform erosion
    eroded_image = cv2.erode(img, kernel, iterations=thickness_reduction_factor)

    # Display the eroded image
    cv2.imshow("Eroded Image", eroded_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(output_path, eroded_image)

def detect_line_segments(image_path):
    # Load the image in grayscale
    image = cv2.imread(image_path, 0)

    # Apply Canny edge detection
    edges = cv2.Canny(image, 50, 150, apertureSize=3)

    # Perform Hough Line Transform
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=100, minLineLength=20, maxLineGap=10)

    # Process the detected lines
    dimensions = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            dimensions.append((x1, y1, x2, y2, length, angle))

    return dimensions

# Call the function to reduce the image to lines and label them

threshold_area = 90
canny_threshold1 = 10
canny_threshold2 = 10
thickness_reduction_factor = 1

# Call the function to remove background elements and retain lines along walls
getWalls(image_path, threshold_area, canny_threshold1, canny_threshold2)

reduction(output_path)

line_segments = detect_line_segments(output_path)
for segment in line_segments:
    x1, y1, x2, y2, length, angle = segment
    print(f"Start Point: ({x1}, {y1}), End Point: ({x2}, {y2}), Length: {length}, Angle: {angle}")

vertexName = "tZz4-vWqWF"

def generateVertex(xcor, ycor, inputLineIDList, vertexName="tZz4-vWqWF"):
    e = {}
    L = []
    verticeName = vertexName
    vertex = {
        "id": verticeName,
        "type": "",
        "prototype": "vertices",
        "name": "Vertex",
        "misc": e,
        "selected": False,
        "properties": e,
        "visible": True,
        "x" : xcor,
        "y" : ycor,
        "lines": inputLineIDList,
        "areas" : L
    }
    return vertex

def generate_COLverticesCOL():
    vertices = {
        "tZz4-vWqWF": generateVertex(600, 1800, ["line1"]),
        "t2z4-vWqWF": generateVertex(700, 1800, ["line3"]),
        # Add more vertices here
    }

    return vertices

xcor = 600
ycor = 1800
input_line_id = ["Xo4EUkJ-u"]

##vertex_json = json.dumps({"vertices": {"tZz4-vWqWF": generateVertex(xcor, ycor, input_line_id)}}, indent=4)
vertices_json = json.dumps({"vertices": generate_COLverticesCOL()}, indent=4)

print(vertices_json)


def generate_line(id, vertices, height, thickness=20, textureA="bricks", textureB="bricks"):
    line = {
        "id": id,
        "type": "wall",
        "prototype": "lines",
        "name": "Wall",
        "misc": {},
        "selected": False,
        "properties": {
            "height": {
                "length": height
            },
            "thickness": {
                "length": thickness
            },
            "textureA": textureA,
            "textureB": textureB
        },
        "visible": True,
        "vertices": vertices,
        "holes": []
    }
    return line

line_id = "YCelF6q2B"
vertices = ["tZz4-vWqWF", "nXLEHSkLdb"]
height = 300
thickness = 20
textureA = "bricks"
textureB = "bricks"

line_json = json.dumps({line_id: generate_line(line_id, vertices, height)}, indent=4)
print(line_json)