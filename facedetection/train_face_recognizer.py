import cv2
import numpy as np
import os

def get_images_and_labels(path):
    images = []
    labels = []
    label_map = {}
    label_counter = 0

    for filename in os.listdir(path):
        if filename.endswith('.jpg'):
            img_path = os.path.join(path, filename)
            # Read image in grayscale
            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if image is not None:
                # Extract label from filename (before the first underscore)
                base_name = filename.split('.')[0]  # Remove the extension
                if '_' in base_name:
                    label_name = base_name.split('_')[0]  # Get name before the underscore
                else:
                    label_name = base_name  # Use the whole base name if no underscore
                
                # Map label_name to a unique numeric label
                if label_name not in label_map:
                    label_map[label_name] = label_counter
                    label_counter += 1
                
                label = label_map[label_name]
                images.append(image)
                labels.append(label)
            else:
                print(f"Warning: Unable to read image {filename}")
    
    return images, labels, label_map

dataset_path = 'dataset'
print("Preparing data for training...")
images, labels, label_map = get_images_and_labels(dataset_path)

# Debug: Print number of images and labels
print(f"Number of images: {len(images)}")
print(f"Labels: {labels}")
print(f"Label map: {label_map}")

if len(images) > 0 and len(labels) > 0:
    # Initialize LBPH Face Recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    # Train the recognizer
    recognizer.train(images, np.array(labels))
    
    # Save the trained model
    trainer_path = 'trainer.yml'
    recognizer.save(trainer_path)
    print(f"Model trained and saved to {trainer_path}")
else:
    print("Error: No images or labels found. Ensure that the dataset directory is correctly populated.")
