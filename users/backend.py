from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from face_recognition.faces import face_recognition

User = get_user_model()

class FaceRecognitionAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        # check if any files are submitted with the request, expected 1
        if len(request.FILES) == 0:
            return None

        # differentiate login videos by csrf tokens
        csrf_token = request.COOKIES['csrftoken']
        face_auth_path = 'face_auth/face_auth_' + csrf_token

        # only accept videos in mp4 (Safari) or webm (Chrome/Firefox) format
        # save the video locally at face_recognition/face_auth/
        if "face_auth_mp4" in request.FILES:
            face_auth_path += '.mp4'
            with open('face_recognition/' + face_auth_path, "wb+") as face_auth_file:
                for chunk in request.FILES['face_auth_mp4'].chunks():
                    face_auth_file.write(chunk)
        else:
            face_auth_path += '.webm'
            with open('face_recognition/' + face_auth_path, "wb+") as face_auth_file:
                for chunk in request.FILES['face_auth_webm'].chunks():
                    face_auth_file.write(chunk)
        
        # run face recognition
        email = face_recognition(face_auth_path=face_auth_path)

        # if a user's email is recognised and exists in the database, return that email address
        if email == "UNKNOWN USER" or email == "FACE VIDEO NOT FOUND":
            return None
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None