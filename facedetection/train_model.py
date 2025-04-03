import cv2
import os
import numpy as np
import mysql.connector

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

def train_model():
    faces = []
    face_ids = []

    # Read all images from the teachers table in the database
    query = "SELECT id, face_image FROM teacher"
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        face_id = row[0]
        face_img = np.frombuffer(row[1], dtype=np.uint8)  # Convert blob data to numpy array
        face_img = cv2.imdecode(face_img, cv2.IMREAD_GRAYSCALE)
        faces.append(face_img)
        face_ids.append(face_id)

    if len(faces) == 0:
        print("Error: No face images found in the database.")
        return

    # Train the recognizer on the faces and IDs
    recognizer.train(faces, np.array(face_ids))

    # Save the trained model to trainer.yml
    recognizer.save('trainer.yml')
    print("Training complete. Model saved as 'trainer.yml'.")

if __name__ == "__main__":
    train_model()
    cursor.close()
    conn.close()
