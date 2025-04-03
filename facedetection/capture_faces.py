import cv2
import numpy as np
import mysql.connector
import bcrypt

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'attendance_system'
}

try:
    # Connect to MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Connected to MySQL database")
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit(1)

# Initialize LBPH Face Recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def capture_faces():
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from webcam")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            
            # Convert face_img to bytes for storing in MySQL
            _, img_encoded = cv2.imencode('.jpg', face_img)
            img_bytes = img_encoded.tobytes()
            
            # Prompt user to enter teacher's name and password
            teacher_name = input("Enter teacher's name (q to quit): ").strip()
            if teacher_name.lower() == 'q':
                break
            
            password = input("Enter password for this teacher: ").strip()
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            try:
                # Store face image and hashed password in the database
                insert_query = "INSERT INTO teacher (name, face_image, password) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (teacher_name, img_bytes, hashed_password.decode('utf-8')))
                conn.commit()
                print(f"Face captured and stored for {teacher_name}")
                
                # Draw rectangle around the face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, teacher_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                
            except mysql.connector.Error as err:
                print(f"Error storing face in MySQL: {err}")
        
        cv2.imshow('Capture Faces', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    capture_faces()
