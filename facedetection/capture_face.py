import cv2
import os

# Directory to save captured face images
dataset_path = 'dataset'

# Ensure the dataset directory exists
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)
    print(f"Directory '{dataset_path}' created.")

def capture_faces():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    teacher_name = input("Enter teacher's name (q to quit): ").strip()
    if teacher_name.lower() == 'q':
        print("Exiting...")
        cap.release()
        cv2.destroyAllWindows()
        return
    
    count = 0  # To keep track of the number of images captured
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from webcam")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            
            # Generate filename for the image
            image_filename = os.path.join(dataset_path, f"{teacher_name}_{count}.jpg")
            cv2.imwrite(image_filename, face_img)
            print(f"Image saved as {image_filename}")
            
            count += 1
            
            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, teacher_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
        # Display the frame
        cv2.imshow('Capture Faces', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_faces()
