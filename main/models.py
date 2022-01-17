from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Genre(models.Model):
    slug = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.slug

VISIBILITY = (
    ('Public', 'Public'),
    ('Private', 'Private'),
)

class Audio(models.Model):
    title = models.CharField(max_length=150)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='audios')
    description = models.CharField(max_length=250, blank=True, null=True) # oprional
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audios') # more than one person can be on the track <- the person who uploaded the song
    visibility = models.CharField(choices=VISIBILITY, max_length=7)
    audio = models.FileField(upload_to='audios')
    likes = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f'"{self.title}", uploaded by {self.uploader}'

    def leave_like(self):
        self.likes += 1
        self.save()


class Comment(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment left by {self.user.email} on track titled '{self.audio.title}', track's id={self.audio.id}"

# class UploadedAudio(models.Model):
#     artist = models.ForeignKey(User, on_delete=models.CASCADE)
#     audio = models.ForeignKey(Audio, on_delete=models.CASCADE)
#     date_posted = models.DateField(auto_now_add=True)
