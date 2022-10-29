import cv2
import pickle
import os

def face_recognition(face_auth_path="face_auth/face_auth_temp.mp4"):
    if os.path.basename(os.getcwd()) != "face_recognition":
        oldwd = os.getcwd()
        os.chdir("face_recognition")

    if not os.path.exists(face_auth_path):
        if os.getcwd() != oldwd:
            os.chdir(oldwd)
        return "FACE VIDEO NOT FOUND"
    cap = cv2.VideoCapture(face_auth_path)
    
    # Load recognize and read label from model
    recognizer = cv2.face.LBPHFaceRecognizer_create(radius=2, neighbors=6, grid_x=10, grid_y=10)

    recognizer.read("train.yml")

    labels = {}
    with open("labels.pickle", "rb") as f:
        labels = pickle.load(f)
        labels = {v: k for k, v in labels.items()}

    # Check face_auth video and detect face
    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

    recognized = False
    for i in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        ret, frame = cap.read()
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
            if conf >= 100:
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
