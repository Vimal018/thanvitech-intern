from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import bcrypt
import cv2
import numpy as np
import secrets
import os
from datetime import datetime
import threading
import time

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Secure random key

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'attendance_system'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def verify_password(stored_hash, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))

# Path to the file used for inter-process communication
face_detection_status_file = 'face_detection_status.txt'
confidence_threshold = 100  # Set appropriate threshold based on your model's performance

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "SELECT id, password FROM teacher WHERE name = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and verify_password(user[1], password):
            user_id = user[0]
            today_date = datetime.now().date()
            
            conn = get_db_connection()  # Reopen connection for another query
            try:
                cursor = conn.cursor()
                query = "SELECT COUNT(*) FROM attendance WHERE teacher_id = %s AND date = %s"
                cursor.execute(query, (user_id, today_date))
                attendance_count = cursor.fetchone()[0]
                cursor.close()

                if attendance_count > 0:
                    return "Attendance already marked for today."

                # Start face detection in a separate thread
                threading.Thread(target=face_detection_process, args=(user_id,)).start()
                
                # Check for face detection status
                while not os.path.exists(face_detection_status_file):
                    time.sleep(1)  # Wait for face detection to write to the file
                
                with open(face_detection_status_file, 'r') as f:
                    face_id_detected = f.read().strip()
                
                if face_id_detected:
                    os.remove(face_detection_status_file)  # Clean up the status file
                    return redirect(url_for('attendance'))
                else:
                    os.remove(face_detection_status_file)  # Clean up the status file
                    return "Face not recognized"
            finally:
                conn.close()
        else:
            return "Invalid username or password"
    finally:
        conn.close()

@app.route('/attendance')
def attendance():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "SELECT teacher_name, timestamp FROM attendance ORDER BY timestamp DESC"
        cursor.execute(query)
        attendance_records = cursor.fetchall()
        cursor.close()
        return render_template('attendance.html', records=attendance_records)
    finally:
        conn.close()

def face_detection_process(user_id):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    model_path = 'trainer.yml'
    if not os.path.exists(model_path):
        print("Model not found. Please train the model first.")
        return

    recognizer.read(model_path)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            face_id, confidence = recognizer.predict(face_img)
            
            if confidence < confidence_threshold:
                conn = get_db_connection()
                try:
                    cursor = conn.cursor()
                    query = "SELECT id, name FROM teacher WHERE id = %s"
                    cursor.execute(query, (face_id,))
                    result = cursor.fetchone()
                    cursor.close()
                    
                    if result:
                        teacher_id = result[0]
                        teacher_name = result[1]
                        
                        if teacher_id == user_id:
                            today_date = datetime.now().date()
                            conn = get_db_connection()  # Reopen connection for another query
                            try:
                                cursor = conn.cursor()
                                query = "SELECT COUNT(*) FROM attendance WHERE teacher_id = %s AND date = %s"
                                cursor.execute(query, (teacher_id, today_date))
                                attendance_count = cursor.fetchone()[0]
                                cursor.close()
                                
                                if attendance_count == 0:
                                    cursor = conn.cursor()
                                    query = "INSERT INTO attendance (teacher_id, teacher_name, date) VALUES (%s, %s, %s)"
                                    cursor.execute(query, (teacher_id, teacher_name, today_date))
                                    conn.commit()
                                    cursor.close()
                                    
                                    with open(face_detection_status_file, 'w') as f:
                                        f.write(str(teacher_id))
                                    cap.release()
                                    cv2.destroyAllWindows()
                                    return
                            finally:
                                conn.close()
                finally:
                    conn.close()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    app.run(debug=True)
