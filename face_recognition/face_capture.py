import cv2
import os
import sys, getopt

if len(sys.argv[1:]) == 0:
    print('Usage: face_capture.py -u <user_name> -n <num_imgs>')
    sys.exit(2)

# parse input arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "hu:n:", ["help", "user_name=", "num_imgs="])
except getopt.GetoptError as error:
    print('Usage: face_capture.py -u <user_name> -n <num_imgs>')
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print('face_capture.py -u <user_name> -n <num_imgs>')
        sys.exit()
    elif opt in ("-u", "--user_name"):
        user_name = arg
    elif opt in ("-n", "--num_imgs"):
        num_imgs = int(arg)

faceCascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(0)

# Specify the `user_name` and `num_imgs` here.
# user_name = "EMAIL_ADDRESS"
# num_imgs = 400
if not os.path.exists('data/{}'.format(user_name)):
    os.mkdir('data/{}'.format(user_name))

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (350, 50)
fontScale = 1
fontColor = (102, 102, 225)
lineType = 2

# Open camera
for cnt in range(1, num_imgs + 1):
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    frame_copy = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(200, 200),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    msg = "Saving {}'s Face Data [{}/{}]".format(user_name, cnt, num_imgs)
    cv2.putText(frame, msg,
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)


    # Display the resulting frame
    cv2.imshow('Video', frame)
    # Store the captured images in `data/Jack`
    cv2.imwrite("data/{}/{}{:03d}.jpg".format(user_name, user_name, cnt), frame_copy)

    key = cv2.waitKey(100)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
