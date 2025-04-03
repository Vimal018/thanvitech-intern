import mysql.connector
import bcrypt

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'attendance_system'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def hash_password(password):
    # Hash the password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def insert_teacher(name, face_image_path, password):
    hashed_password = hash_password(password)
    
    # Read the face image file and convert it to binary
    with open(face_image_path, 'rb') as file:
        face_image = file.read()
    
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Prepare SQL statement
        query = """
        INSERT INTO teacher (name, face_image, password) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (name, face_image, hashed_password))
        
        # Commit the transaction
        conn.commit()
        print("Record inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Example usage
# name = 'vimal'
# face_image_path = r'C:\Users\Vimal\OneDrive\Pictures\Camera Roll\WIN_20240729_11_09_15_Pro.jpg'  # Replace with actual path to the image file
# password = 'vimal2409'

# insert_teacher(name, face_image_path, password)

def update_password(name, new_password):
    hashed_password = hash_password(new_password)
    
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Prepare SQL statement
        query = """
        UPDATE teacher
        SET password = %s
        WHERE name = %s
        """
        cursor.execute(query, (hashed_password, name))
        
        # Commit the transaction
        conn.commit()
        print("Password updated successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()




# name = 'sam'
# face_image_path = r'C:\Users\Vimal\OneDrive\Pictures\Camera Roll\WIN_20240730_11_42_12_Pro.jpg'
# password = 'sam123'

# insert_teacher(name, face_image_path, password)

name = 'sam'
new_password = 'samNew123'

update_password(name, new_password)
