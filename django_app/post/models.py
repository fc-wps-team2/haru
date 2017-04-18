from django.conf import settings
from django.db import models


class Post(models.Model):
    EMOTION_HAPPY = 1
    EMOTION_BAD = 2
    EMOTION_USUALLY = 3

    EMOTION_STATUS = (
        (EMOTION_HAPPY, 'Happy'),
        (EMOTION_BAD, 'Bad'),
        (EMOTION_USUALLY, 'Usually'),

    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='post', blank=True)
    day = models.DateField(auto_now_add=True)
    status = models.IntegerField(choices=EMOTION_STATUS)

    # 제목에 숫자를 넣었을때 문자열로 바꿔서 저장.
    def __str__(self):
        return self.title
