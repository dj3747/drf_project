from rest_framework.exceptions import ValidationError


class VideoURLValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if not (value.startswith("https://youtube.com") or value.startswith("https://youtu.be")):
            raise ValidationError("Допустимы ссылки только на youtube.com или youtu.be")
