import ftplib
import cv2
from SimpleFacerec import SimpleFacerec
import mysql.connector
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from io import BytesIO
import face_recognition
from better_profanity import profanity

app = Flask(__name__)
CORS(app)
@app.route('/api/facialreco')
def FacialReco():

    HOSTNAME = "192.168.1.31"
    USERNAME = "ftp-user"
    PASSWORD = "ftpuser"

    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = "utf-8"
    print("connected")
    sfr = SimpleFacerec()

    try:
        connection = mysql.connector.connect(host='192.168.1.31',
                                             database='erppro',
                                             user='root',
                                             password='guessitplease',
                                             port="3306")

        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT email, image from user"""

        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        for row in record:
            username = row[0]
            image_path = row[1]

            print(f"Loading image for user {username} from FTP\n")

            file = BytesIO()
            ftp_server.retrbinary(f"RETR {image_path}", file.write)
            file.seek(0)
            image = face_recognition.load_image_file(file)

            # Encode the image
            encodings = face_recognition.face_encodings(image)
            if encodings:
                sfr.known_face_encodings.append(encodings[0])
                sfr.known_face_names.append(username)

    except mysql.connector.Error as error:
        print(f"Failed to read BLOB data from MySQL table {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    nameA = "Unknown"
    # Encoded known faces

    # Load camera
    cap = cv2.VideoCapture(0)
    
    

    while True:
        ret, frame = cap.read()

        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
            if name != "Unknown":
                nameA = name
                break

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 2:
            break
        if nameA != "Unknown":
            return nameA
            break

    cap.release()
    cv2.destroyAllWindows()
    return nameA

@app.route('/api/cencor')
def censor():

    text = request.args.get('text')
    custom_badwords = ['putain', 'merde', 'con','conne','ducon','connard','connasse','enculé','bordel','salaud','saloperie','Fils de pute']
    profanity.add_censor_words(custom_badwords)
    # text to be censored

    censored = profanity.censor(text, '-')

    return censored

if __name__ == "__main__":
    FacialReco()
