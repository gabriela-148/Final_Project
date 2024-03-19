# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # at the command prompt type:
    # pip install opencv-python

    # OpenCV is a library of programming functions for computer vision applications
    import cv2
    import numpy as np

    # Load the image
    image = cv2.imread('grid40x40.jpg')

    # Check if the image was loaded successfully
    if image is None:
        print("Error: Unable to load image.")
        exit(1)

    # Resize the image to 50x50
    resized_image = cv2.resize(image, (50, 50))

    # Convert the resized image to grayscale
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Threshold the image
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Invert the binary image
    binary = cv2.bitwise_not(binary)

    # Convert the binary image to a matrix of 0s and 1s
    matrix = (binary / 255).astype(int)

    # Save the matrix into a text file
    np.savetxt('floorplan_matrix.txt', matrix, fmt='%d')

    print("Matrix saved to floorplan_matrix.txt")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
