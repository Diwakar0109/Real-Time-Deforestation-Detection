import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

def get_latest_image(pattern="*_latest.jpg"):
    """Find the latest image file matching the given pattern."""
    files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    return files[0] if files else None

def process_forest_detection(input_image):
    """Detect forested areas in an image and save the output."""
    lower_green = np.array([25, 40, 20])  # Lower bound of green in HSV
    upper_green = np.array([100, 255, 255])  # Upper bound of green in HSV
    
    image = cv2.imread(input_image)
    if image is None:
        print(f"Error: Could not load {input_image}.")
        return
    
    # Convert to HSV and create a mask for green areas
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    result = cv2.bitwise_and(image, image, mask=mask)
    
    # Generate output filename by appending "_processed" before ".jpg"
    output_image = input_image.replace(".jpg", "_processed.jpg")

    # Save processed image
    cv2.imwrite(output_image, result)
    print(f"Processed: {input_image} -> {output_image}")
    
    # Display results
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    plt.subplot(1, 2, 2)
    plt.title("Detected Forest Areas")
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.show()

# Find the latest image and process it
latest_image = get_latest_image()
if latest_image:
    process_forest_detection(latest_image)
else:
    print("No image matching '*_latest.jpg' found.")
