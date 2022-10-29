from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from face_recognition.faces import face_recognition

User = get_user_model()

class FaceRecognitionAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        email = face_recognition()
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