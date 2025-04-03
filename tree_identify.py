import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def process_forest_detection(input_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Define green color range for forests
    lower_green = np.array([25, 40, 20])  # Lower bound of green
    upper_green = np.array([100, 255, 255])  # Upper bound of green
    
    # Process each image in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            
            if image is None:
                print(f"Error: Could not load {filename}. Skipping...")
                continue
            
            # Convert to HSV color space
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Create a mask for green areas
            mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Apply the mask to the image
            result = cv2.bitwise_and(image, image, mask=mask)
            
            # Save the output image
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, result)
            print(f"Processed: {filename} -> {output_path}")
            
            # Display results
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.title("Original Image")
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            plt.subplot(1, 2, 2)
            plt.title("Detected Forest Areas")
            plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
            plt.show()

# Example usage
input_folder = "SENTINEL_2"
output_folder = "SENTINEL_2_processed"
process_forest_detection(input_folder, output_folder)
