import cv2
import pickle
import os

def face_recognition(face_auth_path):
    if os.path.basename(os.getcwd()) != "face_recognition":
        oldwd = os.getcwd()
        os.chdir("face_recognition")

    # Load recognize and read label from model
    recognizer = cv2.face.LBPHFaceRecognizer_create(radius=2, neighbors=7, grid_x=10, grid_y=10)

    recognizer.read("train.yml")

    labels = {}
    with open("labels.pickle", "rb") as f:
        labels = pickle.load(f)
        labels = {v: k for k, v in labels.items()}

    # Check face_auth video and detect face
    if not os.path.exists(face_auth_path):
        return "FACE VIDEO NOT FOUND"
    cap = cv2.VideoCapture(face_auth_path)
    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    recognized = False
    
    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(200, 200) 
        )

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            # predict the id and confidence for faces
            id_, conf = recognizer.predict(roi_gray)
            
            # If the face is recognized
            if conf < 100:
                # debugging information
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 0, 0)
                stroke = 2
                cv2.putText(frame, f"{name} conf={conf}", (x, y), font, 0.6, color, stroke, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
                cv2.imwrite("face_auth/face_detected.jpg", frame)
                
                recognized = True
                result = labels[id_]
                break
        
        if recognized:
            break
    os.remove(face_auth_path)
    if os.getcwd() != oldwd:
        os.chdir(oldwd)
    cap.release()
    cv2.destroyAllWindows()
    if recognized:
        return result
    return "UNKNOWN USER"
