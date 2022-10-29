from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from face_recognition.faces import face_recognition

User = get_user_model()

class FaceRecognitionAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        csrf_token = request.COOKIES['csrftoken']
        face_auth_path = 'face_recognition/face_auth/face_auth_' + csrf_token + '.mp4'
        with open(face_auth_path, "wb+") as face_auth_file:
            for chunk in request.FILES['face_auth'].chunks():
                face_auth_file.write(chunk)
        face_auth_path = 'face_auth/face_auth_' + csrf_token + '.mp4'
        email = face_recognition(face_auth_path=face_auth_path)
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