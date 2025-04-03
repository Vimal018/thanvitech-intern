import cv2
import numpy as np

# Load trained LBPH Face Recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')  # Path to the trained model

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def face_detection():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            
            # Predict the face using the recognizer
            face_id, confidence = recognizer.predict(face_img)
            
            # Handle predictions and display
            if confidence < 100:
                label = f"ID: {face_id}, Confidence: {round(100 - confidence)}%"
            else:
                label = "Unknown"
            
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        cv2.imshow('Face Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    face_detection()
