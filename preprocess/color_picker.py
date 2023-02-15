import cv2

# Load the image
image = cv2.imread(
    "data/helsinki2019/color_masks/kuusi_1519_24.935997999999998_60.18871_24.940472_60.191871.png"
)


# Define the mouse callback function
def pick_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        color = image[y, x]
        print(f"RGB color at ({x}, {y}): {color}")


# Create a window and display the image
cv2.namedWindow("Image")
cv2.imshow("Image", image)

# Set the mouse callback function for the window
cv2.setMouseCallback("Image", pick_color)

# Wait for the user to click a mouse button
cv2.waitKey(0)

# Close the window
cv2.destroyAllWindows()