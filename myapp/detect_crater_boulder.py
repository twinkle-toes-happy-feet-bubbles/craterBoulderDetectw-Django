import cv2
import numpy as np
from datetime import datetime
import os

def detect_crater_or_boulder(image_path, output_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    color_image = cv2.imread(image_path)  # Load the color image for annotation
    
    # Ensure images are loaded correctly
    if image is None or color_image is None:
        print(f"Error loading image from {image_path}")
        return
    
    image_blur = cv2.GaussianBlur(image, (5, 5), 0)
    
    # Apply thresholding
    _, thresh = cv2.threshold(image_blur, 128, 255, cv2.THRESH_BINARY)
    
    # Detect edges using Canny
    edges = cv2.Canny(thresh, 100, 200)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    crater_count = 0
    boulder_count = 0
    
    for contour in contours:
        # Get the bounding box
        x, y, w, h = cv2.boundingRect(contour)
        
        # Extract the region of interest
        roi = image[y:y+h, x:x+w]
        
        # Ensure ROI is not empty
        if roi.size == 0:
            continue
        
        # Analyze the brightness
        center_brightness = np.mean(roi[h//4:3*h//4, w//4:3*w//4])
        edge_brightness = (np.mean(roi[:h//4, :]) + np.mean(roi[3*h//4:, :]) + 
                           np.mean(roi[:, :w//4]) + np.mean(roi[:, 3*w//4:])) / 4
        
        # Determine if it's a crater or boulder
        if center_brightness < edge_brightness:
            crater_count += 1
            # Draw a circle around the crater
            center = (x + w//2, y + h//2)
            radius = max(w, h) // 2
            cv2.circle(color_image, center, radius, (255, 0, 0), 2)  # Blue circle for craters
        else:
            boulder_count += 1
            # Draw a green rectangle around the boulder
            cv2.rectangle(color_image, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Green rectangle for boulders
    
    # Add date and time to the image
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(color_image, date_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Save the annotated image
    cv2.imwrite(output_path, color_image)
    
    # Construct a message
    message = f"Detected {crater_count} craters and {boulder_count} boulders."

    return output_path, message
