import os
import re
import cv2
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def extract_year(filename):
    match = re.search(r'\d{4}', filename)
    return int(match.group()) if match else None

def get_closest_years(input_year, num_years, available_years):
    past_years = [year for year in available_years if year < input_year]
    past_years.sort(reverse=True)
    return past_years[:num_years] if past_years else [max(available_years)]

def compute_deforestation_loss(img1, img2):
    img1_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    img2_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    
    vegetation_mask1 = img1_hsv[:, :, 1] > 60
    vegetation_mask2 = img2_hsv[:, :, 1] > 60
    
    vegetation_loss = np.logical_and(vegetation_mask2, np.logical_not(vegetation_mask1))
    afforestation_gain = np.logical_and(vegetation_mask1, np.logical_not(vegetation_mask2))
    
    loss_percentage = (np.sum(vegetation_loss) / vegetation_loss.size) * 100
    gain_percentage = (np.sum(afforestation_gain) / afforestation_gain.size) * 100
    
    diff_img = np.zeros_like(img1[:, :, 0])
    diff_img[vegetation_loss] = 255  
    
    if gain_percentage > loss_percentage:
        return 0, "Afforestation detected", diff_img
    else:
        return loss_percentage, "Deforestation detected" if loss_percentage > 5 else "No major deforestation detected", diff_img

def display_images(input_img, past_img, diff_img, year, input_year):
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(past_img, cv2.COLOR_BGR2RGB))
    plt.title(f'Image from {year}')
    
    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB))
    plt.title(f'Image from {input_year}')
    
    plt.subplot(1, 3, 3)
    plt.imshow(diff_img, cmap='hot')
    plt.title('Vegetation Changes')
    plt.show()

def get_latest_processed_image():
    """Finds the latest processed image matching *_latest_processed.jpg."""
    files = sorted(glob("*_latest_processed.jpg"), key=os.path.getmtime, reverse=True)
    return files[0] if files else None

def analyze_deforestation(input_image_path, image_folder, num_years):
    input_year = extract_year(os.path.basename(input_image_path))
    if input_year is None:
        print("Year not found in filename!")
        return
    
    available_images = glob(os.path.join(image_folder, '*.jpg'))
    available_years = sorted(set(extract_year(os.path.basename(img)) for img in available_images if extract_year(os.path.basename(img)) is not None))
    
    if not available_years:
        print("No historical images available.")
        return
    
    closest_years = get_closest_years(input_year, num_years, available_years)
    print(f"Comparing {input_year} with {closest_years}")
    
    input_img = cv2.imread(input_image_path)
    
    for year in closest_years:
        past_img_path = next((img for img in available_images if extract_year(os.path.basename(img)) == year), None)
        if past_img_path:
            past_img = cv2.imread(past_img_path)
            loss, status, diff_img = compute_deforestation_loss(input_img, past_img)
            print(f"Comparison {year} to {input_year}: {status} ({loss:.2f}% loss)")
            display_images(input_img, past_img, diff_img, year, input_year)
        else:
            print(f"No image found for year {year}.")
        
    input_year = extract_year(os.path.basename(input_image_path))
    if input_year is None:
        print("Year not found in filename!")
        return
    
    available_images = glob(os.path.join(image_folder, '*.jpg'))
    available_years = sorted(set(extract_year(os.path.basename(img)) for img in available_images if extract_year(os.path.basename(img)) is not None))
    
    if not available_years:
        print("No historical images available.")
        return
    
    earliest_year = min(available_years)  # Get the oldest available year
    earliest_image_path = next((img for img in available_images if extract_year(os.path.basename(img)) == earliest_year), None)

    if earliest_image_path:
        print(f"Comparing overall deforestation from {earliest_year} to {input_year}...")
        
        earliest_img = cv2.imread(earliest_image_path)
        input_img = cv2.imread(input_image_path)
        
        overall_loss, overall_status, overall_diff_img = compute_deforestation_loss(input_img, earliest_img)
        
        print(f"Overall Deforestation from {earliest_year} to {input_year}: {overall_status} ({overall_loss:.2f}% loss)")
        display_images(input_img, earliest_img, overall_diff_img, earliest_year, input_year)
    else:
        print("No earliest historical image found.")

if __name__ == "__main__":
    latest_processed_image = get_latest_processed_image()
    if latest_processed_image:
        image_folder = "SENTINEL_2_processed"
        num_years = int(input("Enter number of years to check: "))
        analyze_deforestation(latest_processed_image, image_folder, num_years)
    else:
        print("No processed image found matching '*_latest_processed.jpg'.")
