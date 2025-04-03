import cv2
import numpy as np
import mysql.connector
from datetime import datetime

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

# Load trained LBPH Face Recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

# Load pre-trained Haar Cascade classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def mark_attendance(user_id):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    
    # Check if the user has already been marked present today
    check_query = "SELECT COUNT(*) FROM attendance WHERE user_id = %s AND date = %s"
    cursor.execute(check_query, (user_id, date))
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert attendance record
        insert_query = "INSERT INTO attendance (user_id, date, time) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (user_id, date, time))
        conn.commit()

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]
        
        # Perform liveliness check using eye detection
        eyes = eye_cascade.detectMultiScale(face_img)
        if len(eyes) == 0:
            continue  # Skip this face if no eyes are detected
        
        # Predict the face using the recognizer
        face_id, confidence = recognizer.predict(face_img)
        
        # Fetch the name from the database based on face_id
        query = "SELECT name FROM teacher WHERE id = %s"
        cursor.execute(query, (face_id,))
        result = cursor.fetchone()
        
        if result is not None:
            teacher_name = result[0]
            # Mark attendance for the recognized user
            mark_attendance(face_id)
        else:
            teacher_name = "Unknown"
        
        # Display name and confidence level
        if confidence < 100:
            cv2.putText(frame, f"{teacher_name} - Confidence: {round(100 - confidence)}%", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        
        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    return frame

def mark_attendance_system():
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from webcam")
            break
        
        # Process the frame
        frame = process_frame(frame)
        
        # Display the frame
        cv2.imshow('Mark Attendance', frame)
        
        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()
    
    # Close cursor and connection to MySQL
    cursor.close()
    conn.close()

if __name__ == "__main__":
    mark_attendance_system()
